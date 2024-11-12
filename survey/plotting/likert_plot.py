import pandas as pd
import plot_likert as pl
from collections import defaultdict
import matplotlib.pyplot as plt
import ast
import re


def convert_to_defaultdict(string):
    print(string)
    cleaned_string = re.sub(r"^defaultdict\(.*?, ", "", string)[:-1]
    print(cleaned_string)
    # Convert the string to a dictionary
    normal_dict = ast.literal_eval(cleaned_string)
    print(type(normal_dict))
    # Convert the dictionary to a defaultdict
    return defaultdict(list, normal_dict)


another_scale = ["strongly_disagree", "disagree", "neutral", "agree", "strongly_agree"]
CIPHE_answers = pd.read_json("cluster_data_exp1_ciphe.json")
print(CIPHE_answers)
intrusion_answers = pd.read_json("cluster_data_exp1_intrusion.json")
print(intrusion_answers)

pairs = [(23, 4), (26, 5), (24, 1), (22, 3), (28, 6), (25, 2), (27, 7)]


C_df = pd.DataFrame()
for i_c, i_i in pairs:
    c_df = CIPHE_answers["likert_answers"][CIPHE_answers.cluster_id == i_c]
    i_df = intrusion_answers["likert_answers"][intrusion_answers.cluster_id == i_i]
    print(c_df.iloc[0])
    print(i_df)
    for column in ["opinion", "emotion", "interest"]:  # "inclusion", "naming",
        print(column)
        C_df[f"CIPHE_{column}"] = c_df.iloc[0][column]
        C_df[f"intrusion_{column}"] = i_df.iloc[0][column][0:-1]

    print(C_df)
    pl.plot_likert(C_df, another_scale, colors=pl.colors.likert5, figsize=(6, 5))
    plt.title(f"{i_i}")
    plt.yticks(rotation=65)
    plt.savefig(f"likert_figure_{i_i}.png")
    plt.show()
