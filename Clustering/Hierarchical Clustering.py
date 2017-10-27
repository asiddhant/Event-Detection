import numpy
import re
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation,LSTM
from keras.optimizers import RMSprop
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import fcluster


# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

optimizer = RMSprop(lr=0.02)
loaded_model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])


def customdistance(x,y):
	X=x-y
	Y=x*y
	I=np.concatenate(X,Y)
	dist=loaded_model.predict(I)
	return dist
	
newsVecs = pd.read_csv("newsVecs.csv")
label = newsVecs.ix[:,:2]
newsVecs = np.newsVecs.ix[:,2:]
#Creates a sparse distance matrix based on custom distance measure
Z = linkage(newsVecs,customdistance)
c, coph_dists = cophenet(Z, pdist(newsVecs))


#Dendrrogram Visualization (Takes a long time : Comment While Running)
plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    Z,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
)
plt.show()

#Truncated Dendrogram (500 Clusters)
plt.title('Hierarchical Clustering Dendrogram (truncated)')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    Z,
    truncate_mode='lastp',  # show only the last p merged clusters
    p=12,  # show only the last p merged clusters
    show_leaf_counts=False,  # otherwise numbers in brackets are counts
    leaf_rotation=90.,
    leaf_font_size=12.,
    show_contracted=True,  # to get a distribution impression in truncated branches
)
plt.show()

#Obtaining the Clusters
max_d = 500
clusters = fcluster(Z, max_d, criterion=customdistance)
clusters=pd.Dataframe(clusters)
output=pd.concat([newsData["ID"],clusters],1)
output.to_csv("deeplearning_output.csv",index=False)



