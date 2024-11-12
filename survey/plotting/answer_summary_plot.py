import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import re
import seaborn as sns
from nltk.corpus import stopwords
import nltk

nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))
DESCRPTIONS = []

# Load the CSV file
file_path = "cluster_data.csv"
df = pd.read_csv(file_path)
print(df)

# Load the topics JSON file
topics_file_path = "ciphe_topics_241027.csv"
topics_df = pd.read_csv(topics_file_path)
print(topics_df)

# Calculate the average score for each cluster
df["article_scores"] = df["article_scores"].apply(eval)  # Convert to lists if necessary
df["average_score"] = df["article_scores"].apply(
    lambda scores: sum(scores) / len(scores) if scores else 0
)


# Define a function to get the top word in answers, avoiding stopwords
def get_top_word(answers):
    words = [
        word.lower()
        for word in " ".join(eval(answers)).split()
        if word.lower() not in STOPWORDS
    ]
    word_counts = Counter(words)
    if word_counts.most_common(1)[0][0] not in DESCRPTIONS:
        DESCRPTIONS.append(word_counts.most_common(1)[0][0])
        return word_counts.most_common(1)[0][0]
    else:
        return word_counts.most_common(1)[0][0] + "_2"


df["cluster_name"] = df["uf_answers"].apply(get_top_word)

# Likert scale mapping and functions to process likert answers
likert_scale_map = {
    "strongly_disagree": 0.0,
    "disagree": 0.25,
    "neutral": 0.5,
    "agree": 0.75,
    "strongly_agree": 1.0,
}


def clean_likert_string(likert_str):
    clean_str = re.sub(r"defaultdict\(<class 'list'>, ", "", likert_str)
    clean_str = clean_str.rstrip(")")
    return eval(clean_str)


def map_likert_answers(likert_dict_str):
    likert_dict = clean_likert_string(likert_dict_str)
    mapped_likert = {
        key: [likert_scale_map.get(answer.lower(), np.nan) for answer in answers]
        for key, answers in likert_dict.items()
    }
    return {
        key: np.nanmean(vals) if vals else np.nan for key, vals in mapped_likert.items()
    }


likert_averages = df["likert_answers"].apply(map_likert_answers).apply(pd.Series)

df = pd.concat([df, likert_averages], axis=1)

# Merge with topics_df on 'topic_id' and 'cluster_id'
merged_df = df.merge(topics_df, left_on=["cluster_id"], right_on=["topic_id"])

# Sort by topic_size
merged_df = merged_df.sort_values(by="topic_size")

# Plotting
plt.figure(figsize=(12, 8))
bar = sns.barplot(data=merged_df, x="cluster_name", y="average_score")
line = sns.lineplot(
    data=merged_df,
    x="cluster_name",
    y="opinion",
    color="gold",
    marker="v",
    markersize=10,
)
line2 = sns.lineplot(
    data=merged_df,
    x="cluster_name",
    y="emotion",
    color="red",
    marker="v",
    markersize=10,
)
line3 = sns.lineplot(
    data=merged_df,
    x="cluster_name",
    y="interest",
    color="green",
    marker="v",
    markersize=10,
)

# Labels and title
plt.xlabel("Cluster Name")
plt.ylabel("Score")
plt.title("Average Article Score per Cluster with Likert Scale Averages")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
