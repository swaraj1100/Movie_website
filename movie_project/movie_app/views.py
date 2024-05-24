
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import MovieForm
from .forms import RatingForm
from django.contrib import messages
from .models import Movie, Rating, Comment
from .forms import CommentForm
from .models import Category,Movie

def home(request):
    return render(request,'index.html')


def your_view(request):
    categories = Category.objects.all()
    return render(request, 'movie_list.html', {'categories': categories})


def register(request):
    if request.method == 'POST':
        print(request.POST)
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already taken.")
                return redirect('register')

            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")

            else:

                user = User.objects.create_user(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
                user.save()

        else:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        return redirect('login')
    return render(request, 'sign-up.html')



def movies_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    movies = Movie.objects.filter(category=category)
    return render(request, 'movies_by_category.html', {'category': category, 'movies': movies})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('movie_list')


        else:
            messages.info(request, "invalid credentials")
            return redirect('login')

    return render(request, "sign-in.html")



def my_logout_view(request):
    logout(request)

    return redirect('home')

@login_required
def movie_list(request):
    query = request.GET.get('q')
    categories = Category.objects.all()
    if query:
        movies = Movie.objects.filter(name__icontains=query)
    else:
        movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies, 'categories': categories})

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.uploaded_by = request.user
            movie.save()
            messages.success(request, 'Movie added successfully')
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form})

@login_required
def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk, uploaded_by=request.user)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movie updated successfully')
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)
    return render(request, 'edit_movie.html', {'form': form})

@login_required
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk, uploaded_by=request.user)
    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'Movie deleted successfully')
        return redirect('movie_list')
    return render(request, 'delete_movie.html', {'movie': movie})



def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    ratings = Rating.objects.filter(pk=pk)
    comments = movie.comments.all()

    if request.method == 'POST':
        if 'rate_movie' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.movie = movie
                rating.user = request.user
                rating.save()
                messages.success(request, 'Your rating has been submitted.')
                return redirect('movie_detail', pk=pk)
            else:
                messages.error(request, 'Error submitting your rating. Please try again.')
                comment_form = CommentForm()
        elif 'comment_movie' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.movie = movie
                comment.user = request.user
                comment.save()
                messages.success(request, 'Your comment has been submitted.')
                return redirect('movie_detail', pk=pk)
            else:
                messages.error(request, 'Error submitting your comment. Please try again.')
                rating_form = RatingForm()
    else:
        rating_form = RatingForm()
        comment_form = CommentForm()

    context = {
        'movie': movie,
        'ratings': ratings,
        'comments': comments,
        'rating_form': rating_form,
        'comment_form': comment_form,

    }
    return render(request, 'movie_detail.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        return redirect('movie_list')
    else:
        return render(request, 'edit_profile.html')



def search_results(request):
    query = request.GET.get('q')
    if query:

        movies = Movie.objects.filter(name__icontains=query)
    else:
        movies = Movie.objects.all()
    return render(request, 'search.html', {'movies': movies, 'query': query})



@login_required
def view_profile(request):
    return render(request, 'profile.html')


