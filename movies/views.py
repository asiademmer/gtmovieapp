import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required

API_URL = "https://api.themoviedb.org/3/movie/"
API_KEY = "6729c4cad6820ce8cfdfc6ffe135b332"


def index(request):
    search_term = request.GET.get('search')
    page_number = request.GET.get('page', 1)

    # Fetch movies from API
    response = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&page={page_number}")

    # Debugging: Print the raw response text to check for any issues
    if response.status_code == 200:
        try:
            api_movies = response.json().get('results', [])  # Parse the JSON
        except ValueError as e:
            print("Error parsing JSON:", e)
            api_movies = []
    else:
        api_movies = []

    total_pages = response.json().get('total_pages', 1) if api_movies else 1

    if search_term:
        api_movies = [movie for movie in api_movies if search_term.lower() in movie["title"].lower()]

    template_data = {
        'title': 'Movies',
        'movies': api_movies,
        'page': int(page_number),
        'total_pages': total_pages,
    }
    return render(request, 'movies/index.html', {'template_data': template_data})


def show(request, id):
    # Fetch movie details from TMDb API
    response = requests.get(f"{API_URL}{id}?api_key={API_KEY}")
    if response.status_code == 200:
        movie_details = response.json()
    else:
        movie_details = None

    # Get reviews from the database
    reviews = Review.objects.filter(movie_id=id)

    template_data = {
        'title': movie_details['title'] if movie_details else 'Movie Not Found',
        'movie': movie_details,
        'reviews': reviews,
    }

    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)