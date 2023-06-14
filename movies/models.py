from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Avg

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        existing_actor = Actor.objects.filter(name=self.name).first()
        if existing_actor and existing_actor != self:
            raise ValidationError("Director with this name already exists.")
        super().save(*args, **kwargs)


class Director(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=40, blank=True, default='movie name')
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=1000, blank=True, default='movie description')
    image = models.ImageField(upload_to='movie_images/')
    year = models.IntegerField(null=True)
    actor = models.ManyToManyField(Actor, blank=True)
    directors = models.ForeignKey(Director, on_delete=models.CASCADE, blank=True, null=True)
    genre = models.ManyToManyField(Genre, blank=True)
    is_exclusive = models.BooleanField(default=False, verbose_name='Эксклюзивный')

    @property
    def average_rating(self):
        return self.rating_set.aggregate(avg_rating=Avg('star')).get('avg_rating', 0)

    def __str__(self):
        return self.name


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.movie.name}'


class RatingStar(models.Model):
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'
        ordering = ['value']


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')


    def __str__(self):
        return f'{self.star} -{self.user.username}  : {self.movie.name}'