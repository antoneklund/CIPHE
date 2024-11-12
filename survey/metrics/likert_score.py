import pandas as pd

TOTAL_CLUSTERS = 10
CLUSTER_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

ALL_ARTICLE_IDS = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    ["11", "12", "13", "14", "15", "16", "17", "18", "19", "20"],
    ["21", "22", "23", "24", "25", "26", "27", "28", "29", "30"],
    ["31", "32", "33", "34", "35", "36", "37", "38", "39", "40"],
    ["41", "42", "43", "44", "45", "46", "47", "48", "49", "50"],
    ["51", "52", "53", "54", "55", "56", "57", "58", "59", "60"],
    ["61", "62", "63", "64", "65", "66", "67", "68", "69", "70"],
    ["71", "72", "73", "74", "75", "76", "77", "78", "79", "80"],
    ["81", "82", "83", "84", "85", "86", "87", "88", "89", "90"],
    ["91", "92", "93", "94", "95", "96", "97", "98", "99", "100"],
]

for i in CLUSTER_IDS:
    df = pd.read_json("paper_files/tax_likert.json")
    df = df[df["cluster_id"] == i]
    # df = df[df["user_id"].isin([4, 5, 6, 8, 9, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 24, 26, 27, 28, 29])]
    # df = df.drop(columns=["page_id", "order", "survey_id", "id", "user_id", "cluster_id"])

    result = pd.DataFrame(
        index=["strongly_disagree", "disagree", "neutral", "agree", "strongly_agree"]
    )

    # Define response categories
    for column in df.columns:
        counts = df[column].value_counts()
        result[column] = result.index.map(counts.get).fillna(0).astype(int)

    scale = {
        "strongly_disagree": 0,
        "disagree": 0.25,
        "neutral": 0.5,
        "agree": 0.75,
        "strongly_agree": 1,
    }
    math_df = df.copy()
    math_df["inclusion"] = math_df.inclusion.map(scale)
    math_df["naming"] = math_df.naming.map(scale)
    math_df["opinion"] = math_df.opinion.map(scale)
    math_df["emotion"] = math_df.emotion.map(scale)
    math_df["interest"] = math_df.interest.map(scale)
    math_df["style"] = math_df.style.map(scale)

    print(f"Cluster: {i}")
    print(f"inclusion: {math_df.inclusion.mean()}")
    print(f"naming: {math_df.naming.mean()}")
    print(f"opinion: {math_df.opinion.mean()}")
    print(f"emotion: {math_df.emotion.mean()}")
    print(f"interest: {math_df.interest.mean()}")
    print(f"style: {math_df.style.mean()}")
