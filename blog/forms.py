from django import forms

from .models import Comment


class EmailShareForm(forms.Form):
    title = forms.CharField(max_length=25, required=True,
                            widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Name'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'E-Mail'}))
    to = forms.EmailField(required=True,
                          widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'To'}))
    comment = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={"class": "form-control mb-1", 'placeholder': 'Comments'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Текст комментария'}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Enter search term...'}))
