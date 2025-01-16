import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data_news = {"CP": [0.9363636364,
                    0.9590909091,
                    0.8045454545,
                    0.8181818182,
                    0.7818181818,
                    0.8954545455,
                    0.5545454545],
             "IA": [0.7235966023,
                    0.8196712237,
                    0.6623715513,
                    0.6913326522,
                    0.7244471605,
                    0.7279750059,
                    0.4657640447],
             "INTR": [0.7692307692,
                      0.9615384615,
                      0.5384615385,
                      0.7307692308,
                      0.6153846154,
                      1,
                      0.3846153846],
             "NPMI": [0.03697772217,
                      0.2091872074,
                      0.2529426709,
                      0.1369797598,
                      0.3571600687,
                      0.1673822769,
                      -0.09328228751],
             "C_v": [0.6196807642,
                     0.8488818727,
                     0.9117373531,
                     0.7314151641,
                     0.9434892155,
                     0.7215635688,
                     0.3299675295],
             "UMASS": [-0.3330375601,
                       -0.4139705481,
                       -0.5427101667,
                       -0.5112633348,
                       -0.533272603,
                       -0.9267126491,
                       -0.1567327418],
             "Silhouette": [0.02577455235,
                            0.07343562014,
                            0.1010876621,
                            0.04688061533,
                            0.1740881998,
                            0.0912418896,
                            -0.1311438699],
             "Size": [1244,
                      610,
                      606,
                      1730,
                      119,
                      139,
                      7499]
             }


data_yelp = {
    "CP": [0.9739130435,
           0.9695652174,
           0.7608695652,
           0.9782608696,
           0.9304347826,
           0.9565217391,
           0.8434782609],
    "IA": [0.8410418098,
           0.8208152648,
           0.6738738806,
           0.8370472989,
           0.7819222049,
           0.7777295296,
           0.7265999232],
    "INTR": [0.625,
             0.7083333333,
             0.5833333333,
             0.125,
             0.625,
             0.5833333333,
             0.375],
    "NPMI": [0.05424737309,
             0.1863250038,
             0.03594719551,
             0.08185830053,
             0.07070389859,
             -0.01960818336,
             0.0009779900804],
    "C_v": [0.5140370404,
            0.7710964428,
            0.7829350792,
            0.6500226177,
            0.6794406871,
            0.420042018,
            0.4092971309],
    "UMASS": [-0.1500976065,
              -0.006611751565,
              -0.1559531217,
              -1.290603319,
              -0.3598672092,
              -5.046813733,
              -0.001932415856],
    "Silhouette": [0.03643617863,
                   0.02226393,
                   0.0129537633,
                   0.1437036935,
                   0.1031631216,
                   0.1559296906,
                   -0.1355222645],
    "Size": [1680,
             1128,
             3731,
             159,
             253,
             106,
             11748],
}

data_wiki = {
    "CP": [0.8391304348,
           0.647826087,
           0.9086956522,
           0.9347826087,
           0.852173913,
           0.9869565217,
           0.5826086957],
    "IA": [0.6591292822,
           0.549600719,
           0.7817339768,
           0.8674295551,
           0.6951638803,
           0.9023322549,
           0.3437335439],
    "INTR": [0.5217391304,
             0.6086956522,
             0.6956521739,
             0.8695652174,
             0.8695652174,
             0.3913043478,
             0.652173913],
    "NPMI": [0.1424413054,
             0.01608315182,
             0.1488256458,
             0.2965071009,
             0.1532843335,
             0.03648650396,
             0.006211843356],
    "C_v": [0.7604068834,
            0.5036810614,
            0.8391926079,
            0.8758811381,
            0.8069097459,
            0.5641084585,
            0.4330502044],
    "UMASS": [-0.3981855078,
              -0.6089112389,
              -0.7256146877,
              -0.514954312,
              -0.3232580534,
              -0.05138801233,
              -0.02216223717],
    "Silhouette": [0.04944068268,
                   0.08062177525,
                   0.05373648932,
                   0.08087407695,
                   0.04831453874,
                   0.08535205148,
                   -0.1507320392],
    "Size": [385,
             236,
             543,
             185,
             1011,
             1889,
             26542]
}



# df = pd.read_csv("EXP_2_results.csv")
# print(df)
# df = df.drop(columns=["Cluster", "Desc"])

# data = data_news

df_news = pd.DataFrame(data_news)
df_wiki = pd.DataFrame(data_wiki)
df_yelp = pd.DataFrame(data_yelp)

# DROP INTR
# df_news = df_news.drop(columns=["INTR"])
# df_wiki = df_wiki.drop(columns=["INTR"])
# df_yelp = df_yelp.drop(columns=["INTR"])


# DROP TO REMOVE RANDOM CLUSTER
# df = df.drop(0)
# df_news = df_news.drop(6)
# df_wiki = df_wiki.drop(6)
# df_yelp = df_yelp.drop(6)



df = pd.concat([df_news, df_wiki, df_yelp])#


# normalized_df = (df - df.min()) / (df.max() - df.min())
# print(normalized_df)
# df = normalized_df


# # Compute Pearson correlation between variables
# results = {}
# for column in ["C_v", "NPMI", "UMASS", "Silhouette", "Size"]:
#     corr, p_value = pearsonr(df[column], df["CP"])
#     results[column] = {"Pearson Correlation": corr, "P-value": p_value}

# # Print the results
# print(pd.DataFrame(results).T)



desired_order = ['CP', 'IA', 'C_v', 'NPMI', 'UMASS', 'Silhouette', 'INTR'] 
df_corr = pd.read_csv("df_corr.csv")
# df_corr = df_corr.drop(columns=["C_v","NPMI", "UMASS", "Sil_768D","Sil_15D"])
df_corr = df_corr.drop(columns=["A_inc","A_name","L_inc","L_name"])

df_corr = df_corr.corr()
print(df_corr)
# df_corr = df_corr.transpose()
# df_corr = df.corr().reindex(index=desired_order, columns=desired_order)
plt.figure(figsize=(5, 3.5))
sns.heatmap(df_corr, annot=True, cmap=sns.light_palette(
    "seagreen", as_cmap=True), fmt=".2f", vmin=-0.5, vmax=1.0)
plt.title("Correlation CP and Automatic Metrics")
plt.xticks(rotation=90)
plt.yticks(rotation=0)
plt.savefig("corr_matrix.pdf", format="pdf", bbox_inches="tight")
plt.show()
