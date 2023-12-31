from django import forms
from .models import Post, Comment, MessageModel


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

class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)
    
class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=100)
    image = forms.ImageField(required= False)
    
    class Meta:
        model = MessageModel
        fields = ['body', 'image']
        
class ExploreForm(forms.Form):
    query = forms.CharField(label='',
                            widget= forms.TextInput(attrs={
                                'placeholder': 'Explore tags',
                            }))