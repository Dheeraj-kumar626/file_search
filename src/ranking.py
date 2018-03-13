
from math import log
import operator
from nltk.stem.porter import *

k1 = 1.2
k2 = 100
b = 0.75
R = 0.0

def score_BM25(n, f, qf, r, N, dl, avdl):
        K = compute_K(dl, avdl)
        first = log( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)) )
        second = ((k1 + 1) * f) / (K + f)
        third = ((k2+1) * qf) / (k2 + qf)
        return first * second * third

def compute_K(dl, avdl):
        return k1 * ((1-b) + b * (float(dl)/float(avdl)) )

class QueryProcessor:
        def __init__(self,queries, index, dlt):
                self.queries = queries
                self.index = index
                self.dlt = dlt

        def run(self):
                results = []
                for query in self.queries:
                        results.append(self.run_query(query))
                return results

        def run_query(self, query):
                query_result = dict()
                for term in query:
                        if term in self.index:
                                doc_dict = self.index[term] # retrieve index entry
                                for docid, freq in doc_dict.items(): #for each document and its word frequency
                                        score = score_BM25(n=len(doc_dict), f=freq, qf=1, r=0, N=len(self.dlt),
                                                                           dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length()) # calculate score
                                        if docid in query_result: #this document has already been scored once
                                                query_result[docid] += score
                                        else:
                                                query_result[docid] = score
                return query_result