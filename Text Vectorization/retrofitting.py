import argparse
import gzip
import math
import numpy
import re
import sys

from copy import deepcopy

isNumber = re.compile(r'\d+.*')
def norm_doc(doc):
  if isNumber.search(doc.lower()):
    return '---num---'
  elif re.sub(r'\W+', '', doc) == '':
    return '---punc---'
  else:
    return doc.lower()

''' Read all the doc vectors and normalize them '''
def read_doc_vecs(filename):
  docVectors = {}
  if filename.endswith('.gz'): fileObject = gzip.open(filename, 'r')
  else: fileObject = open(filename, 'r')
  
  for line in fileObject:
    line = line.strip().lower()
    doc = line.split()[0]
    docVectors[doc] = numpy.zeros(len(line.split())-1, dtype=float)
    for index, vecVal in enumerate(line.split()[1:]):
      docVectors[doc][index] = float(vecVal)
    ''' normalize weight vector '''
    docVectors[doc] /= math.sqrt((docVectors[doc]**2).sum() + 1e-6)
    
  sys.stderr.write("Vectors read from: "+filename+" \n")
  return docVectors

''' Write doc vectors to file '''
def print_doc_vecs(docVectors, outFileName):
  sys.stderr.write('\nWriting down the vectors in '+outFileName+'\n')
  outFile = open(outFileName, 'w')  
  for doc, values in docVectors.iteritems():
    outFile.write(doc+' ')
    for val in docVectors[doc]:
      outFile.write('%.4f' %(val)+' ')
    outFile.write('\n')      
  outFile.close()
  
''' Read the PPDB doc relations as a dictionary '''
def read_NER(filename, docVecs):
  NER = {}
  for line in open(filename, 'r'):
    docs = line.lower().strip().split()
    NER[norm_doc(docs[0])] = [norm_doc(doc) for doc in docs[1:]]
  return NER

''' Retrofit doc vectors to a NER '''
def retrofit(docVecs, NER, numIters):
  newWordVecs = deepcopy(docVecs)
  wvVocab = set(newWordVecs.keys())
  loopVocab = wvVocab.intersection(set(NER.keys()))
  for it in range(numIters):
    # loop through every node also in ontology (else just use data estimate)
    for doc in loopVocab:
      docNeighbours = set(NER[doc]).intersection(wvVocab)
      numNeighbours = len(docNeighbours)
      #no neighbours, pass - use data estimate
      if numNeighbours == 0:
        continue
      # the weight of the data estimate if the number of neighbours
      newVec = numNeighbours * docVecs[doc]
      # loop over neighbours and add to new vector (currently with weight 1)
      for ppWord in docNeighbours:
        newVec += newWordVecs[ppWord]
      newWordVecs[doc] = newVec/(2*numNeighbours)
  return newWordVecs
  
def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--input", type=str, default=None, help="Input doc vecs")
  parser.add_argument("-l", "--NER", type=str, default=None, help="Lexicon file name")
  parser.add_argument("-o", "--output", type=str, help="Output doc vecs")
  parser.add_argument("-n", "--numiter", type=int, default=10, help="Num iterations")
  args = parser.parse_args()

  docVecs = pd.read_csv("newsVecs.csv")
  label = newsVecs.ix[:,:1]
  docVecs = np.newsVecs.ix[:,1:]
    
  NER = read_NER(args.NER, docVecs)
  numIter = int(args.numiter)
  outFileName = args.output
  
  docVecs=retrofit(docVecs, NER, numIter)
  docVecs=pd.concat([pd.Dataframe(label),pd.Dataframe(docVecs)],1)
  docVecs.to_csv("newsVecs.csv",index=False)

main()