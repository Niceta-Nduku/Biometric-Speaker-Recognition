import os
import numpy as np
from scipy.io import wavfile
import features as mfcc
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
        
    
    def trainUBM(self):

        for digit in self.digit_features:
            digit_gmm = GaussianMixture(n_components=self.num_components,covariance_type='diag')
        
            lengths = []
            
            X = []
            for u in self.digit_features[digit]:
                lengths.append(len(u))
                if len(X) == 0:
                    X = u
                else:
                    X = np.concatenate([X, u])
                    
            digit_gmm.fit(X)

            self.all_digit_UBM[digit] = digit_gmm  

    def saveUBM(self):    
        pickle.dump(self.all_digit_UBM,open(self.file_to_save,"wb"))

    def loadUBM(self):
        self.all_digit_UBM = pickle.load(open(self.file_to_save,"rb"))    

    def getUBM(self):
        return self.all_digit_UBM 
    

        
if __name__ == "__main__":
    pass