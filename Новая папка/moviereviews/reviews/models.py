from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg



class Genre(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    year = models.PositiveIntegerField()
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.FloatField(default=0)

    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_rating(self):
        """Пересчёт рейтинга фильма по отзывам"""
        avg = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        self.rating = round(avg, 1) if avg else 0
        self.save(update_fields=['rating'])

    def str(self):
        return self.title


class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    favorited_by = models.ManyToManyField(
        User, blank=True, related_name='favorite_reviews'
    )
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'film')    

    def str(self):
        return f"{self.author.username} – {self.film.title}"