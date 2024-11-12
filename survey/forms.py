from django import forms
from .models import (
    LikertScaleQuestion,
    UFQuestion,
    ArticleQuestion,
    TaxonomyQuestion,
    CharacteristicsQuestion,
)


class UFForm(forms.ModelForm):
    class Meta:
        model = UFQuestion
        fields = ["uf_choices", "text_answer", "excluded"]
        widgets = {
            "uf_choices": forms.RadioSelect(attrs={"class": "horizontal-radio"}),
            "text_answer": forms.TextInput(attrs={"class": "freetext"}),
            "excluded": forms.TextInput(attrs={"class": "freetext"}),
        }


class FTForm(forms.ModelForm):
    class Meta:
        model = UFQuestion
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


class CharacteristicsForm(forms.ModelForm):
    LIKERT_CHOICES = [
        ("strongly_disagree", "Strongly Disagree"),
        ("disagree", "Disagree"),
        ("neutral", "Neutral"),
        ("agree", "Agree"),
        ("strongly_agree", "Strongly Agree"),
    ]
    theme = forms.ChoiceField(
        label="... a common topic, theme or event. (Stock market, Politics, Olympics)",
        choices=LIKERT_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "horizontal-radio"}),
    )
    opinion = forms.ChoiceField(
        label="... conveying the author's opinion about something. (debate, review, perspective)",
        choices=LIKERT_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "horizontal-radio"}),
    )
    emotion = forms.ChoiceField(
        label="... creating an emotional response. (heartwarming, anger, fear)",
        choices=LIKERT_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "horizontal-radio"}),
    )

    class Meta:
        model = CharacteristicsQuestion
        fields = ["theme", "opinion", "emotion"]


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
