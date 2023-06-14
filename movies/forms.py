from django import forms
from .models import RatingStar, Rating, Comment


class RatingForm(forms.Form):
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ('star', )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'message')