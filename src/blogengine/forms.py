from django import forms

from blogengine.models import Post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "text"
        ]
