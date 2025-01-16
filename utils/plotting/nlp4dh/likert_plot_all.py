import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

DATA_PATHS = [
    "paper_files/uf_likert.json",
    "paper_files/ft_likert.json",
    "paper_files/tax_likert.json",
]
# APPROVED_IDS = [[11,13,14,15,16,17,18,19,20,21,22,24,25,26,28,29,30,33,35,36,37],
#                 [3,4,6,8,9,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,31],
#                 [4, 5, 6, 8, 9, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 24, 26, 27, 28, 29]
#                 ]

LIKERT_QUESTIONS = [
    "I can easily comprehend the contents of the articles.",
    "It was easy to choose which articles to include and exclude.",
    "It was easy to name the group.",
    "I am familiar with the area that I named.",
]

LIKERT_ORDER = ["comprehension", "simplicity", "naming", "knowledge"]

df_all = pd.DataFrame()
for survey_id, path in enumerate(DATA_PATHS):
    df = pd.read_json(path)
    df.survey_id = survey_id
    # df = df[df["user_id"].isin(approved)]
    df_all = pd.concat([df_all, df])

df_all = df_all.drop(columns=["page_id", "order", "user_id"])
print(df_all.survey_id.value_counts())

print(df_all)

for question_id, question_text in zip(LIKERT_ORDER, LIKERT_QUESTIONS):
    print_df = df_all[[question_id, "cluster_id", "survey_id"]]
    result = pd.DataFrame(
        index=["strongly_disagree", "disagree", "neutral", "agree", "strongly_agree"]
    )
    for cluster_id in range(1, 11):
        for survey_id in range(0, 3):
            df_add = df_all[
                (df_all.survey_id == survey_id) & (df_all.cluster_id == cluster_id)
            ]
            counts = df_add[question_id].value_counts()
            result[str(cluster_id) + "_" + str(survey_id)] = (
                result.index.map(counts.get).fillna(0).astype(int)
            )
    # print(print_df)
    print(result)
    result = result.transpose()

    responses = ["strongly_disagree", "disagree", "neutral", "agree", "strongly_agree"]
    gradual_cmap = cm.get_cmap("PiYG", len(result.columns))
    ax = result.plot(kind="bar", stacked=True, cmap=gradual_cmap, figsize=(12, 2.5))
    ax.legend(
        loc="upper right",
        bbox_to_anchor=(0.9, -0.2),
        ncol=len(result.columns),
        fancybox=True,
        shadow=True,
    )
    plt.title(question_text)
    # plt.savefig(f"/home/anton/Pictures/likert_combined/{question_id}.png", bbox_inches='tight')
    plt.show()


for question_id, question_text in zip(LIKERT_ORDER, LIKERT_QUESTIONS):
    df = pd.read_json("data/likert_uf3.json")
    # cluster_id_to_plot = i
    # df = df[df["cluster_id"] == cluster_id_to_plot]
    df = df[
        df["user_id"].isin(
            [4, 5, 6, 8, 9, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 24, 26, 27, 28, 29]
        )
    ]
    df = df.drop(
        columns=["page_id", "order", "survey_id", "id", "user_id", "cluster_id"]
    )

    result = pd.DataFrame(
        index=["strongly_disagree", "disagree", "neutral", "agree", "strongly_agree"]
    )

    # Define response categories
    for column in df.columns:
        counts = df[column].value_counts()
        result[column] = result.index.map(counts.get).fillna(0).astype(int)

    responses = ["strongly_disagree", "disagree", "neutral", "agree", "strongly_agree"]
    # result = result.transpose()
    # print(result)

    gradual_cmap = cm.get_cmap("PiYG", len(result.columns))
    ax = result.plot(kind="barh", stacked=True, cmap=gradual_cmap, figsize=(10, 6))
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.05),
        ncol=len(result.columns),
        fancybox=True,
        shadow=True,
    )
    # plt.title(f"Likert scale Cluster {cluster_id_to_plot}")
    plt.xticks([])
    # plt.savefig(f"/home/anton/Pictures/tax_likert/cluster_{cluster_id_to_plot}.png")
    # plt.show()
