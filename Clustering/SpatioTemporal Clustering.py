#This code makes use of DBSCAN- Density based clustering for spatio-temporal Clustering

from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from numpy.random import rand
from numpy import square, sqrt

def getcoordinates(place):
	geolocator = Nominatim()
	location = geolocator.geocode(place)
	return [location.latitude, location.longitude]
def regionQuery(P, eps, D):	
	neighbourPts = []
	for point in D:
		#print point		
		if sqrt(square(P[1] - point[1]) + square(P[2] - point[2]))<eps:
			neighbourPts.append(point)

	return neighbourPts

def DBSCAN(D, eps, MinPts):
	noise = []
	visited = []
	C = []
	c_n = -1
	for point in D:
		visited.append(point) #marking point as visited
	#	print point		
		neighbourPts = regionQuery(point, eps, D)
		if len(neighbourPts) < MinPts:
			noise.append(point)
		else:
			C.append([])			
			c_n+=1
			expandCluster(point, neighbourPts, C, c_n,eps, MinPts, D, visited)

	print "no. of clusters: " , len(C)	
	print "length of noise:", len(noise)
	for cluster in C:
		col =[rand(1),rand(1),rand(1)]		
		print cluster		
		plt.scatter([i[1] for i in cluster],[i[2] for i in cluster],color=col)
	plt.show()

		

def expandCluster(P, neighbourPts, C, c_n,eps, MinPts, D, visited):
	
	C[c_n].append(P)
	for point in neighbourPts:
		if point not in visited:
			visited.append(point) 
			neighbourPts_2 = regionQuery(point, eps, D)
			if len(neighbourPts_2) >= MinPts:
				neighbourPts += neighbourPts_2
		if point not in (i for i in C):
			C[c_n].append(point)

def spatiotemporalclustering(topic):
	eps = input("enter eps")
	impdata=topic.ix[:,[2,4,5]]
	DBSCAN(topic,eps,10)


def main():
	newsDataset=read.csv("newsDataset.csv")
	Imp=pd.concat([newsDataset["ID"],newsDataset["Cluster"],newsDataset["TimeStamp"],newsDataset["Location"]],1)
	coordinates=[]
	for i in range(Imp.shape[0]):
		coordinates+=[getcoordinates(Imp["Location"][i])]
	coordinates=pd.Dataframe([coordinates])
	Imp=pd.concat([Imp,coordinates],1)
	#Examine Each Topic Individually #Limit the number of Clusters to 10
	for i in  range(500):
		tempin= Imp.loc[(Imp.Cluster== i)]
		tempout = spatiotemporalclustering(tempin)
		tempout = pd.Dataframe(tempout)
		with open("FinalOutput.csv", 'a') as f:
                (tempout).to_csv(f,header=False,index=False)


main()