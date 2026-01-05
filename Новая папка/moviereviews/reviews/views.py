from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

from .models import Film, Genre, Review, Favorite
from .forms import RegisterForm

# Главная страница
def home(request):
    films = Film.objects.all().order_by('-created_at')
    return render(request, 'reviews/home.html', {'films': films})

# Каталог фильмов с фильтром и сортировкой
def film_list(request):
    films = Film.objects.all()
    genres = Genre.objects.all()
    genre_id = request.GET.get('genre')
    if genre_id:
        try:
            genre_id = int(genre_id)
            films = films.filter(genre_id=genre_id)
        except ValueError:
            pass
    sort = request.GET.get('sort')
    if sort == 'rating':
        films = films.order_by('-rating')
    elif sort == 'year':
        films = films.order_by('-year')
    else:
        films = films.order_by('-created_at')
    context = {
        'films': films,
        'genres': genres,
        'selected_genre': genre_id,
        'selected_sort': sort,
    }
    return render(request, 'reviews/film_list.html', context)

# Детали фильма
def film_detail(request, pk):
    film = get_object_or_404(Film, pk=pk)
    reviews = film.reviews.all().order_by('-created_at')
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, film=film).exists()
    return render(request, 'reviews/film_detail.html', {
        'film': film,
        'reviews': reviews,
        'is_favorite': is_favorite
    })

# Добавление отзыва
@login_required
@require_POST
def add_review(request, pk):
    film = get_object_or_404(Film, pk=pk)
    text = request.POST.get('text')
    rating = request.POST.get('rating')
    if text and rating:
        Review.objects.create(film=film, author=request.user, text=text, rating=int(rating))
    return redirect('film_detail', pk=pk)

# Удаление отзыва
@login_required
@require_POST
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.author == request.user or request.user.is_staff:
        review.delete()
    return redirect('film_detail', pk=review.film.pk)


# Лайк отзыва
@login_required
@require_POST
def favorite_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user in review.favorited_by.all():
        review.favorited_by.remove(request.user)
    else:
        review.favorited_by.add(request.user)
    return redirect('film_detail', pk=review.film.pk)

# Регистрация
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['nickname']
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'reviews/register.html', {'form': form})

# Вход по email
def login_view(request):
    error = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                error = 'Неверный пароль'
        except User.DoesNotExist:
            error = 'Пользователь не найден'
    return render(request, 'reviews/login.html', {'error': error})

# Выход
def logout_view(request):
    logout(request)
    return redirect('home')
