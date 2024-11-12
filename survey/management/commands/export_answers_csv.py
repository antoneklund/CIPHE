import csv
from django.core.management.base import BaseCommand
from django.db.models import Prefetch
from survey.models import User, Page


class Command(BaseCommand):
    help = "Export survey answers as a CSV for specific users"

    def add_arguments(self, parser):
        # Add an argument to pass a list of user IDs
        parser.add_argument(
            "--user-ids", nargs="+", type=int, help="List of User IDs to export"
        )

    def handle(self, *args, **kwargs):
        # Retrieve the user IDs passed as arguments
        user_ids = kwargs["user_ids"]

        if not user_ids:
            self.stdout.write(
                self.style.ERROR("Please provide at least one user ID using --user-ids")
            )
            return

        # Define the file path to save the CSV
        file_path = "survey_answers_filtered.csv"

        # Open a CSV file for writing
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)

            # Write header row
            header = [
                "User ID",
                "Prolific Identity",
                "Current Cluster Index",
                "Cluster Order",  #'Article IDs',
                "UFQuestion Answer",
                "LikertScale Inclusion",
                "LikertScale Naming",
                "LikertScale Opinion",
                "LikertScale Emotion",
                "LikertScale Interest",
                "LikertScale Style",
                "Article Question Selected",
            ]
            writer.writerow(header)

            # Query the users by the given user IDs and prefetch related pages and questions
            users = User.objects.filter(id__in=user_ids).prefetch_related(
                Prefetch(
                    "page_set",
                    queryset=Page.objects.prefetch_related(
                        "ufquestion_set",
                        "likertscalequestion_set",
                        "articlequestion_set",
                    ),
                )
            )

            # Iterate over each user
            for user in users:
                # Iterate over each page related to the user
                for page in user.page_set.all():
                    # Extract UFQuestion answers
                    uf_question_answers = (
                        ", ".join(
                            [ufq.text_answer for ufq in page.ufquestion_set.all()]
                        )
                        or "N/A"
                    )

                    # Extract LikertScaleQuestion answers
                    likert_question = page.likertscalequestion_set.first()

                    # Check if LikertScaleQuestion exists
                    if likert_question:
                        likert_answers = [
                            likert_question.inclusion or "N/A",
                            likert_question.naming or "N/A",
                            likert_question.opinion or "N/A",
                            likert_question.emotion or "N/A",
                            likert_question.interest or "N/A",
                            likert_question.style or "N/A",
                        ]
                    else:
                        # If no LikertScaleQuestion, fill with 'N/A'
                        likert_answers = ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]

                    # Extract ArticleQuestion answers
                    article_question_selected = (
                        ", ".join(
                            [aq.selected for aq in page.articlequestion_set.all()]
                        )
                        or "N/A"
                    )

                    # Write a row for each user and their associated survey data
                    writer.writerow(
                        [
                            user.id,
                            user.prolific_identity,
                            user.current_cluster_index,
                            user.cluster_order,
                            # user.article_ids,
                            uf_question_answers,
                            *likert_answers,
                            article_question_selected,
                        ]
                    )

        self.stdout.write(
            self.style.SUCCESS(f"Survey answers exported successfully to {file_path}")
        )
