import numpy as np
import sys
from sklearn import svm

# Read train data
X_train = np.loadtxt(sys.argv[1], dtype="float", delimiter=",")
X_outliers = np.loadtxt(sys.argv[2], dtype="float", delimiter=",")
X_test = np.loadtxt(sys.argv[3], dtype="float", delimiter=",")

# fit svm model
clf = svm.OneClassSVM(nu=0.3, kernel="rbf", gamma=0.1)
clf.fit(X_train)
y_pred_train = clf.predict(X_train)
y_pred_test = clf.predict(X_test)
y_pred_outliers = clf.predict(X_outliers)
n_error_train = y_pred_train[y_pred_train == -1].size
n_error_test = y_pred_test[y_pred_test == -1].size
n_error_outliers = y_pred_outliers[y_pred_outliers == 1].size

print 'Training set size: %d' %y_pred_train.size
print 'No. of Outliers in Training set: %d' %n_error_train
print 'No. of outliers in test set: %d' %n_error_test
print 'No. of inliers in outlier set: %d' %n_error_outliers

#for i,a in enumerate(y_pred_train):
#	print '%s is %d' % (a, i)

for i in xrange(len(y_pred_test)):
	if y_pred_test[i] == -1:
		print i, X_test[i]

