"""определяет формы связанные с моделями приложения
формы обрабатывают пользовательский ввод и обработывают данные"""
from django import forms
from django.utils import timezone

from blog.models import Comment, Post


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.now()#установка начального значения на текущее время


    class Meta:#определяет мета информацию формы
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'format': '%Y-%m-%dT%H:%M'
            }),#натсройка виджетов для полей формы
        }


class CommentForm(forms.ModelForm):#форма для экземпляров модели comment
    class Meta:
        model = Comment
        exclude = ('author', 'post', 'is_published')
