from django import forms
from .models import Movie
from .models import Rating,Comment



class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'poster', 'youtube_link', 'description', 'category', 'actors', 'year']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

