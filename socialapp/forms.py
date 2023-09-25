from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'rows': '4',
        'placeholder': 'What\'s on your mind?',

    }))
    
    image = forms.ImageField(required= False)

    class Meta:
        model = Post
        fields = ['content' , 'image']


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'rows': '4',
        'placeholder': 'Write a comment...',
    }))

    class Meta:
        model = Comment
        fields = ['content']
