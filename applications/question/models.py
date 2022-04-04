from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='question')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='question')
    title = models.TextField()
    image = models.ImageField(upload_to='')
    problem = models.TextField()
    public_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='answer')
    solution = models.TextField()
    image = models.ImageField(upload_to='', blank=True)
    public_date = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(10), MinValueValidator(1)])

    def __str__(self):
        return self.question.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='like')
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='like')
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.like









