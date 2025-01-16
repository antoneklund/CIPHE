import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.utils import get_top_word


def add_vlines_at_medians(grouped_sorted):
    for i, row in grouped_sorted.iterrows():
        print(row)
        plt.vlines(x=i, ymin=0, ymax=row["median"], color='grey', linestyle='--', linewidth=1)

def plot_bar_plot(json_path):
    full_df = pd.read_json(json_path)
    name_answers = full_df["name_answers"].to_list()
    top_keywords = [get_top_word(n) for n in name_answers]
    # print(top_keywords)
    full_df["description"] = top_keywords
    df_expanded = full_df.explode('article_scores')
    df_expanded['article_scores'] = pd.to_numeric(df_expanded['article_scores'])
    df_expanded["CP"] = 1 - df_expanded["article_scores"]
    grouped = df_expanded.groupby('description')['CP'].agg(['median', 'mean'])
    grouped_sorted = grouped.sort_values(by=['median', 'mean'], ascending=[False, False])
    sorted_descriptions = grouped_sorted.index
    df_expanded["description"] = pd.Categorical(df_expanded["description"], categories=sorted_descriptions, ordered=True)

    alternate_colors = ['#d8a539' if i % 2 == 0 else '#5ab4ac' for i in range(len(sorted_descriptions))]
    flierprops = dict(marker='x', color='black', alpha=0.5)
    medianprops = dict(color='blue', linewidth=3)
    
    plt.figure(figsize=(12, 5))
    sns.boxplot(x='description', y='CP', data=df_expanded, palette=alternate_colors, flierprops=flierprops, medianprops=medianprops)
    add_vlines_at_medians(grouped_sorted)
    plt.ylim(bottom=-0.01)
    plt.xlabel("cluster_id")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("CP")
    plt.xlabel(None)
    plt.savefig("boxplot_exp2.pdf",  format="pdf", bbox_inches="tight")
    plt.show()