import os
import argparse
import numpy as np
from scipy.io import wavfile
import python.features as mfcc
import sklearn.mixture as skm
from hmmlearn import hmm

class UBM(object):

    def __init__(self,num_coef):

        self.digit_features = {}
        self.all_digit_UBM = {}

    def loadtrainingfeatures(self,input_folder):

        self.digit_features = {}

        for dirname in os.listdir(input_folder):

            digit_folder = os.path.join(input_folder,dirname)

            if not os.path.isdir(digit_folder):
                continue

            all_speaker_features  = []

            for speaker in os.listdir(digit_folder):

                speaker_folder =  os.path.join(digit_folder,speaker)


                features = np.asarray(())

                for filename in [x for x in os.listdir(speaker_folder) if x.endswith('.wav')][:5]:

                    filepath = os.path.join(speaker_folder,filename)
                    sampling_rate, audio_signal = wavfile.read(filepath)

                    feat = mfcc.getMFCC(audio_signal,sampling_rate)

                    if features.size == 0:
                        features = feat
                    else:
                        features = np.vstack((features, feat))

                all_speaker_features.append(features)

            self.digit_features[dirname] = all_speaker_features
        
    
    def trainUBM(self):

        for digit in self.digit_features:
            digit_hmm = hmm.GMMHMM(n_components=8, n_iter=100, init_params="smt", covariance_type='diag',algorithm="viterbi")
            
            for speaker in digit_features[digit]:
                digit_hmm.fit(speaker)
            self.all_digit_UBM[digit] = digit_hmm

    def saveUBM(self,filename):

        pass

    def loadUBM(self,filename):
        pass    

    def getUBM(self):
        return self.all_digit_UBM






                
if __name__ == "__main__":
    pass