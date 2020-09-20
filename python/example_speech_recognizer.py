import os
import argparse
import numpy as np
from scipy.io import wavfile
from python_speech_features import mfcc
from hmmlearn import hmm

def build_arg_parser():
    parser = argparse.ArgumentParser(description='Train')
    parser.add_argument("--train-folder",dest="train-folder",required=True,help="Input folder with audio for training files",
    "--test-folder",dest="test-folder",required=True,help="Input folder with audio files for testing")

    return parser


class HMMTrain(object):
    def __init__(self, model_name='GaussianHMM',n_states=8, n_gaussians=8, cov_type='diag', n_iter=1000):
        self.model_name = model_name
        self.n_states = n_states
        self.n_gaussians = n_gaussians
        self.cov_type = cov_type
        self.n_iter = n_iter
        self.models = [] 
    
        if self.model_name == 'GaussianHMM':
            self.model = hmm.GaussianHMM(n_components=self.n_states,n_iter=self.n_iter,covariance_type=self.cov_type)
        elif self.model_name == 'GMMHMM':
            self.model = hmm.GMMHMM(n_components=self.n_states,n_mix=self.n_gaussians, n_iter=self.n_iter)
        else:
            raise TypeError('Invalid model type')


    def train(self,X):
        np.seterr(all='ignore')
        self.models.append(self.model.fit(X))

    def get_score(self,input):
        self.model.score(input)

if __name__ == if __name__ == "__main__":
    args = build_arg_parser().parse_args()
    input_folder = args

    hmm_models = []

    for dirname in os.listdir(input_folder):

        