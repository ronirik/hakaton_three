from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.question.views import CategoryListView, QuestionCreateView, QuestionListView, QuestionUpdateView, \
    QuestionDeleteView, AnswerViewSet, QuestionDetailView

router = DefaultRouter()
router.register('answers', AnswerViewSet)

urlpatterns = [
    path('categories-list/', CategoryListView.as_view()),
    path('create/', QuestionCreateView.as_view()),
    path('list/', QuestionListView.as_view()),
    path('update/<int:pk>/', QuestionUpdateView.as_view()),
    path('delete/<int:pk>/', QuestionDeleteView.as_view()),
    path('', include(router.urls)),
    # path('list/', QuestionListView.as_view()),
    path('<int:pk>/', QuestionDetailView.as_view()),
    # path('<int:pk>/favorite/', FavoriteView.as_view())
]
# urlpatterns.extend(router.urls)
