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
from nltk.metrics import agreement as agree

TOTAL_CLUSTERS = 10
SURVEY_ID = 1


def calculate_model_score(article_responses):
    scores = []
    for response in article_responses:
        converted_response = ast.literal_eval(response.selected)
        scores.append(len(converted_response) / TOTAL_CLUSTERS)
    return np.mean(scores), scores


def calculate_likert_standard_deviation(likert_answers):
    """Calculates the average score for a list of Likert scale answers (strings)."""
    values = []
    likert_scale_map = {
        "strongly_disagree": 0.0,
        "disagree": 0.25,
        "neutral": 0.5,
        "agree": 0.75,
        "strongly_agree": 1.0,
    }

    for answer in likert_answers:
        if answer:  # Check if there's an answer
            values.append(likert_scale_map.get(answer, 0))

    if values:
        return np.std(values)
    return None  # If there are no values to average


def calculate_likert_median(likert_answers):
    """Calculates the average score for a list of Likert scale answers (strings)."""
    values = []
    likert_scale_map = {
        "strongly_disagree": 0.0,
        "disagree": 0.25,
        "neutral": 0.5,
        "agree": 0.75,
        "strongly_agree": 1.0,
    }

    for answer in likert_answers:
        if answer:  # Check if there's an answer
            values.append(likert_scale_map.get(answer, 0))

    if values:
        return np.median(values)
    return None  # If there are no values to average


def calculate_likert_average(likert_answers):
    """Calculates the average score for a list of Likert scale answers (strings)."""
    values = []
    likert_scale_map = {
        "strongly_disagree": 0.0,
        "disagree": 0.25,
        "neutral": 0.5,
        "agree": 0.75,
        "strongly_agree": 1.0,
    }

    for answer in likert_answers:
        if answer:  # Check if there's an answer
            values.append(likert_scale_map.get(answer, 0))

    if values:
        return np.mean(values)
    return None  # If there are no values to average


def calculate_likert_frequency_table(likert_answers):
    """Calculate frequency table for the Likert scale answers."""
    result = {
        "strongly_disagree": 0,
        "disagree": 0,
        "neutral": 0,
        "agree": 0,
        "strongly_agree": 0,
    }
    for answer in likert_answers:
        if answer:
            result[answer] += 1
    return result


def calculate_agreement(article_answers, all_articles):
    # print(all_articles)
    # print(article_answers)

    responses = []
    segmentation_responses = []
    unique_segmentations = []
    segmentation_counts = {}  # Dictionary to store counts of unique segmentations

    for i, selected_articles in enumerate(
        article_answers["selected"]
    ):  # (articles, uf)
        # print(selected_articles)
        selected_processed = ast.literal_eval(selected_articles)
        selected_processed = [int(a) for a in selected_processed]
        selected_processed = convert_to_bool_list(selected_processed, all_articles)
        # print(selected_processed)

        for j, a in enumerate(selected_processed):
            responses.append(
                (str(i), str(j), a)
            )  # Tuple of (user_id, article_id, bool(response))

        if (
            selected_articles not in unique_segmentations
        ):  # Checking if segmentation is already in the list
            unique_segmentations.append(selected_articles)
            segmentation_counts[selected_articles] = 0

        segmentation_counts[selected_articles] += 1
        segmentation_responses.append((str(i), 0, selected_articles))

    agreement = agree.AnnotationTask(data=responses)
    segmentation_agree = agree.AnnotationTask(data=segmentation_responses)
    nr_unique = len(unique_segmentations)

    return agreement, segmentation_agree, nr_unique, segmentation_counts


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
        cluster_uf_answers = defaultdict(list)

        mapping_oc_and_label = pd.read_json("original_label_link.json")

        # Iterate over each user
        for user_id in user_ids:
            uf_answers = UFQuestion.objects.filter(page__user_id=user_id)
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
                cluster_article_answers[cluster_id]["selected"].append(article.selected)
                cluster_id = convert_to_original_label(
                    article.page.cluster.id, mapping_oc_and_label
                )
                _, article_scores = calculate_model_score([article])
                cluster_article_scores[cluster_id].append(article_scores[0])

            for uf in uf_answers:
                cluster_id = convert_to_original_label(
                    uf.page.cluster.id, mapping_oc_and_label
                )
                cluster_uf_answers[cluster_id].append(uf.text_answer)

        print("----------------------------------------------------------------\n")
        print("\nAverage Scores and UF Answers for Each Cluster:")
        for cluster_id, likert_answers in cluster_likert_answers.items():
            print(f"\nCluster ID: {cluster_id}")
            print(f"UF Answers for Cluster {cluster_id}:")
            for uf_answer in cluster_uf_answers[cluster_id]:
                print(f" - {uf_answer}")

            # Calculate the average for each Likert field
            likert_avg_inclusion = calculate_likert_average(likert_answers["inclusion"])
            likert_avg_naming = calculate_likert_average(likert_answers["naming"])
            likert_avg_opinion = calculate_likert_average(likert_answers["opinion"])
            likert_avg_emotion = calculate_likert_average(likert_answers["emotion"])
            likert_avg_interest = calculate_likert_average(likert_answers["interest"])
            likert_avg_style = calculate_likert_average(likert_answers["style"])

            likert_std_opinion = calculate_likert_standard_deviation(
                likert_answers["opinion"]
            )
            likert_std_emotion = calculate_likert_standard_deviation(
                likert_answers["emotion"]
            )
            likert_std_interest = calculate_likert_standard_deviation(
                likert_answers["interest"]
            )

            likert_median_opinion = calculate_likert_median(likert_answers["opinion"])
            likert_median_emotion = calculate_likert_median(likert_answers["emotion"])
            likert_median_interest = calculate_likert_median(likert_answers["interest"])

            frequency_table_opinion = calculate_likert_frequency_table(
                likert_answers["opinion"]
            )
            frequency_table_emotion = calculate_likert_frequency_table(
                likert_answers["emotion"]
            )
            frequency_table_interest = calculate_likert_frequency_table(
                likert_answers["interest"]
            )

            # Calculate average Article score for this cluster
            overall_article_avg = (
                np.mean(cluster_article_scores[cluster_id])
                if cluster_article_scores[cluster_id]
                else 0
            )

            # Calculate agreement for CIPHE metrics
            articles_ids = Article.objects.filter(
                cluster__survey_id=SURVEY_ID
            ).values_list("id", flat=True)
            articles_ids_list = list(articles_ids)
            agreement, segmentation_agree, nr_unique, segmentation_counts = (
                calculate_agreement(
                    cluster_article_answers[cluster_id], articles_ids_list
                )
            )
            n_participants = len(user_ids)
            # Print averages for this cluster
            print(f"Average Article Score: {1 - overall_article_avg}")
            print(f"Inclusion agreement: {agreement.avg_Ao()}")
            # print(f"Segmentation agreement: {segmentation_agree.avg_Ao()}")
            print(f"Unique segmentations: {nr_unique}")
            print(
                f"Largest segmentation: {max(segmentation_counts.values())/n_participants}"
            )
            print(f"Segmentation agreement: {1-((nr_unique - 1) / (n_participants-1))}")
            print(f"Likert Inclusion: {likert_avg_inclusion}")
            print(f"Likert Naming: {likert_avg_naming}")
            print(
                f"Likert Opinion: avg:{likert_avg_opinion} std:{likert_std_opinion} median:{likert_median_opinion}"
            )
            print(f"Likert Opinion Frequency Table: {frequency_table_opinion}")
            print(
                f"Likert Emotion: avg:{likert_avg_emotion} std:{likert_std_emotion} median:{likert_median_emotion}"
            )
            print(f"Likert Emotion Frequency Table: {frequency_table_emotion}")
            print(
                f"Likert Engagement: avg:{likert_avg_interest} std:{likert_std_interest} median:{likert_median_interest}"
            )
            print(f"Likert Interest Frequency Table: {frequency_table_interest}")
            print(f"Likert Simplicity: {likert_avg_style}")

            # Merging all data into a DataFrame
            data = []
            all_cluster_ids = (
                set(cluster_likert_answers.keys())
                | set(cluster_article_answers.keys())
                | set(cluster_article_scores.keys())
                | set(cluster_uf_answers.keys())
            )

            for cluster_id in all_cluster_ids:
                row = {
                    "cluster_id": cluster_id,
                    "likert_answers": cluster_likert_answers.get(cluster_id, {}),
                    "article_answers": cluster_article_answers.get(cluster_id, {}),
                    "article_scores": cluster_article_scores.get(cluster_id, []),
                    "uf_answers": cluster_uf_answers.get(cluster_id, []),
                }
                data.append(row)

            df = pd.DataFrame(data)

            # # Convert lists and dictionaries to strings for CSV compatibility
            # df["likert_answers"] = df["likert_answers"].apply(lambda x: str(x))
            # df["article_answers"] = df["article_answers"].apply(lambda x: str(x))
            # df["article_scores"] = df["article_scores"].apply(lambda x: str(x))
            # df["uf_answers"] = df["uf_answers"].apply(lambda x: str(x))

            # Save to json
            df.to_json("cluster_data.json", index=False)
