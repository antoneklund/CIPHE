import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
import nltk
from utils.utils import get_top_word

nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))
DESCRPTIONS = []

file_path = "cluster_data_exp2.json"
df = pd.read_json(file_path)
print(df)

topics_file_path = "ciphe_topics_241027.csv"
topics_df = pd.read_csv(topics_file_path)

df["average_score"] = df["article_scores"].apply(
    lambda scores: sum(scores) / len(scores) if scores else 0
)

df["cluster_name"] = df["name_answers"].apply(get_top_word)

likert_scale_map = {
    "strongly_disagree": 0.0,
    "disagree": 0.25,
    "neutral": 0.5,
    "agree": 0.75,
    "strongly_agree": 1.0,
}

def map_likert_answers(likert_dict, characteristic):
    opinion = likert_dict[characteristic]
    return opinion

def convert_numerical(list_likert):
    numerical_list = [likert_scale_map[likert] for likert in list_likert]
    return numerical_list

df["opinion"] = df["likert_answers"].apply(map_likert_answers, args=["opinion"])
df["emotion"] = df["likert_answers"].apply(map_likert_answers, args=["emotion"])
df["interest"] = df["likert_answers"].apply(map_likert_answers, args=["interest"])
df["opinion_num"] = df["opinion"].apply(convert_numerical)
df["emotion_num"] = df["emotion"].apply(convert_numerical)
df["interest_num"] = df["interest"].apply(convert_numerical)


df["avg_opinion"] = df["opinion_num"].apply(
    lambda scores: sum(scores) / len(scores) if scores else 0
)
df["avg_emotion"] = df["emotion_num"].apply(
    lambda scores: sum(scores) / len(scores) if scores else 0
)
df["avg_interest"] = df["interest_num"].apply(
    lambda scores: sum(scores) / len(scores) if scores else 0
)

ranked_df = df.sort_values(by="avg_emotion", ascending=False).reset_index(drop=True)
ranked_df = ranked_df.drop(columns=["likert_answers", "article_answers", "article_scores"])
print(ranked_df)

plt.figure(figsize=(12, 8))
melted_df = ranked_df.melt(
    id_vars="cluster_name",
    value_vars=["avg_opinion", "avg_emotion", "avg_interest"],
    var_name="Metric",
    value_name="Value"
)

sns.barplot(
    data=melted_df,
    x="cluster_name",
    y="Value",
    hue="Metric"
)

plt.xlabel("Cluster Name")
plt.ylabel("Score")
plt.title("Characteristics Averages ranked by Engagement")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
