import pandas as pd
import matplotlib.pyplot as plt


df1 = pd.read_csv("ft.csv")
df2 = pd.read_csv("uf.csv")
df3 = pd.read_csv("tax.csv")
df1 = df1.drop(columns=["alpha", "Clusters"])
df2 = df2.drop(columns=["alpha", "Clusters"])
df3 = df3.drop(columns=["alpha", "Clusters"])


# Set the Name column as index
df1.set_index("Name", inplace=True)
df2.set_index("Name", inplace=True)
df3.set_index("Name", inplace=True)

# # Stack the values for each column
# stacked_df = pd.concat([df1, df2, df3], keys=['FT', 'UF', 'TAX'])
instructions = ["FT", "UF", "TAX"]

unique_names = df1.index.to_list()
stacked_df = pd.DataFrame()
for name in unique_names:
    # for instruct in instructions:
    stacked_df = pd.concat([stacked_df, df1[df1.index == name]])
    stacked_df = pd.concat([stacked_df, df2[df2.index == name]])
    stacked_df = pd.concat([stacked_df, df3[df3.index == name]])

# # Plot the stacked bar chart
stacked_df.plot(kind="bar", stacked=True, figsize=(12, 8))
plt.title("Stacked Bar Chart of CSV Data")
plt.xlabel("Name")
plt.ylabel("Values")
plt.legend(title="CSV Files")
plt.show()
