from django.core.management.base import BaseCommand
from survey.models import Cluster, Article, ArticleQuestion, UFQuestion
import numpy as np
import ast
from nltk.metrics import agreement as agree
from nltk.metrics import binary_distance

TOTAL_CLUSTERS = 7
CLUSTERS_SIZE = 10


def calculate_model_score(article_responses, uf_responses):
    scores = []

    responses = zip(article_responses, uf_responses)
    for response, uf in responses:
        if uf.uf_choices == "none":
            converted_response = []
        else:
            converted_response = ast.literal_eval(response.selected)
        scores.append(len(converted_response) / CLUSTERS_SIZE)
    return np.mean(scores), scores


def convert_to_bool_list(selected, all_articles):
    selected_processed = []
    for a in all_articles:
        if a in selected:
            selected_processed.append(True)
        else:
            selected_processed.append(False)
    return selected_processed


def calculate_agreement(article_answers, uf_answers, cluster_id):
    all_articles = Article.objects.filter(cluster_id=cluster_id)
    all_articles = [str(article.id) for article in all_articles]

    zipped_responses = zip(article_answers, uf_answers)

    responses = []
    segmentation_responses = []
    unique_segmentations = []
    segmentation_counts = {}  # Dictionary to store counts of unique segmentations

    for i, (answer, uf) in enumerate(zipped_responses):
        selected = answer.selected
        selected_processed = ast.literal_eval(selected)

        if uf.uf_choices == "none":
            selected_processed = [False] * 10
            print(f"uf_id: {uf.id}")
        else:
            selected_processed = convert_to_bool_list(selected_processed, all_articles)

        for j, a in enumerate(selected_processed):
            responses.append((str(i), str(j), a))

        if (
            selected not in unique_segmentations
        ):  # Checking if segmentation is already in the list
            unique_segmentations.append(selected)
            segmentation_counts[selected] = 0

        segmentation_counts[selected] += 1  # Incrementing count for the segmentation

        segmentation_responses.append((str(i), 0, selected))

    agreement = agree.AnnotationTask(data=responses, distance=binary_distance)
    segmentation_agree = agree.AnnotationTask(data=segmentation_responses)
    nr_unique = len(unique_segmentations)

    return agreement, segmentation_agree, nr_unique, segmentation_counts


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("user_id", type=str, help="Users to investigate [1,2,...]")

    def handle(self, *args, **kwargs):
        user_id = [int(x) for x in ast.literal_eval(kwargs["user_id"])]
        print(user_id)
        # prolific_id = User.objects.get(pk=user_id).prolific_identity

        # article_answers = ArticleQuestion.objects.filter(page__user_id=user_id)
        # likert_answers = LikertScaleQuestion.objects.filter(page__user_id=user_id)

        clusters = Cluster.objects.filter(survey_id=1)
        for cluster in clusters:
            naming_answers = UFQuestion.objects.filter(
                page__cluster_id=cluster.id, page__user_id__in=user_id
            )
            article_answers = ArticleQuestion.objects.filter(
                page__cluster_id=cluster.id, page__user_id__in=user_id
            )
            responses = zip(naming_answers, article_answers)
            agreement, segmentation_agree, nr_unique, segmentation_counts = (
                calculate_agreement(article_answers, naming_answers, cluster.id)
            )
            total_score, _ = calculate_model_score(article_answers, naming_answers)
            print(f"Nr answers: {len(naming_answers)}")
            print(f"Cluster {cluster.id}")
            print(f"Score: {total_score}")
            print(f"Average observed agreement: {agreement.avg_Ao()}")
            print(f"Krippendorfs alpha: {agreement.alpha()}")
            print(f"Segmentation agreement: {segmentation_agree.avg_Ao()}")
            print(f"Unique segmentations: {nr_unique}")
            print(
                f"Largest segmentation: {max(segmentation_counts.values())/len(naming_answers)}"
            )
            print(
                f"Unique Segmentation score: {1-(nr_unique/len(naming_answers)) + (1/len(naming_answers))}"
            )

            for uf, a in responses:
                print(f"Name: {uf.text_answer}, id: {uf.id}")
                print(f"Articles: {a.selected}, id: {a.id}")
            print("\n\n")
