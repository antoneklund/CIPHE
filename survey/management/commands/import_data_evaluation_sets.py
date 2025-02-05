from django.core.management.base import BaseCommand
from survey.models import Survey, Cluster, Article
import pandas as pd


class Command(BaseCommand):
    help = "Import data from a file into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path", type=str, help="Path to the file containing data"
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        # Your logic to read data from the file and populate the database
        articles_df = pd.read_json(file_path)
        group_ids = articles_df.group.value_counts().index.to_list()
        for group_id in group_ids:
            survey = Survey(title="CIPHE Survey")
            survey.save()
            clusters_in_group = articles_df.evaluation_set_label[
                articles_df.group == group_id
            ].unique()
            print(clusters_in_group)
            for cluster_id in clusters_in_group:
                cluster = Cluster()
                cluster.survey = survey
                cluster.original_cluster = cluster_id
                cluster.save()
                articles_in_cluster = articles_df[
                    articles_df.evaluation_set_label == cluster_id
                ]
                for i, row in articles_in_cluster.iterrows():
                    article = Article()
                    article.cluster = cluster
                    article.title = row.title
                    article.body = row.text[0:1000]
                    article.save()

        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
