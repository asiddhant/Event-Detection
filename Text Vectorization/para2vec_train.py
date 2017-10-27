#Training Paragraph 2 Vec Model
import gensim.models as gnsm

#Training parameters
vector_size = 300
window_size = 10
min_count = 1
sampling_threshold = 1e-5
negative_size = 5
train_epoch = 500
# Enter 0 = dbow; 1 = dmpv
dm = 1 
#number of parallel processes
worker_count = 8

# Split a Document into Paragraphs.
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

newsDataset=read.csv("newsDataset.csv")
text=[]
for i in range(newsDataset.shape[0]):
	text+=[paragraph_splitter(newsDataset.FULLTEXT[i])]

#input corpus
train_corpus = text
#output model
saved_path = "model.bin"

#train doc2vec model
docs = gnsm.doc2vec.TaggedLineDocument(train_corpus)
model = gnsm.Doc2Vec(docs, size=vector_size, window=window_size, min_count=min_count, 
                     sample=sampling_threshold, workers=worker_count, hs=0, dm=dm, negative=negative_size, 
                     dbow_words=1, dm_concat=1, iter=train_epoch)

#save model
model.save(saved_path)