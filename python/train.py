import os
import argparse
import numpy as np
from scipy.io import wavfile
import python.features as mfcc
from sklearn.mixture import GaussianMixture
# from hmmlearn.hmm import GMMHMM

class trainUBM():

    def __init__(self,num_coef):

        self.digit = {} #digit UBM

        
    def loadData(self, input_folder):
        """
        Function to load recordings to train 
        """

        for dirname in os.listdir(input_folder):

            digit_folder = os.path.join(input_folder,dirname)

            if not os.path.isdir(digit_folder):
                continue

            ubm = GaussianMixture(n_components=8,covariance_type='diag')


            for speaker in os.listdir(digit_folder):

                speaker_folder =  os.path.join(digit_folder,speaker)
                
                s = speaker_folder.split('\\')

                features = np.asarray(())

                for filename in [x for x in os.listdir(speaker_folder) if x.endswith('.wav')][:-1]:

                    filepath = os.path.join(speaker_folder,filename)
                    sampling_rate, audio_signal = wavfile.read(filepath)

                    feat = mfcc.getMFCC(audio_signal,sampling_rate)

                    if features.size == 0:
                        features = feat
                    else:
                        features = np.vstack((features, feat))

            ubm.fit(features) 
            features = np.asarray(())
            self.digit[dirname] = ubm    





                
if __name__ == "__main__":
    pass