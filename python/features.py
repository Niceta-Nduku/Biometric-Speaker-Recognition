
import numpy as np
from sklearn import preprocessing
import python_speech_features as mfcc

WINLEN = 0.025
WINSTEP = 0.01
NUM_FEAT = 13
ENERGY = True

def getMFCC(audio_signal, sample_rate):
    
    mfcc_features = mfcc.mfcc(audio_signal, sample_rate, winlen=WINLEN,winstep=WINSTEP,numcep=-NUM_FEAT)
    mfcc_features = preprocessing.scale(mfcc_features)
    
    return mfcc_features