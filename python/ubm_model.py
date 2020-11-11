import os
import numpy as np
from scipy.io import wavfile
import features as mfcc
from hmmlearn.hmm import GMMHMM
from sklearn.mixture import GaussianMixture
import pickle

class UBM(object):

    def __init__(self,num_coef=64,outputfile="UBM"):
        """

        Args:
            num_coef (int, optional): number of gaussian components. Defaults to 64.
            outputfile (str, optional): file to save UBM. Defaults to "UBM.t".
        """

        self.digit_features = {}
        self.all_digit_UBM = {}
        self.single_ubm = None
        self.num_components = num_coef
        self.file_to_save = outputfile
        

    def loadtrainingfeatures(self,files):
        """
        Extract features to train UBM

        Args:
            files (dict): dictionay (key - digit, value - .wav files)
        """

        for d in files:
        
            all_speaker_features  = []

            for filename in files[d]:

                sampling_rate, audio_signal = wavfile.read(filename)

                feat = mfcc.getMFCC(audio_signal,sampling_rate)

                all_speaker_features.append(feat)

            self.digit_features[d] = all_speaker_features
          
    def trainDigitUBM(self):

        for digit in self.digit_features:
            digit_gmm =  GaussianMixture(n_components=self.num_components,covariance_type='diag')
            
            X = []
            for u in self.digit_features[digit]:
                if len(X) == 0:
                    X = u
                else:
                    X = np.concatenate([X, u])
                    
            digit_gmm.fit(X)

            self.all_digit_UBM[digit] = digit_gmm  

    def trainHMMUBM(self):

        for digit in self.digit_features:
            digit_hmm = GMMHMM(n_components=4,n_mix = 4, covariance_type='diag')
        
            lengths = []
            
            X = []
            for u in self.digit_features[digit]:
                lengths.append(len(u))
                if len(X) == 0:
                    X = u
                else:
                    X = np.concatenate([X, u])
                    
            digit_hmm.fit(X,lengths)

            self.all_digit_UBM[digit] = digit_hmm

    def trainSingleUBM(self):
        self.single_ubm = GaussianMixture(n_components=self.num_components,covariance_type='diag')

        for digit in self.digit_features:
              
            X = []
            for u in self.digit_features[digit]:
                if len(X) == 0:
                    X = u
                else:
                    X = np.concatenate([X, u])
                    
            self.single_ubm.fit(X)

    def saveUBM(self):    
        pickle.dump(self.all_digit_UBM,open(self.file_to_save,"wb"))

    def loadUBM(self):
        self.all_digit_UBM = pickle.load(open(self.file_to_save,"rb"))    

    def getUBM(self,ubm_type = 'd'):
        if ubm_type == 'd':
            return self.all_digit_UBM 
        else:
            return self.single_ubm
    

        
if __name__ == "__main__":
    pass