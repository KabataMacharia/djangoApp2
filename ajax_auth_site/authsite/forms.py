from django import forms
from authsite.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # exclude = ['author', 'updated', 'created', ]
        fields = ['text','email', 'password']
        widgets = {
            'text': forms.TextInput(
                attrs={'id': 'post-text', 'required': True}
            ),
            'email': forms.TextInput(
                attrs={'id': 'email', 'required': True, 'placeholder': 'Email Address'}
            ),
            'password': forms.TextInput(
                attrs={'id': 'password', 'required': True, 'placeholder': 'Password here'}
            ),
        }
