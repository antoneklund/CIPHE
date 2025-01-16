import pandas as pd


df1 = pd.read_csv("ft.csv")
df2 = pd.read_csv("uf.csv")
df3 = pd.read_csv("tax.csv")
df1 = df1.drop(columns=["alpha", "Clusters"])
df2 = df2.drop(columns=["alpha", "Clusters"])
df3 = df3.drop(columns=["alpha", "Clusters"])


# # Set the Name column as index
# df1.set_index('Name', inplace=True)
# df2.set_index('Name', inplace=True)
# df3.set_index('Name', inplace=True)

# # Stack the values for each column
# stacked_df = pd.concat([df1, df2, df3], keys=['FT', 'UF', 'TAX'])
instructions = ["FT", "UF", "TAX"]

df1["Instruct"] = "FT"
df2["Instruct"] = "UF"
df3["Instruct"] = "TAX"

df_all = pd.concat([df1, df2, df3])
df_all = df_all.groupby("Name")
print(df_all)
