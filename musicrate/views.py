import requests, json, datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import ReviewForm, SearchForm, UserForm
from .spotify_api_util import getTokenData
from django.http import Http404, JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Avg, Count

# Create your views here.
def album_list(request):
    return render(request, 'musicrate/album_list.html', {})

# Homepage. List of all reviews
def review_list(request):
	if(request.user.is_authenticated):
		feed_reviews = Review.objects.filter(reviewer__in=request.user.profile.follows.all()).order_by('-created')[:10]
	else:
		feed_reviews = None
	top_reviews = Review.objects.order_by('-rating', '-updated')[:10]
	new_reviews = Review.objects.order_by('-updated')[:10]
	return render(request, 'musicrate/review_list.html', {'feed_reviews':feed_reviews,'top_reviews':top_reviews, 'new_reviews':new_reviews})

def review_detail(request, pk):
	review = get_object_or_404(Review, pk=pk)
	return render(request, 'musicrate/review_detail.html', {'review':review})

def review_edit(request, pk):
	review = get_object_or_404(Review, pk=pk)
	print("Received request of type " + request.method)
	if request.method == "POST":
		form = ReviewForm(request.POST)
		print("Valid request: " + form.is_valid().__str__())
		if form.is_valid():
		    review.rating = form.cleaned_data['rating']
		    review.comment = form.cleaned_data['comment']
		    review.updated = timezone.now()
		    review.save()
		    print("Redirecting to detail view")
		    return redirect('review_detail', pk=review.pk)
	else:
	    form = ReviewForm(instance=review)
	    album = review.album
	return render(request, 'musicrate/review_edit.html', {'form': form, 'album': album, 'new': False})

# Modified to prepopulate with an album
def review_new(request, pk=None):
	if request.method == "POST":
		form = ReviewForm(request.POST)
		if form.is_valid():
		    review = form.save(commit=False)
		    review.reviewer = Profile.objects.get(user=request.user)
		    review.save()
		    return redirect('review_detail', pk=review.pk)
	elif pk is not None:
		# If  album is provided, initialize with album prepopulated
		album = get_object_or_404(Album, pk=pk)

		# Try to get the existing review, if there is one
		review = Review.objects.filter(reviewer=request.user.profile, album=album)
		
		# If single review exists
		if len(review) == 1:
			# Redirect user to edit it
			review = review[0]
			return redirect('review_edit', pk=review.pk)
		# If 0 reviews exist
		elif len(review) == 0:
			# Send up form with album prepopulated
			form = ReviewForm(initial={'album': album})
			# Render the form
			return render(request, 'musicrate/review_edit.html', {'form': form, 'album':album})
		else:
			# If the number of existing reviews from user for album is not 1 or 0
			# Something has gone horribly wrong.
			# Abort!
			return redirect('review_list')
	elif pk is None:
		# If album is not provided, give blank form
		form = ReviewForm()
		return render(request, 'musicrate/review_edit.html', {'form': form, 'new':True})

def album_detail(request, pk):
	# Try to get the album. If not found create one
	album, created = Album.objects.get_or_create(
		spotify_id=pk
	)
	# If new album was created
	if created is True:
		print("Creating a new album!")
		album_name = request.GET['name']
		album_artist = request.GET['artist']
		album_image = request.GET['img']
		print("New album: " + album_name + " by " + album_artist)
		# Populate the rest of the album
		album.title = album_name
		album.artist = album_artist
		album.art_url = album_image
		album.save()
		return redirect('/album/'+pk)
	else:
		reviews = Review.objects.filter(album=album)
		avg = reviews.aggregate(Avg('rating'))['rating__avg']
		reviews = reviews.annotate(Avg('rating'))
		return render(request, 'musicrate/album_detail.html', {'album':album, 'reviews':reviews, 'avg':avg})

def search(request):
	if request.method == "POST":
		form = SearchForm(request.POST)
		if form.is_valid():
			results = request.POST
			queryURL = buildQueryURL(request)
			token = getToken()
			results = getResults(queryURL, token)
			results = trimResults(results)
			return render(request, "musicrate/search_results.html", {'results': results})
	else:
		form = SearchForm()
	return render(request, "musicrate/search.html", {'form': form})

def create_user(request):
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			new_user = User.objects.create_user(**form.cleaned_data)
			# login(new_user)
			# redirect, or however you want to get to the main view
			return render(request, 'musicrate/review_list.html', {})
	else:
		form = UserForm() 
	return render(request, 'musicrate/signup.html', {'form': form})

def user_detail(request, user):
	user = Profile.objects.get(user__username=user)
	reviews = Review.objects.filter(reviewer=user).order_by('-updated', '-created')
	breakdown = Review.objects.filter(reviewer=user).values('rating').annotate(Count('rating'))
	labels = [0,1,2,3,4,5,6,7,8,9,10]
	data = [0,0,0,0,0,0,0,0,0,0,0]
	# User's average review
	avg = reviews.aggregate(Avg('rating'))['rating__avg']
	for x in breakdown:
		labels[x['rating']]=x['rating']
		data[x['rating']]=x['rating__count']
	breakdown = {'labels':labels, 'data':data}
	return render(request, 'musicrate/user_detail.html', {'user':user, 'reviews': reviews, 'breakdown':breakdown, 'avg':avg})

def user_follow(request, user):
	follower = Profile.objects.get(user=request.user)
	followee = Profile.objects.get(user__username=user)
	
	data = {}
	if follower in followee.followed_by.all():
		# Unfollow
		follower.follows.remove(followee);
		data['newbutton'] = "Follow"
		data['message'] = "No longer following " + followee.__str__()
	else:
		# Follow
		follower.follows.add(followee);
		data['newbutton'] = "Unfollow"
		data['message'] = "Now following " + followee.__str__()

	return JsonResponse(data, safe=False)

def artist_detail(request, artist):
	artist = artist.split('-')
	artist = ' '.join(artist)
	reviews = Review.objects.filter(album__artist__iexact=artist)
	reviews = reviews.values('album', 'album__title', 'album__art_url', 'album__artist').distinct().annotate(Avg('rating'))
	return render(request, 'musicrate/artist_detail.html', {'reviews':reviews});

# -------------------Spotify API Functions---------------------------------------------------------

# Takes search input from user, builds a URL to hit spotify API
def buildQueryURL(search_in):
	stem = "https://api.spotify.com/v1/search?q="
	query = ""
	artist = search_in.POST['artist']
	name = search_in.POST['name']	
	if name is not "":
		query += "album%3A" + name
	if artist is not "":
		query += "%20artist%3A" + artist
	query += "&type=album"
	return stem+query

# Requests and loads token for api authentication
def getToken():
	tokenData = getTokenData()
	r = requests.post(url = "https://accounts.spotify.com/api/token", data=tokenData)
	token_json = r.text
	parsed_json = json.loads(token_json)
	token = parsed_json["access_token"]
	return token

# Combines token and request URL to actually hit Spotify's API
def getResults(queryURL, token):
	headers = {"Authorization": "Bearer " + token}
	q = requests.get(url = queryURL, headers=headers)
	response = q.text
	return json.loads(response)

def trimResults(albums):
	results = []
	for album in albums['albums']['items']:
		result = {'name':album['name'],'artist':album['artists'][0]['name'], 'id':album['id'], 'img':album['images'][0]['url'], 'link':album['external_urls']['spotify']}
		results.append(result)
	return results


