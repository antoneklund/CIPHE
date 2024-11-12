from django.core.management.base import BaseCommand
from survey.models import LikertScaleQuestion
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Command(BaseCommand):
    help = "Import data from a file into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path", type=str, help="Path to the file containing data"
        )

    def handle(self, *args, **kwargs):
        # Extracting all Likert responses along with their clusters
        likert_responses = LikertScaleQuestion.objects.select_related(
            "page__cluster"
        ).all()

        # Extracting responses and corresponding clusters for each Likert scale question
        responses_with_clusters = [
            (response.inclusion, response.page.cluster.id)
            for response in likert_responses
            if response.inclusion and response.page and response.page.cluster
        ]
        df = pd.DataFrame(responses_with_clusters, columns=["Response", "Cluster"])
        # Check if all clusters have responses
        valid_clusters = df["Cluster"].unique()
        clusters_with_responses = df.groupby("Cluster").size().index

        # Filter out clusters with no responses
        valid_responses = df[df["Cluster"].isin(clusters_with_responses)]
        # Creating a catplot with hue for clusters
        plt.figure(figsize=(10, 6))
        sns.catplot(
            data=valid_responses,
            x="Cluster",
            y="Response",
            kind="box",
            order=sorted(valid_clusters),
        )
        plt.title("Distribution of Likert Scale Responses by Cluster")
        plt.xlabel("Cluster")
        plt.ylabel("Response")
        plt.xticks(rotation=45)
        plt.show()
