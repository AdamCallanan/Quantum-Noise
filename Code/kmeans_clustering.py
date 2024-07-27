import os
import pandas as pd
from sklearn.cluster import KMeans

# Loading data as "df"
# Assuming "data.csv" in same directory as this code
code_dir = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(code_dir,"data.csv")
df = pd.read_csv(data_path)

dist_data = df.iloc[:,3:]
num_com = df["computer"].nunique()
kmeans = KMeans(n_clusters=num_com).fit(dist_data)

kmeans_df = pd.DataFrame(df["computer"])
kmeans_df["group"] = kmeans.labels_
print(kmeans_df)