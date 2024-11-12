import sqlite3
import pandas as pd

db_path = "/home/anton/code/UF-Survey-Platform/old_databases/240221/db_240221.sqlite3"
query = (
    "select * from survey_ufquestion inner join survey_page on page_id = survey_page.id"
)
save_path = "paper_files/uf_uf.json"

# TAX = [4, 5, 6, 8, 9, 12, 13, 14, 15, 16, 19, 20, 21, 22, 24, 26, 27, 28, 37, 38]
# EXTRA_TAX = [45, 46]
# UF = [11,13,14,15,16,17,18,19,20,21,22,25,26,28,29,30,33,35,36,37]
conn = sqlite3.connect(db_path)

df = pd.read_sql(query, conn)

df = df[
    df.user_id.isin(
        [11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 25, 26, 28, 29, 30, 33, 35, 36, 37]
    )
]

df = df.drop(columns=["id"])
# df = df.drop(index=256)
print(df)

df.to_json(save_path)
