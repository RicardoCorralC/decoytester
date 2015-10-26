# Ricardo Corral Corral, October 2015
import urllib
import RCCpackage.RCCobject as rcco
import RCCpackage.RCCutils as rccu
import tarfile
import os
import warnings
from bs4  import BeautifulSoup
from nativeProteinTest import *

test_html = open('dataset_CASP11.txt','r').read()


def downloadData(nativePDB='http://zhanglab.ccmb.med.umich.edu/decoys/casp11/T0759.native.pdb',
                 zhangModel='http://zhanglab.ccmb.med.umich.edu/decoys/casp11/T0759.Zhang-Server_model1.pdb',
                 quarkModel='http://zhanglab.ccmb.med.umich.edu/decoys/casp11/T0759.QUARK_model1.pdb',
                 decoySet='http://zhanglab.ccmb.med.umich.edu/decoys/casp11/T0759.tar.bz2',
                 stop=10000):

    print '# nativePDB:', nativePDB
    print '# zhangModel:', zhangModel
    print '# quarkModel:', quarkModel
    print '# decoySet:', decoySet

    print '\nRetrieving data...'
    urllib.urlretrieve (nativePDB, "_native.pdb")
    print '.'*10
    urllib.urlretrieve (zhangModel, "_zhangModel.pdb")
    print '.'*10
    urllib.urlretrieve (quarkModel, "_quarkModel.pdb")
    print '.'*10
    urllib.urlretrieve (decoySet, "_decoySet.tar.bz2")
    print '[DONE]\n'

    #print 'Uncompressing data...'
    #opener, mode = tarfile.open, 'r:bz2'
    #cwd = os.getcwd()
    #if not os.path.exists("_decoySetDir"):
    #    os.makedirs("_decoySetDir")
    #os.chdir("_decoySetDir")

    #file = opener("../_decoySet.tar.bz2", mode)
    #file.extractall()
    #file.close()
    #os.chdir(cwd)
    #print '[Done]'

    print '\nConstructing 26d vectors...'

    rccsNative = rcco.RCC("_native.pdb",None).RCCvector
    rccsZhang = rcco.RCC("_zhangModel.pdb",None).RCCvector
    rccsQUARK = rcco.RCC("_quarkModel.pdb",None).RCCvector

    print rccsNative
    print rccsZhang
    print rccsQUARK

    rccsDecoys = []

    #print '\nConstructing 26d vectors for decoy set...'
    #howmany = 0
    #for decoyname in rccu.iter_directory_files("_decoySetDir"):
    #    if howmany > stop: break
    #    howmany += 1
    #    _decoy = rcco.RCC(decoyname,None).RCCvector
    #    rccsDecoys.append(_decoy)
    #    print _decoy
    #    break

    print '[DONE]'

    return {'native':rccsNative,
            'zhang':rccsZhang,
            'quark':rccsQUARK,
            'decoys':rccsDecoys}

def runExperiment(htmltable,clf):
    parsed_html = BeautifulSoup(htmltable)
    links_list = [ a['href'] for a in parsed_html.find_all('a') ]
    fout = open('RESULTS.txt','a',0)
    for i in xrange(len(links_list)/5):
        print '\n### Starting new dataset'
        start = 5*i
        ls = links_list[start:start+5]
        nativePDB, _, zhangModel, quarkModel, decoySet = ls
        npdb = nativePDB[nativePDB.rfind('/')+1:]
        target_name = npdb[:npdb.find('.')]

        _data = downloadData(nativePDB=nativePDB,
                             zhangModel=zhangModel,
                             quarkModel=quarkModel,
                             decoySet=decoySet)

        nativePDB_pred = str(clf.predict(_data['native'])[0])
        zhangModel_pred = str(clf.predict(_data['zhang'])[0])
        quarkModel_pred = str(clf.predict(_data['quark'])[0])
        decoySet_pred = clf.predict(_data['decoys'])
        decoySet_plus = decoySet_pred.count(1)
        decoySet_minus = decoySet_pred.count(-1)

        print 'nativePDB_pred', nativePDB_pred
        print 'zhangModel_pred', zhangModel_pred
        print 'quarkModel_pred', quarkModel_pred
        print 'decoySet_pred', decoySet_pred

        fout.write('%s,%s,%s,%s,%d,%d,%s\n' % (target_name,nativePDB_pred,
                                               zhangModel_pred,
                                               quarkModel_pred,
                                               decoySet_plus,
                                               decoySet_minus,
                                               ','.join([str(a) for a in decoySet_pred])))


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    X_native_train_set = np.loadtxt('culled_pdb_rcc.csv', dtype="float", delimiter=",")
    #nativfoldedprots_rcc.csv
    X_native_test_set = np.loadtxt('nativfoldedprots_rcc.csv', dtype="float", delimiter=",")
    #decoys_4states_rcc.csv
    X_decoy_set = np.loadtxt('decoys_4states_rcc.csv', dtype="float", delimiter=",")

    print '\n### Fitting predictor...'
    nt = native_tester()
    nt.fit(np.vstack([X_native_train_set[:],X_native_test_set[:]]))
    print '### DONE\n'

    runExperiment(htmltable=test_html,clf=nt)
    #dataset = downloadData()
    #print dataset
