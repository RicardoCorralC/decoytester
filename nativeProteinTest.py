# Ricardo Corral Corral, October 2015
import numpy as np
import sys
from sklearn import svm
from sklearn.base import BaseEstimator
import matplotlib.pyplot as plt
from sklearn import cross_validation
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.neighbors import kneighbors_graph


class native_tester(BaseEstimator):

    def __init__(self,nu=0.5,gamma=0.0):
        self.oneClassBaseFunctionsList = []
        self.nu = nu
        self.gamma = gamma

    def fit(self,X,n_iter=5,random=True):
    #    if not random:
            x_train = X[:]
            for i in xrange(n_iter):

                print "\nIteration %d over %d samples" %(i,len(x_train))

                if len(x_train) == 0:
                    break

                clf = svm.OneClassSVM(nu=self.nu, kernel="rbf", gamma=self.gamma)
                clf.fit(x_train)

                self.oneClassBaseFunctionsList.append(clf)

                _x_train = []
                for j in xrange(len(x_train)):
                    if not clf.predict([x_train[j]])[0]==1:
                        _x_train.append(x_train[j])

                x_train = _x_train[:]

    #    else:



            #rs = cross_validation.ShuffleSplit(len(X), n_iter=n_iter, test_size=.6, random_state=0)
            for _i in xrange(1,n_iter):

                clusterer = KMeans(n_clusters=_i)
                clusters = clusterer.fit_predict(X)

                for i in xrange(_i):

                    x_train = [X[k] for k in xrange(len(X)) if clusters[k]==i]

                    print "\nIteration over %d samples" %(len(x_train))

                    clf = svm.OneClassSVM(nu=0.3, kernel="rbf", gamma=0.1)
                    clf.fit(x_train)

                    self.oneClassBaseFunctionsList.append(clf)

                    #_x_train = []
                    #for j in xrange(len(x_train)):
                 #       if not clf.predict([x_train[j]])[0]==1:
                    #        _x_train.append(x_train[j])

                print '\nFitting [DONE]'


    def predict(self,X):
        preds = []
        for clf in self.oneClassBaseFunctionsList:
            preds.append(clf.predict(X))
        #res = sum(preds)/len(preds)
        res = np.vstack(preds)
        #print res
        res = [max(v) for v in res.T]
        print res
        #plt.plot(res)
        #plt.show()
        return res

def main():
    #culled_pdb_rcc.csv
    X_native_train_set = np.loadtxt('culled_pdb_rcc.csv', dtype="float", delimiter=",")
    #nativfoldedprots_rcc.csv
    X_native_test_set = np.loadtxt('nativfoldedprots_rcc.csv', dtype="float", delimiter=",")
    #decoys_4states_rcc.csv
    X_decoy_set = np.loadtxt('decoys_4states_rcc.csv', dtype="float", delimiter=",")

    #CATHFINAL.txt
    X_cath_domains_set = np.loadtxt('CATHFINAL.txt', dtype="float",usecols=(range(1,27)), delimiter=",")

    print X_cath_domains_set
    print X_cath_domains_set.shape
    exit()

    nt = native_tester()
    nt.fit(X_native_train_set[:1000])

    print '\nTesting over native train set structures'
    A = nt.predict(X_native_test_set)

    print '\nTesting over native test set structures'
    B = nt.predict(X_native_test_set)

    print '\nTesting over decoy structures'
    C = nt.predict(X_decoy_set)

    plt.hist(A,label='A',alpha=0.5,normed=1,bins=50)
    plt.hist(B,label='B',alpha=0.5,normed=1,bins=50)
    plt.hist(C,label='C',alpha=0.5,normed=1,bins=50)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
