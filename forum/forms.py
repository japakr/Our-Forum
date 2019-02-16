from django import forms

from .models import Topic, Post

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'text']
        labels = {'text': ''}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        labels = {'text': ''}
