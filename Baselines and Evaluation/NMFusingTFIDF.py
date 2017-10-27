from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pickle
import numpy as np
import scipy.sparse as sp
from sys import float_info

newsData = pd.read_csv("newsdataset.csv")

trainset=[]
for row in range(newsData.shape[0]):
	trainset+=[re.sub(r'\W+', ' ', newsData.FULLTEXT[row]).lower()]

count_vectorizer = CountVectorizer()
count_vectorizer.fit_transform(trainset)
term_matrix = count_vectorizer.transform(trainset)

tfidf = TfidfTransformer(norm="l2")
tfidf.fit(termmatrix)
tfidfmatrix = tfidf.transform(termmatrix)

#Only for Visualization Purposes. Takes Lots of Space
densetfidf=tf_idf_matrix.todense()

class NMF(object):

    def convert_sparse_matrix(self, data):
        s1, s2 = data.shape
        if s1 == 3:
            data = data.T
        vals = data[:, 2]
        rows = data[:, 0]
        cols = data[:, 1]
        n = rows.max()
        m = cols.max()
        A = sp.csr_matrix((vals, (rows, cols)), shape=(n + 1, m + 1))
        return A

    def rand_sparse_matrix(self, n=10, m=10, alpha=0.1):
        num = int(n * m * alpha)
        vals = np.random.rand(num)
        rows = np.random.randint(0, n, size=num)
        cols = np.random.randint(0, m, size=num)
        A = sp.csr_matrix((vals, (rows, cols)), shape=(n, m))
        return A

    def setup(self, A, k=5):
        n, m = A.shape
        # sigma = ((float)(A.size)) / n / m
        W0 = np.random.rand(n, k)
        H0 = np.random.rand(k, m)

        self.errors = []
        self.A = A
        self.H = H0
        self.W = W0

        self.clusterH = None
        self.clusterW = None

    def run(self, iter_num=100, calc_error=False, calc_error_num=10):
        H = self.H
        W = self.W
        eps = float_info.min
        A = self.A

        for i in range(1, iter_num):

            # update H
            # H=H.*(W'*A)./(W'*W*H+eps)
            H = H * ((A.T * W).T) / (W.T.dot(W).dot(H) + eps)
            # update W
            # W=W.*(A*H')./(W*(H*H')+eps);
            W = W * (A * H.T) / (W.dot(H.dot(H.T)) + eps)

            if i % calc_error_num != 0:
                continue
            print '.',
            if not calc_error:
                continue
            M = A - W.dot(H)
            error = np.multiply(M, M).sum()
            self.errors.append(error)
        self.H = H
        self.W = W

        print 'end'

    def clusters(self):
        self.clusterH = np.argmax(self.H, 0)
        self.clusterW = np.argmax(self.W, 1)

nmf = NMF()
A = tfidfmatrix
nmf.setup(A, k=500)
nmf.run(iter_num=100)
clusters=nmf.clusters()

clusters=pd.Dataframe(clusters)
output=pd.concat([newsData["ID"],clusters],1)
output.to_csv("nmfusingtfidf_output.csv",index=False)