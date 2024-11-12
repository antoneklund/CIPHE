from django.db import models
from django.core.validators import int_list_validator


class Survey(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    prolific_identity = models.CharField(max_length=100, default="")
    current_cluster_index = models.IntegerField(default=0)
    cluster_order = models.CharField(
        max_length=200, default=[], validators=[int_list_validator]
    )
    article_ids = models.CharField(
        max_length=4096, default=[], validators=[int_list_validator]
    )


class Cluster(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.SET_NULL, null=True)
    # original_cluster = models.IntegerField(default=0)


class Page(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cluster = models.ForeignKey(Cluster, on_delete=models.SET_NULL, null=True)
    order = models.IntegerField(default=0)


class Article(models.Model):
    cluster = models.ForeignKey(Cluster, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=1000)


class UFQuestion(models.Model):
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True)
    CHOICES = [("event", "Event"), ("theme", "Theme"), ("other", "Other")]
    uf_choices = models.CharField(
        max_length=20, choices=CHOICES, blank=False, null=True
    )
    text_answer = models.CharField(max_length=50, null=True, default="")
    excluded = models.CharField(max_length=200, null=True, default="None")


class TaxonomyQuestion(models.Model):
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True)
    CATEGORIES = [
        ("culture", "Culture"),
        ("entertainment", "Entertainment"),
        ("news-politics", "News-Politics"),
        ("news-crime", "News-Crime"),
        ("news-war", "News-War"),
        ("lifestyle", "Lifestyle"),
        ("science", "Science"),
        ("home-garden", "Home & Garden"),
        ("sports", "Sports"),
        ("business-finance", "Business & Finance"),
        ("personal-finance", "Personal Finance"),
        ("automotive", "Automotive"),
        ("weather", "Weather"),
        ("technology", "Technology"),
        ("environment", "Environment"),
        ("real-estate", "Real Estate"),
        ("other", "Other"),
    ]
    category = models.CharField(
        max_length=30, choices=CATEGORIES, blank=False, null=True
    )
    text_answer = models.CharField(max_length=200, null=True, default="")


class CharacteristicsQuestion(models.Model):
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True)
    CHOICES = [
        ("strongly_disagree", "Strongly Disagree"),
        ("disagree", "Disagree"),
        ("neutral", "Neutral"),
        ("agree", "Agree"),
        ("strongly_agree", "Strongly Agree"),
    ]
    theme = models.CharField(max_length=20, choices=CHOICES, null=True, blank=True)
    opinion = models.CharField(max_length=20, choices=CHOICES, null=True, blank=True)
    emotion = models.CharField(max_length=20, choices=CHOICES, null=True, blank=True)


class LikertScaleQuestion(models.Model):
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True)
    CHOICES = [
        ("strongly_disagree", "Strongly Disagree"),
        ("disagree", "Disagree"),
        ("neutral", "Neutral"),
        ("agree", "Agree"),
        ("strongly_agree", "Strongly Agree"),
    ]
    inclusion = models.CharField(max_length=20, choices=CHOICES, null=True, blank=True)
    naming = models.CharField(max_length=20, choices=CHOICES, null=True, blank=True)
    opinion = models.CharField(max_length=20, choices=CHOICES, null=True, blank=True)
    emotion = models.CharField(max_length=20, choices=CHOICES, null=True, blank=True)
    interest = models.CharField(max_length=20, choices=CHOICES, null=True, blank=True)
    style = models.CharField(max_length=20, choices=CHOICES, null=True, blank=True)


class ArticleQuestion(models.Model):
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True)
    selected = models.CharField(max_length=1000)
