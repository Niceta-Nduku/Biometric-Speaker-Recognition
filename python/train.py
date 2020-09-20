import os
import argparse
import numpy as np
from scipy.io import wavfile
from python_speech_features import mfcc
from hmmlearn.hmm import GMMHMM

def loadData(folder):
    """
    Function to load recordings to train 
    """

    #open folder
    #for each subfolder, (check if digit corresponds)
    #      read in wav file (check if digit corresponds)
    #      extract  features
    #      append to array of features
    #      append label (name_number)
    #



class HMMTrain(object):
    def __init__(self, n_states=8, n_gaussians=8, cov_type='diag', n_iter=1000):
        self.n_states = n_states
        self.n_gaussians = n_gaussians
        self.cov_type = cov_type
        self.n_iter = n_iter
        self.models = [] 
    
        self.model = GMMHMM(n_components=self.n_states,n_mix=self.n_gaussians, n_iter=self.n_iter)

    def train(self,X):
        self.models.append(self.model.fit(X))

    def get_score(self):
        self.model.score(input)

if __name__ == if __name__ == "__main__":
    pass