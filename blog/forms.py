from django import forms
from .models import Post,Category
from ckeditor.widgets import CKEditorWidget  # Import CKEditorWidget

class PostForm(forms.ModelForm):
   class Meta:
        model = Post
        fields = ['title', 'category', 'image', 'content']
        # widgets = {
        #     'content':forms.CharField(widget=CKEditorWidget()),
        # }
