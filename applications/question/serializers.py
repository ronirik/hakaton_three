from rest_framework import serializers

from applications.question.models import Category, Question, Answer, Like


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('id', 'question', 'solution', 'image')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author_id'] = request.user.id
        answer = Answer.objects.create(**validated_data)
        return answer


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'category', 'title', 'image', 'problem', 'answer')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author_id'] = request.user.id
        question = Question.objects.create(**validated_data)
        return question

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['category'] = instance.category.title
        # rep['user'] = f'{instance.user}'
        total_rating = [i.rating for i in instance.answer.all()]
        if len(total_rating) != 0:
            rep['total_rating'] = sum(total_rating)/len(total_rating)
        else:
            rep['total_rating'] = ''
        rep['like'] = instance.like.filter(like=True).count()
        rep['author'] = instance.author.email
        rep['solutions'] = AnswerSerializer(Answer.objects.filter(question=instance.id),
                                                                  many=True).data
        return rep

