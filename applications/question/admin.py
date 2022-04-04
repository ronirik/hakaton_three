from django.contrib import admin

from applications.question.models import Category, Question

admin.site.register(Category)
admin.site.register(Question)
