import numpy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mongo_to_csv import readMongo

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import warnings

import sys
sys.path.append("..")
from MongoDB.script import Mongodb
from MySQL.database import MySQL

class Clustering(Mongodb):
    def __init__(self):
        super().__init__()
        self.query = '''SELECT * FROM hotels'''

    def createDataFrame(self):
        df = readMongo(self.col)
        # df = pd.read_sql(self.query, self.engine)
        df.to_csv("data.csv", index=False)
        # return self.createHotelDataSet(df)


    def createHotelDataSet(self, df):
        df['Hotel'] = df['Categories'].str.contains('Hotel')
        return df

    def predict(self,df):
        coords = df[['Longitude', 'Latitude']]

        distortions = []
        K = range(1, 25)
        for k in K:
            kmeansModel = KMeans(n_clusters=k)
            kmeansModel = kmeansModel.fit(coords)
            distortions.append(kmeansModel.inertia_)
        fig, ax = plt.subplots(figsize=(12, 8))
        plt.plot(K, distortions, marker='o')
        plt.xlabel('k')
        plt.ylabel('Distortions')
        plt.title('Elbow Method For Optimal k')
        plt.savefig('elbow.png')
        plt.show()
        sil = []
        kmax = 30

        # dissimilarity would not be defined for a single cluster, thus, minimum number of clusters should be 2
        for k in range(2, kmax + 1):
            kmeans = KMeans(n_clusters=k).fit(coords)
            labels = kmeans.labels_
            sil.append(silhouette_score(coords, labels, metric='euclidean'))

        kmeans = KMeans(n_clusters=3, init='random',
                        n_init=10, max_iter=300,
                        tol=1e-04, random_state=0)
        kmeans.fit(coords)
        y = kmeans.labels_
        print("k = 5", " silhouette_score ", silhouette_score(coords, y, metric='euclidean'))
        print(kmeans.cluster_centers_)
        df['cluster'] = kmeans.predict(df[['Longitude','Latitude']])
        return df

    def getTopHotel(self,df):
        top_destination = df.sort_values(by=['Review Count', 'Stars'], ascending=False)
        top_destination.head()


if __name__ == '__main__':
    model = Clustering()
    model.createDataFrame()
    # results = model.predict(dataset)