from survey.models import Question, Answer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import *


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows questions to be viewed.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=False)
    def count(self, request):
        return Response({'count': Question.objects.count()})
