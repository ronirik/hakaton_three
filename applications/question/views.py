from rest_framework import status, generics, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from applications.question.models import Category, Question, Answer, Like
from applications.question.permissions import IsQuestionAuthor
from applications.question.serializers import CategorySerializer, QuestionSerializer, AnswerSerializer
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend




class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Question create view
# class QuestionListView(generics.ListAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer


class QuestionCreateView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        elif self.action == 'like':
            permissions = [IsAuthenticated, ]
        else:
            permissions = [IsQuestionAuthor, ]
        return [permission() for permission in permissions]


class QuestionUpdateView(generics.UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsQuestionAuthor, ]


class QuestionDeleteView(generics.DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsQuestionAuthor, ]


# CRUD for answers
class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, ]

    @action(detail=True, methods=['POST'])
    def like(self, request, *args, **kwargs):
        question = self.get_object().question
        like_obj, _ = Like.objects.get_or_create(question=question,
                                                 user=request.user)
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'liked'
        if not like_obj.like:
            status = 'unliked'
        return Response({'status': status})


# class QuestionYearFilter(rest_framework.FilterSet):
#     min_public_date = rest_framework.DateFilter(field_name='public_date', lookup_expr='gte')
#     max_public_date = rest_framework.DateFilter(field_name='public_date', lookup_expr='lte')
#
#     class Meta:
#         model = Question
#         fields = [
#             'min_public_date',
#             'max_public_date',
#             'category',
#         ]

class QuestionCategoryFilter(rest_framework.FilterSet):
    # min_year = rest_framework.DataFilter(field_name='year', lookup_expr='gte')
    # max_year = rest_framework.NumberFilter(field_name='year', lookup_expr='lte')

    class Meta:
        model = Question
        fields = [
            'category',
        ]

class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_class = QuestionCategoryFilter
    search_fields = ['title', 'problem', ]

    def get_serializer_context(self):
        return {'request': self.request}

class QuestionDetailView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


