from django.test import TestCase
from .models import *


class TestWithFilledDb(TestCase):
    def setUp(self):
        survey = Survey.objects.create(title='survey title')
        q1 = Question.objects.create(
            type=AnswerType.SINGLE,
            text='question one text',
            survey=survey
        )
        a1 = Answer.objects.create(text='answer1', question=q1)
        a2 = Answer.objects.create(text='answer2', question=q1)

        q2 = Question.objects.create(
            type=AnswerType.MULTIPLE,
            text='question two text',
            survey=survey
        )
        a3 = Answer.objects.create(text='answer3', question=q2)
        a4 = Answer.objects.create(text='answer4', question=q2)

        q3 = Question.objects.create(
            type=AnswerType.TEXT,
            text='question three text',
            survey=survey
        )

        s = Session.objects.create()
        # single choice question result
        r1 = Result.objects.create(session=s, question=q1)
        r1.answers.add(a1)

        # multiple choices question result
        r2 = Result.objects.create(session=s, question=q2)
        r2.answers.add(a3)
        r2.answers.add(a4)

        # text answer question result
        rans = Answer.objects.create(text='random answer', question=q3)
        r3 = Result.objects.create(session=s, question=q3)
        r3.answers.add(rans)

        RecordedData.objects.create(
            result=r3,
            timestamp='00:00',
            surprise=0.1,
            fear=0.3,
            happiness=0.1,
            anger=0.0,
            disgust=0.0,
            sadness=0.0,
            neutral=0.5,
        )


class SurveyTestCase(TestWithFilledDb):
    def test_all_questions_can_be_queried_by_survey_title(self):
        questions = Question.objects.filter(survey__title__contains='survey title')
        self.assertEqual(len(questions), 3)
        self.assertEqual(questions[0].text, 'question one text')
        self.assertEqual(questions[1].text, 'question two text')
        self.assertEqual(questions[2].text, 'question three text')
