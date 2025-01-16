from django.core.management.base import BaseCommand
from survey.models import (
    LikertScaleQuestion,
    ArticleQuestion,
    NameQuestion,
    Cluster,
)
import numpy as np
import pandas as pd
import ast
from collections import defaultdict
from utils.metrics.metrics import print_CIPHE_metrics

SAMPLE_SIZE = 10
HAS_ORIGINAL_LABEL = False


def calculate_model_score(article_responses):
    scores = []
    for response in article_responses:
        converted_response = ast.literal_eval(response.selected)
        scores.append(len(converted_response) / SAMPLE_SIZE)
    return np.mean(scores), scores


def convert_to_bool_list(selected, all_articles):
    selected_processed = []
    for a in all_articles:
        if a in selected:
            selected_processed.append(False)
        else:
            selected_processed.append(True)
    return selected_processed


def convert_to_original_label(django_object_id, mapping):
    cluster = Cluster.objects.get(pk=django_object_id)
    if HAS_ORIGINAL_LABEL:
        django_eval_set_label = cluster.original_cluster
        original_label = mapping.label[
            mapping.evaluation_set_label == django_eval_set_label
        ].unique()[0]
        return original_label
    else:
        return cluster.id


def get_all_articles(cluster_id):
    """Note: If the import_data command has been used to add articles
    to the survey, the cluster_id from the db is enough for
    identifying all articles for that survey.
    """
    all_articles = [i for i in range((cluster_id - 1) * 10 + 1, cluster_id * 10 + 1)]
    return all_articles


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "user_ids", nargs="+", type=int, help="List of User IDs to investigate"
        )

    def handle(self, *args, **kwargs):
        user_ids = kwargs["user_ids"]

        cluster_likert_answers = defaultdict(lambda: defaultdict(list))
        cluster_article_answers = defaultdict(lambda: defaultdict(list))
        cluster_article_scores = defaultdict(list)
        cluster_name_answers = defaultdict(list)

        mapping_oc_and_label = pd.read_json("original_label_link.json")

        for user_id in user_ids:
            name_answers = NameQuestion.objects.filter(page__user_id=user_id)
            article_answers = ArticleQuestion.objects.filter(page__user_id=user_id)
            likert_answers = LikertScaleQuestion.objects.filter(page__user_id=user_id)

            for likert in likert_answers:
                cluster_id = convert_to_original_label(
                    likert.page.cluster.id, mapping_oc_and_label
                )
                cluster_likert_answers[cluster_id]["inclusion"].append(likert.inclusion)
                cluster_likert_answers[cluster_id]["naming"].append(likert.naming)
                cluster_likert_answers[cluster_id]["opinion"].append(likert.opinion)
                cluster_likert_answers[cluster_id]["emotion"].append(likert.emotion)
                cluster_likert_answers[cluster_id]["interest"].append(likert.interest)
                cluster_likert_answers[cluster_id]["style"].append(likert.style)

            for article in article_answers:
                cluster_id = convert_to_original_label(
                    article.page.cluster.id, mapping_oc_and_label
                )
                all_articles = get_all_articles(cluster_id)
                cluster_article_answers[cluster_id]["selected"].append(article.selected)
                cluster_article_answers[cluster_id]["all_articles"].append(all_articles)
                _, article_scores = calculate_model_score([article])
                cluster_article_scores[cluster_id].append(article_scores[0])

            for name in name_answers:
                cluster_id = convert_to_original_label(
                    name.page.cluster.id, mapping_oc_and_label
                )
                cluster_name_answers[cluster_id].append(name.text_answer)

        data = []
        all_cluster_ids = (
            set(cluster_likert_answers.keys())
            | set(cluster_article_answers.keys())
            | set(cluster_article_scores.keys())
            | set(cluster_name_answers.keys())
        )

        for cluster_id in all_cluster_ids:
            row = {
                "cluster_id": cluster_id,
                "likert_answers": cluster_likert_answers.get(cluster_id, {}),
                "article_answers": cluster_article_answers.get(cluster_id, {}),
                "article_scores": cluster_article_scores.get(cluster_id, []),
                "name_answers": cluster_name_answers.get(cluster_id, []),
            }
            data.append(row)

        df = pd.DataFrame(data)

        for _, cluster in df.iterrows():
            print_CIPHE_metrics(cluster)
