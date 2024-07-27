import os
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Loading data as "df"
# Assuming "data.csv" in same directory as this code
code_dir = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(code_dir,"data.csv")
df = pd.read_csv(data_path)

# print(len(df.iloc[:,3:].columns))

n = 22
pca = PCA (n_components=n)
reduced_data = pca.fit_transform(df.iloc[:,3:])
reduced_data = pd.DataFrame(reduced_data)

dist_data = reduced_data.iloc[:,:n]
num_com = df["computer"].nunique()
kmeans = KMeans(n_clusters=num_com).fit(dist_data)

kmeans_df = pd.DataFrame(df["computer"])
kmeans_df["group"] = kmeans.labels_
print(f"K-means clustering of {n} dimension PCA reduced data:")
print(kmeans_df)
print()

kmeans_crosstab = pd.crosstab(kmeans_df["computer"],kmeans_df["group"],normalize="index")
print("Analyzing the K-means clustering of the data:")
print(kmeans_crosstab)