import numpy as np
import lda
import lda.datasets
import pickle

# Loading Dataset
newsData = pd.read_csv("newsdataset.csv")
n_topics = 500
n_iter = 1500

#For Reproducibility
randomstate =1

#LDA Model
model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
model.fit(newsData)

#Visualizing Top N Words in a Cluster
topic_word = model.topic_word_ 
n_top_words = 10
for i, topic_dist in enumerate(topic_word):
topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
print('Topic {}: {}'.format(i, ' '.join(topic_words)))

#Assigning each Document to the topic to which it belongs with highest probability
doc_topic = model.doc_topic_

clusters=[]
for i in range(newsData.shape[0]):
	clusters+=[doc_topic[i].argmax()]

clusters=pd.Dataframe(clusters)
output=pd.concat([newsData["ID"],clusters],1)
output.to_csv("naivelda_output.csv",index=False)
