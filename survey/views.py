from django.shortcuts import render, redirect
from .models import (
    Article,
    User,
    LikertScaleQuestion,
    NameQuestion,
    ArticleQuestion,
    Page,
    Survey,
    Cluster,
    TaxonomyQuestion,
)
from .forms import LikertScaleForm, NameForm, TaxonomyForm
import random as r
from django.middleware import csrf
import ast
import numpy as np


SURVEY_ID = 2  # Change which survey should be live
SAMPLE_SIZE = 10  # only for calculating the score on thank_you page
INSTRUCTION_SET = "FT"  # Choose between FreeText "FT" and Taxonomy "TAX"
ARTICLE_PATH = None  # TODO: work to remove


def welcome(request):
    if request.method == "POST":
        prolific_id = request.POST.get("prolific_id")
        request.session["prolific_id"] = prolific_id
        return instruction(request)

    return render(request, "survey/welcome.html", {})


def create_anonymous_user(prolific_id, cluster_order):
    print("Creating new user")
    user = User()
    user.prolific_identity = prolific_id
    user.cluster_order = cluster_order
    user.current_cluster_index = 0
    user.save()
    return user


def create_page(request, user):
    page = Page()
    page.user = user
    page.save()
    request.session["page_id"] = page.id
    return page


def get_page(user):
    if Page.objects.filter(user_id=user.id, order=user.current_cluster_index).exists():
        page = Page.objects.filter(user_id=user.id, order=user.current_cluster_index)[0]
    else:
        page = -1
    return page


def page_has_responses(page):
    return LikertScaleQuestion.objects.filter(page=page).exists()


def get_survey(survey_id=SURVEY_ID):
    survey = Survey.objects.get(pk=SURVEY_ID)
    return survey


def get_user(request):
    user_id = request.session.get("user_id")
    if user_id:
        user = User.objects.get(pk=user_id)
    return user


def get_clusters(survey_id):
    clusters = Cluster.objects.filter(survey_id=survey_id)
    return clusters


def setup_cluster_order(clusters):
    cluster_ids = [c.id for c in clusters]
    r.shuffle(cluster_ids)
    return cluster_ids


def check_user_exists(prolific_id):
    exists = User.objects.filter(prolific_identity=prolific_id).exists()
    return exists


def instruction(request):
    survey = get_survey(survey_id=SURVEY_ID).id
    if check_user_exists(request.session["prolific_id"]):
        print("User exists. Loading user data...")
        user = User.objects.filter(prolific_identity=request.session["prolific_id"])[0]
    else:
        clusters = get_clusters(survey_id=survey)
        cluster_order = setup_cluster_order(clusters)
        user = create_anonymous_user(
            request.session["prolific_id"], cluster_order
        )
    request.session["user_id"] = user.id
    return render(request, "survey/instruction.html", {"user": user})


def convert_to_bool_list(selected, all_articles):
    all_articles = [str(a) for a in all_articles]
    selected_processed = []
    for a in all_articles:
        if a in selected:
            selected_processed.append(True)
        else:
            selected_processed.append(False)
    return selected_processed


def save_current_page(user, request):
    if INSTRUCTION_SET == "FT":
        naming_form = NameForm(request.POST)
    elif INSTRUCTION_SET == "TAX":
        naming_form = TaxonomyForm(request.POST)
    likert_form = LikertScaleForm(request.POST)

    article_ids = request.POST.getlist("article_ids")
    article_ids = str(article_ids)

    page = get_page(user)
    if page_has_responses(page):
        print("Page has responses")
        article_instance = ArticleQuestion.objects.get(page=page)
        likert_instance = LikertScaleQuestion.objects.get(page=page)

        naming_responses = naming_form.save(commit=False)
        if INSTRUCTION_SET == "FT":
            naming_instance = NameQuestion.objects.get(page=page)
            naming_instance.text_answer = naming_responses.text_answer
        elif INSTRUCTION_SET == "TAX":
            naming_instance = TaxonomyQuestion.objects.get(page=page)
            naming_instance.category = naming_responses.category
            naming_instance.text_answer = naming_responses.text_answer
        naming_instance.save()
        article_instance.selected = article_ids
        article_instance.save()
        likert_responses = likert_form.save(commit=False)
        likert_instance.inclusion = likert_responses.inclusion
        likert_instance.naming = likert_responses.naming
        likert_instance.opinion = likert_responses.opinion
        likert_instance.emotion = likert_responses.emotion
        likert_instance.interest = likert_responses.interest
        likert_instance.style = likert_responses.style
        likert_instance.save()
    else:
        article_instance = ArticleQuestion()
        article_instance.page = page
        article_instance.selected = article_ids
        article_instance.save()
        naming_instance = naming_form.save(commit=False)
        naming_instance.page = page
        naming_instance.save()
        likert_instance = likert_form.save(commit=False)
        likert_instance.page = page
        likert_instance.save()


def load_current_page_content(user, request):
    page = get_page(user)
    if page == -1:
        return redirect("survey_page")

    if page_has_responses(page):
        if INSTRUCTION_SET == "FT":
            naming_instance = NameQuestion.objects.get(page_id=page.id)
            naming_form = NameForm(instance=naming_instance)
        elif INSTRUCTION_SET == "TAX":
            naming_instance = TaxonomyQuestion.objects.get(page_id=page.id)
            naming_form = TaxonomyForm(instance=naming_instance)

        likert_instance = LikertScaleQuestion.objects.get(page_id=page.id)
        likert_form = LikertScaleForm(instance=likert_instance)
        cluster_order = ast.literal_eval(user.cluster_order)
        cluster_id = cluster_order[user.current_cluster_index]
        articles = Article.objects.filter(cluster_id=cluster_id)
        selected_articles = ast.literal_eval(
            ArticleQuestion.objects.get(page_id=page.id).selected
        )
        checkbox_bool_list = convert_to_bool_list(
            selected_articles, articles.values_list("id", flat=True)
        )
        for article, checkbox_bool in zip(articles, checkbox_bool_list):
            article.checkbox_bool = checkbox_bool
        token = csrf.get_token(request)
        request.session["form_token"] = token
        progress_percentage = (user.current_cluster_index / len(cluster_order)) * 100
        return render(
            request,
            "survey/survey_page.html",
            {
                "articles": articles,
                "likert_form": likert_form,
                "naming_form": naming_form,
                "user": user,
                "form_token": token,
                "progress_percentage": progress_percentage,
            },
        )
    else:
        return redirect("survey_page")


def load_new_page(user, request):
    try:
        page = create_page(request, user)
        cluster_order = ast.literal_eval(user.cluster_order)
        current_cluster_id = cluster_order[user.current_cluster_index]
        cluster = Cluster.objects.get(pk=current_cluster_id)
        page.cluster = cluster
        page.survey = get_survey(SURVEY_ID)
        page.order = user.current_cluster_index
        page.save()
    except IndexError:
        return redirect("thank_you")
    likert_form = LikertScaleForm()
    if INSTRUCTION_SET == "FT":
        naming_form = NameForm()
    elif INSTRUCTION_SET == "TAX":
        naming_form = TaxonomyForm()
    articles = Article.objects.filter(cluster_id=current_cluster_id)
    token = csrf.get_token(request)
    request.session["form_token"] = token
    progress_percentage = np.round(
        (user.current_cluster_index / len(cluster_order)) * 100, decimals=1
    )
    print(articles)
    return render(
        request,
        "survey/survey_page.html",
        {
            "articles": articles,
            "likert_form": likert_form,
            "naming_form": naming_form,
            "user": user,
            "form_token": token,
            "progress_percentage": progress_percentage,
        },
    )


def handle_next_button(user, request):
    save_current_page(user, request)
    user.current_cluster_index += 1
    user.save()
    return load_current_page_content(user, request)


def handle_back_button(user, request):
    save_current_page(user, request)
    user.current_cluster_index -= 1
    user.save()
    return load_current_page_content(user, request)


def handle_thank_you_back_button(user, request):
    user.current_cluster_index -= 1
    user.save()
    return load_current_page_content(user, request)


def survey_page(request):
    user = get_user(request)
    if request.method == "POST":
        if "action" in request.POST:
            if request.POST["action"] == "next":
                return handle_next_button(user, request)

            elif request.POST["action"] == "back":
                return handle_back_button(user, request)
    else:
        return load_new_page(user, request)


def calculate_model_score(article_responses):
    scores = []
    for response in article_responses:
        converted_response = ast.literal_eval(response.selected)
        scores.append(1 - (len(converted_response) / SAMPLE_SIZE))
    final_score = np.mean(scores)
    return final_score, scores


def thank_you(request):
    user = get_user(request)
    if request.method == "POST":
        return handle_thank_you_back_button(user, request)
    survey = Survey.objects.get(id=SURVEY_ID)

    name_responses = NameQuestion.objects.filter(page__user=user)
    if INSTRUCTION_SET == "TAX":
        name_responses = TaxonomyQuestion.objects.filter(page__user=user)

    likert_responses = LikertScaleQuestion.objects.filter(page__user=user)

    article_responses = ArticleQuestion.objects.filter(page__user=user)
    total_score, detailed_scores = calculate_model_score(article_responses)
    responses = zip(name_responses, likert_responses, detailed_scores)

    progress_percentage = 100.0

    return render(
        request,
        "survey/thank_you.html",
        {
            "survey": survey,
            "responses": responses,
            "total_score": total_score,
            "progress_percentage": progress_percentage,
        },
    )
