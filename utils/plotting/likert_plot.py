import pandas as pd
import plot_likert as pl
import matplotlib.pyplot as plt


def set_title_characteristic(characteristic, dataset):
    if characteristic=="emotion":
        title_characteristic = "Negative Emotion"
    elif characteristic=="interest":
        title_characteristic = "Engagement"
    elif characteristic=="opinion":
        if dataset=="news":
            title_characteristic="Impact"
        elif dataset=="wiki":
            title_characteristic="Societal Leadership"
        elif dataset=="yelp":
            title_characteristic="Mixed Sentiment"
    return title_characteristic

def structure_bold_labels_from_mannwithney(characteristic, dataset):
    df = pd.read_csv("mannwithney.csv")
    df_mw = df[(df["dataset"] == dataset) & (df["characteristic"]==characteristic)]
    rejections = df_mw.decision.to_list()
    rejections = [item for item in rejections for _ in range(2)]
    rejections.reverse()
    return rejections

dataset="yelp"
CIPHE_answers = pd.read_json(f"exp3_{dataset}_data.json")
keywords_answers = pd.read_json(f"exp1_{dataset}_data.json")
characteristics = ["emotion","opinion","interest"]

# (django_cluster_id, cluster_order, label_string)
news_pairs = [
    (23, 4, "UK Riots"),
    (26, 5, "Recipes"),
    (24, 1, "US Politics"),
    (22, 3, "Phones"),
    (28, 6, "Taylor Swift"),
    (25, 2, "Space"),
    (27, 7, "Unlabeled"),
]
yelp_pairs = [
    (8, 1, "Mexican Rest."),
    (9, 2, "Tours"),
    (10, 3, "Veterinarians"),
    (11, 4, "Markets"),
    (12, 5, "Hotels"),
    (13, 6, "Negative Rest."),
    (14, 7, "Unlabeled"),
]
wiki_pairs = [
    (1, 1, "Religious"),
    (2, 2, "Female Writers"),
    (3, 3, "Musicians"),
    (4, 4, "Swimmers"),
    (5, 5, "Navy Officers"),
    (6, 6, "Badminton"),
    (7, 7, "Unlabeled"),
]
pair_dict={
        "news": news_pairs,
        "yelp": yelp_pairs,
        "wiki": wiki_pairs
        }


pairs = pair_dict[dataset]

fig, axs=plt.subplots(1,3)
subplot_id=0
for characteristic in characteristics:
    C_df = pd.DataFrame()
    for idx, (i_c, i_i, name) in enumerate(pairs):
        c_df = CIPHE_answers["likert_answers"][CIPHE_answers.cluster_id == i_c]
        i_df = keywords_answers["likert_answers"][keywords_answers.cluster_id == i_i]
        if not c_df.empty and not i_df.empty:
            min_length = min(
                len(c_df.iloc[0][characteristic]), len(i_df.iloc[0][characteristic])
            )
            c_opinion = c_df.iloc[0][characteristic][:min_length]
            i_opinion = i_df.iloc[0][characteristic][:min_length]
            C_df[f"{name} - CIPHE"] = c_opinion
            C_df[f"{' '*idx}- KWM"] = i_opinion

    scale_options = ["strongly_disagree", "disagree", "neutral", "agree", "strongly_agree"]
    pl.plot_likert(
        C_df, scale_options, colors=pl.colors.likert5, width=0.8, figsize=(15,4), legend=0, ax=axs[subplot_id]
    )

    data = C_df
    questions = list(data.keys())
    for i in range(0, len(questions), 2):
        axs[subplot_id].axhspan(i -0.5, i + 1.5, color='lightgray', alpha=0.2)
        if i+2 <len(questions):
            axs[subplot_id].axhline(i +1.5, color='gray', linestyle='dashed', linewidth=0.7)

    rejections = structure_bold_labels_from_mannwithney(characteristic, dataset)
    ylabels = axs[subplot_id].get_yticklabels()
    bolder_zip = zip(ylabels, rejections)

    for label, decision in bolder_zip:
        print(label)
        if decision == "Reject":
            print(decision)
            label.set_fontweight('bold')
    axs[subplot_id].set_xlabel('') 
    axs[subplot_id].set_xticks([]) 
    axs[subplot_id].set_xticklabels([]) 
    plt.xticks([])
    plt.tight_layout()

    axs[subplot_id].set_title(set_title_characteristic(characteristic, dataset))
    if subplot_id>0:
        plt.ylabel(None)
    subplot_id+=1

plt.savefig(f"likert_{dataset}.pdf",  format="pdf", bbox_inches="tight")
plt.show()