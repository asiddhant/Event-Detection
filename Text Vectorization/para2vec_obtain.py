import gensim.models as gnsm
import pandas as pd
import re
from spherecluster import SphericalKMeans
import numpy as np
from sklearn.preprocessing import normalize

def paragraph_splitter(doc,np=5):
    parasplit = doc.split('\n\n')
    if len(parasplit)<2 or len(parasplit)>10:
        linesplit = doc.split('\n')
        linecount = len(linesplit)
        parasplit=[]
        for i in range(np):
            temppara=''
            for j in range(i*np,(i+1)*np):
                temppara+=linesplit[j]
        parasplit+=[temppara]

    pgs=parasplit
    pgs = [(re.sub(r'\W+', ' ', pg).lower() for pg in pgs]
    return pgs

def main():
    # Loading the Model
    print 'Loading Model...'
    model = gnsm.Doc2Vec.load("/home/malab/Desktop/Aditya Siddhant/AdityaSiddhant_ISI/Doc2Vec/model.bin")
    print 'Model Load Complete...'
    
    # Loading the Data 
    print 'Loading Data...'
    newsData = pd.read_csv("newsTextDataset.csv")
    print 'Data Load Complete...'
    
    start_alpha=0.01
    infer_epoch=500
    print 'Calculating Vectors...'
    
    nvec=pd.DataFrame([["ID"]+["PN"]+["V"+ str(i) for i in range(1,301)]])
    nvec.to_csv('newsVecs.csv',header=False,index=False)

    for row in range(newsData.shape[0]):
        try:
            pgs=paragraph_splitter(newsData.FULLTEXT[row])
            for i in range(len(pgs)):
                tnvec=model.infer_vector(re.sub(r'\W+', ' ',pgs[i]).lower().split(),alpha=start_alpha, steps=infer_epoch)
                nvec=pd.DataFrame([[newsData['ID'][row]+i]+list(tnvec)])
                with open('newsVecs.csv', 'a') as f:
                    (nvec).to_csv(f, header=False,index=False)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print("Unable to Vectorize")
        if row%100==0:
            print (str(float(row)*100/float(newsData.shape[0]))+" % Complete")
    
    #Reading the vector file
    newsVecs = pd.read_csv("newsVecs.csv")
    label = newsVecs.ix[:,:2]
    newsVecs = np.newsVecs.ix[:,2:]
    

    #Normalization 
    newsVecs = newsVecs / np.linalg.norm(newsVecs)

    #Clustering - Generating Codebook
    K=1000
    skm = SphericalKMeans(n_clusters=K)
    skm.fit(newsVecs)

    centers = skm.cluster_centers_
    newsVecs = np.matmul(newsVecs,np.transpose(centers))
    
    #Taking Softmax to Convert into Probabilities
    for i in range(newsVecs.shape[0]):
        x=newsVecs[i,:]
        x = e ^ (x - max(x)) / sum(e^(x - max(x))
        newsVecs[i,:]=x

    #Making the output sparse
    newsVecs=newsVecs>0.1

    #Renormalizing
    for i in range(newsVecs.shape[0]):
        newsVecs[i,:]=newsVecs[i,:]/sum(newsVecs[i,:])

    nvec=pd.DataFrame([["ID"]+["V"+ str(i) for i in range(1,K+1)]])
    nvec.to_csv('newsVecs.csv',header=False,index=False)
    temp=newsVecs[0,:]
    for i in range(1,len(newsVecs)):
        if(label.ix[i,1]==0)
            temp=temp/(label.ix[i-1,1]+1)
            tnvec=temp
            nvec=pd.DataFrame([[label.ix[i-1,0]+list(tnvec)])
                with open('newsVecs.csv', 'a') as f:
                    (nvec).to_csv(f, header=False,index=False)
            temp=newsVecs[i,:]
        temp+=newsVecs

main()