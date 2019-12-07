from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from .models import *


class AnswerNestedInline(NestedStackedInline):
    model = Answer
    extra = 1


class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    inlines = [AnswerNestedInline]


class SurveyAdmin(NestedModelAdmin):
    model = Survey
    inlines = [QuestionInline]


admin.site.register(Survey, SurveyAdmin)
