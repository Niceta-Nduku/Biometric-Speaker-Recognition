
import numpy as np
from sklearn import preprocessing
import python_speech_features as mfcc

WINLEN = 0.025
WINSTEP = 0.01

def getMFCC(audio_signal, sample_rate, single_phrase=False, mutliple_phrases = False, NUM_FEAT = 13, ENERGY = True , Delta = True):
    
    if (single_phrase):
        audio_signal = remove_silence(audio_signal,sample_rate,single_phrase=True,dev=1)
    if (mutliple_phrases):
        audio_signal = remove_silence(audio_signal,sample_rate,mutliple_phrases=True)
        
    mfcc_features = mfcc.mfcc(audio_signal, sample_rate, winlen=WINLEN,winstep=WINSTEP,numcep=-NUM_FEAT,winfunc=np.hamming)
    mfcc_features = preprocessing.scale(mfcc_features)
    
    return mfcc_features

def remove_silence(audio_signal,sample_rate,startframes = 10, endframes =10, dev = 3, single_phrase=False, mutliple_phrases = False):
    preemph=0.97
    FFT = 512
    winfunc=np.hamming
    framelen = WINLEN*sample_rate
    signal = mfcc.sigproc.preemphasis(signal,preemph)
    frames = mfcc.sigproc.framesig(signal, framelen,  framelen)
    numOfFrames,sizeOfFrame = frames.shape
   
    powerspec = mfcc.sigproc.powspec(frames,FFT)
    energy = np.sum(powerspec,1)
    
    
    first_samples = np.concatenate((energy[:startframes], energy[:-endframes]), axis=None)
    mean = np.mean(first_samples)
    std = np.std(first_samples)
    indexes = np.array([]) #frames to keep

    temp = []
    for i in range(len(energy)):
        d = (abs(energy[i]- mean))/std
#         print(d)
        if(d>dev): 
            if(len(indexes) == 0):
                indexes = [i]
            else:
                indexes= np.append(indexes,i)
        temp.append(d)

    if(single_phrase):
        cleaned_signal= mfcc.sigproc.deframesig(frames[indexes[0]-2:indexes[-1]+3],0,framelen, framelen)
    elif(mutliple_phrases):
        cleaned_signal=
    else:
        raise ValueError("Need to specify how to split")

    return cleaned_signal
