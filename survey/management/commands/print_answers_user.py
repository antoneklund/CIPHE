from django.core.management.base import BaseCommand
from survey.models import User, LikertScaleQuestion, NameQuestion, ArticleQuestion
import ast
from collections import defaultdict

CLUSTER_SIZE = 10


class Command(BaseCommand):
    help = "Prints the answers for a specific user across all clusters"

    def add_arguments(self, parser):
        parser.add_argument("user_id", type=int, help="User ID to print answers for")

    def handle(self, *args, **kwargs):
        user_id = kwargs["user_id"]

        # Retrieve the user object
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"User with ID {user_id} does not exist.")
            )
            return

        # Create dictionaries to store answers for each cluster
        cluster_likert_answers = defaultdict(lambda: defaultdict(list))
        cluster_name_answers = defaultdict(list)
        cluster_article_answers = defaultdict(list)

        # Get the answers from NameQuestion and LikertScaleQuestion
        name_answers = NameQuestion.objects.filter(page__user_id=user_id)
        likert_answers = LikertScaleQuestion.objects.filter(page__user_id=user_id)
        article_answers = ArticleQuestion.objects.filter(page__user_id=user_id)
        # Group LikertScaleQuestions by clusters
        for likert in likert_answers:
            cluster_id = likert.page.cluster.id
            cluster_likert_answers[cluster_id]["inclusion"].append(likert.inclusion)
            cluster_likert_answers[cluster_id]["naming"].append(likert.naming)
            cluster_likert_answers[cluster_id]["opinion"].append(likert.opinion)
            cluster_likert_answers[cluster_id]["emotion"].append(likert.emotion)
            cluster_likert_answers[cluster_id]["interest"].append(likert.interest)
            cluster_likert_answers[cluster_id]["style"].append(likert.style)

        # Group NameQuestion answers by clusters
        for name in name_answers:
            cluster_id = name.page.cluster.id
            cluster_name_answers[cluster_id].append(name.text_answer)

        for article_answer in article_answers:
            cluster_id = article_answer.page.cluster.id
            converted_response = ast.literal_eval(article_answer.selected)
            cluster_article_answers[cluster_id] = 1.0 - (
                len(converted_response) / CLUSTER_SIZE
            )

        # Print answers for each cluster
        self.stdout.write(
            "----------------------------------------------------------------\n"
        )
        self.stdout.write(f"Answers for User: {user.prolific_identity} (ID: {user_id})")
        self.stdout.write(
            "----------------------------------------------------------------\n"
        )

        for cluster_id in cluster_likert_answers.keys() | cluster_name_answers.keys():
            self.stdout.write(f"\nCluster ID: {cluster_id}")
            print(f"Article Score: {cluster_article_answers[cluster_id]}")
            # Print Likert answers
            self.stdout.write("LikertScaleQuestion Answers:")
            likert_fields = [
                "inclusion",
                "naming",
                "opinion",
                "emotion",
                "interest",
                "style",
            ]
            for field in likert_fields:
                answers = cluster_likert_answers[cluster_id][field]
                if answers:
                    self.stdout.write(f" - {field.capitalize()}: {', '.join(answers)}")
                else:
                    self.stdout.write(f" - {field.capitalize()}: No answer")

            # Print name answers
            self.stdout.write("NameQuestion Answers:")
            if cluster_name_answers[cluster_id]:
                for answer in cluster_name_answers[cluster_id]:
                    self.stdout.write(f' - "{answer}"')
            else:
                self.stdout.write(" - No Name answers")

        self.stdout.write(
            "----------------------------------------------------------------"
        )
