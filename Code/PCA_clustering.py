import os
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Loading data as "df"
# Assuming "data.csv" in same directory as this code
code_dir = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(code_dir,"data.csv")
df = pd.read_csv(data_path)

pca = PCA (n_components=3)
reduced_data = pca.fit_transform(df.iloc[:,3:])
reduced_data = pd.DataFrame(reduced_data)
reduced_data.columns = ["x","y","z"]
reduced_data["computer"] = df["computer"]

fig = plt.figure()
ax = plt.axes(projection='3d')
for computer in reduced_data["computer"].unique():
    reduced_com = reduced_data[reduced_data.computer == computer].reset_index()
    ax.scatter(reduced_com["x"],reduced_com["y"],reduced_com["z"],label=computer)

plt.legend(title="computer")
plt.show()
# analysis_dir = os.path.join(code_dir,'..',"Analysis")
# analysis_dir = os.path.normpath(analysis_dir)
# plt.savefig(f"{analysis_dir}/PCA.png")