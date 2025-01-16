import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

DATA_PATHS = [
    "paper_files/uf_likert.json",
    "paper_files/ft_likert.json",
    "paper_files/tax_likert.json",
]

LIKERT_QUESTIONS = [
    "I can easily comprehend \nthe contents of the articles.",
    "It was easy to choose which \narticles to include and exclude.",
    "It was easy to name \nthe group.",
    "I am familiar with the \narea that I named.",
]

LIKERT_ORDER = ["comprehension", "simplicity", "naming", "knowledge"]

INSTRUCT_ORDER = ["UF", "FT", "TAX"]

df_all = pd.DataFrame()
for survey_id, path in enumerate(DATA_PATHS):
    df = pd.read_json(path)
    df.survey_id = survey_id
    df_all = pd.concat([df_all, df])

df_all = df_all.drop(columns=["page_id", "order", "user_id"])
print(df_all.survey_id.value_counts())

print(df_all)
df_all.to_csv("likert_data.csv")

for question_id, question_text in zip(LIKERT_ORDER, LIKERT_QUESTIONS):
    print_df = df_all[[question_id, "cluster_id", "survey_id"]]
    result = pd.DataFrame(
        index=["strongly_disagree", "disagree", "neutral", "agree", "strongly_agree"]
    )
    # for cluster_id in range(1,11):
    for survey_id, instruct_name in enumerate(INSTRUCT_ORDER):
        df_add = df_all[df_all.survey_id == survey_id]
        counts = df_add[question_id].value_counts()
        result[instruct_name] = result.index.map(counts.get).fillna(0).astype(int)
    # print(print_df)
    print(result)
    result = result.transpose()

    responses = ["strongly_disagree", "disagree", "neutral", "agree", "strongly_agree"]
    gradual_cmap = cm.get_cmap("PiYG", len(result.columns))
    ax = result.plot(kind="bar", stacked=True, cmap=gradual_cmap, figsize=(3, 4))
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
