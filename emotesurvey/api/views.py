from survey.models import Question, Answer, Result
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from . import serializers


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows questions to be viewed.
    """
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer

    @action(detail=False)
    def count(self, request):
        return Response({'count': Question.objects.count()})


class ResultsViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    def get_queryset(self):
        return Result.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.RawResultSerializer
        return serializers.ResultSerializer

    def create(self, request):
        #TODO(srgynmv): use RawResultSerializer to process the incoming result.
        pass
