from django.contrib import admin
from django.urls import path, include
from .views import QuestionAnswerView

urlpatterns = [
    path('qna/', QuestionAnswerView.as_view()),
]



