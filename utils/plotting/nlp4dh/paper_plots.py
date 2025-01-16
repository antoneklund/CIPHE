import pandas as pd
import matplotlib.pyplot as plt

# Re-load the original data and clean it again based on prior instructions
data = pd.read_csv("ia_plot.csv")

# Dropping unnecessary columns and handling 'Unnamed' columns as instructed
data_cleaned = data.drop(columns=["Clusters", "Instruct", "Unnamed: 13", "Unnamed: 14"])
# data_cleaned["Unnamed: 12"] = data_cleaned["Unnamed: 12"] - 0.01
data_cleaned["ia"] = (
    data_cleaned["A_inc"]
    + data_cleaned["A_seg"]
    + data_cleaned["A_name"]
    + data_cleaned["L_inc"]
    + data_cleaned["L_name"]
) / 5
print(data_cleaned)

# Set 'Name' as index and convert numeric columns for stacking
data_cleaned.set_index("Name", inplace=True)
data_numeric = data_cleaned.apply(pd.to_numeric, errors="coerce")

# Filtering out NaN rows from the 'Name' column and removing unwanted columns
data_filtered = data_numeric.dropna(how="all")

# Renaming columns to remove "Unnamed" labels
column_mapping = {
    col: col if "Unnamed" not in col else "" for col in data_filtered.columns
}
data_filtered.rename(columns=column_mapping, inplace=True)

# Plotting the stacked bar plot again
fig, ax = plt.subplots(figsize=(10, 6))

# Plot with 'Unnamed' columns in white
data_filtered.plot(
    kind="bar",
    stacked=True,
    ax=ax,
    color=[
        "#ff00ff",
        "white",
        "#8e44ad",
        "white",
        "#46bdc6",
        "white",
        "#34a853",
        "white",
        "#ff6d01",
        "white",
        "black",
    ],
)

# Removing empty labels from the legend
handles, labels = ax.get_legend_handles_labels()
ax.legend(
    handles=[handle for handle, label in zip(handles, labels) if label != ""],
    labels=[label for label in labels if label != ""],
)


# Adding labels and title
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])

# Custom y-axis labels
custom_labels = ["A_inc", "A_seg", "A_name", "L_inc", "L_name", "IA"]
right_xlabels = ["0", "1/0", "1/0", "1/0", "1/0", "1/0"]
ax.set_yticklabels(custom_labels)
# ax_secondary = ax.secondary_yaxis('right')
# ax_secondary.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])  # Set tick positions
# ax_secondary.set_yticklabels(right_xlabels)
# plt.title("Stacked Bar Plot of Survey Results")
# plt.ylabel("Metric")
plt.xlabel(None)
# plt.legend(None)
ax.grid(True)
ax.grid(linestyle="--")
ax.get_legend().remove()
ax.set_ylim([0.0, 1.2])

# Display the plot
plt.tight_layout()
plt.show()
