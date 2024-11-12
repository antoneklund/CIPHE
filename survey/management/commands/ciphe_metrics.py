from django.core.management.base import BaseCommand
from survey.models import (
    LikertScaleQuestion,
    ArticleQuestion,
    UFQuestion,
    Article,
    Cluster,
)
import numpy as np
import pandas as pd
import ast
from collections import defaultdict
from survey.metrics.metrics import print_CIPHE_metrics

TOTAL_CLUSTERS = 10
SURVEY_ID = 1
HAS_ORIGINAL_LABEL = False


def calculate_model_score(article_responses):
    scores = []
    for response in article_responses:
        converted_response = ast.literal_eval(response.selected)
        scores.append(len(converted_response) / TOTAL_CLUSTERS)
    return np.mean(scores), scores


def convert_to_original_label(django_object_id, mapping):
    cluster = Cluster.objects.get(pk=django_object_id)
    django_eval_set_label = cluster.original_cluster
    original_label = mapping.label[
        mapping.evaluation_set_label == django_eval_set_label
    ].unique()[0]
    return original_label


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Modify to accept multiple user IDs
        parser.add_argument(
            "user_ids", nargs="+", type=int, help="List of User IDs to investigate"
        )

    def handle(self, *args, **kwargs):
        user_ids = kwargs["user_ids"]

        # Create dictionaries to store likert answers and UFQuestion answers for each cluster
        cluster_likert_answers = defaultdict(lambda: defaultdict(list))
        cluster_article_answers = defaultdict(lambda: defaultdict(list))
        cluster_article_scores = defaultdict(list)
        cluster_name_answers = defaultdict(list)

        mapping_oc_and_label = pd.read_json("original_label_link.json")

        # Iterate over each user
        for user_id in user_ids:
            name_answers = UFQuestion.objects.filter(page__user_id=user_id)
            article_answers = ArticleQuestion.objects.filter(page__user_id=user_id)
            likert_answers = LikertScaleQuestion.objects.filter(page__user_id=user_id)

            for likert in likert_answers:
                if HAS_ORIGINAL_LABEL:
                    cluster_id = convert_to_original_label(
                        likert.page.cluster.id, mapping_oc_and_label
                    )
                else:
                    cluster_id = likert.page.cluster.id
                cluster_likert_answers[cluster_id]["inclusion"].append(likert.inclusion)
                cluster_likert_answers[cluster_id]["naming"].append(likert.naming)
                cluster_likert_answers[cluster_id]["opinion"].append(likert.opinion)
                cluster_likert_answers[cluster_id]["emotion"].append(likert.emotion)
                cluster_likert_answers[cluster_id]["interest"].append(likert.interest)
                if hasattr(likert, "style"):
                    cluster_likert_answers[cluster_id]["style"].append(likert.style)

            for article in article_answers:
                cluster = Cluster.objects.get(page__id=article.page_id)
                article_ids = Article.objects.filter(cluster=cluster).values_list(
                    "id", flat=True
                )
                articles_ids_list = list(article_ids)
                if HAS_ORIGINAL_LABEL:
                    cluster_id = convert_to_original_label(
                        article.page.cluster.id, mapping_oc_and_label
                    )
                else:
                    cluster_id = article.page.cluster.id
                cluster_article_answers[cluster_id]["selected"].append(article.selected)
                cluster_article_answers[cluster_id]["all_articles"].append(
                    articles_ids_list
                )
                _, article_scores = calculate_model_score([article])
                cluster_article_scores[cluster_id].append(article_scores[0])

            for name in name_answers:
                if HAS_ORIGINAL_LABEL:
                    cluster_id = convert_to_original_label(
                        name.page.cluster.id, mapping_oc_and_label
                    )
                else:
                    cluster_id = name.page.cluster.id
                cluster_name_answers[cluster_id].append(name.text_answer)

        # Merging all data into a DataFrame
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

        # # Convert lists and dictionaries to strings for CSV compatibility
        # df["likert_answers"] = df["likert_answers"].apply(lambda x: str(x))
        # df["article_answers"] = df["article_answers"].apply(lambda x: str(x))
        # df["article_scores"] = df["article_scores"].apply(lambda x: str(x))
        # df["name_answers"] = df["name_answers"].apply(lambda x: str(x))

        # Save to json
        df.to_json("cluster_data.json", index=False)
        for i, cluster_row in df.iterrows():
            print_CIPHE_metrics(cluster_row)
