from django import forms
from .models import (
    LikertScaleQuestion,
    NameQuestion,
    ArticleQuestion,
    TaxonomyQuestion,
)


class NameForm(forms.ModelForm):
    class Meta:
        model = NameQuestion
        fields = ["text_answer"]
        widgets = {
            "text_answer": forms.TextInput(attrs={"class": "freetext"}),
        }


class TaxonomyForm(forms.ModelForm):
    class Meta:
        model = TaxonomyQuestion
        fields = ["text_answer", "category"]
        widgets = {
            "text_answer": forms.TextInput(attrs={"class": "freetext"}),
            "category": forms.Select(attrs={"class": "category"}),
        }


class LikertScaleForm(forms.ModelForm):
    LIKERT_CHOICES = [
        ("strongly_disagree", "Strongly Disagree"),
        ("disagree", "Disagree"),
        ("neutral", "Neutral"),
        ("agree", "Agree"),
        ("strongly_agree", "Strongly Agree"),
    ]
    inclusion = forms.ChoiceField(
        label="It was easy to choose which articles to include and exclude.",
        choices=LIKERT_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "horizontal-radio"}),
    )
    naming = forms.ChoiceField(
        label="It was easy to name the group.",
        choices=LIKERT_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "horizontal-radio"}),
    )
    opinion = forms.ChoiceField(
        label="I feel the group is important from a societal perspective.",
        choices=LIKERT_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "horizontal-radio"}),
    )
    emotion = forms.ChoiceField(
        label="I get a negative emotional response from the group content. (e.g., anger, sadness, fear).",
        choices=LIKERT_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "horizontal-radio"}),
    )
    interest = forms.ChoiceField(
        label="I found the group engaging.",
        choices=LIKERT_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "horizontal-radio"}),
    )
    style = forms.ChoiceField(
        label="I percieved the articles similar to each other.",
        choices=LIKERT_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "horizontal-radio"}),
    )

    class Meta:
        model = LikertScaleQuestion
        fields = ["inclusion", "naming", "opinion", "emotion", "interest", "style"]


class ArticleForm(forms.Form):
    class Meta:
        model = ArticleQuestion
