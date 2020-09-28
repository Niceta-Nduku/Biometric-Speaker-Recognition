import os
import argparse
import numpy as np
from scipy.io import wavfile
from python_speech_features import mfcc
from hmmlearn import hmm

def build_arg_parser():
    parser = argparse.ArgumentParser(description='Train')
    parser.add_argument("--train-folder",dest="train_folder",required=True,help="Input folder with audio for training files")
    parser.add_argument("--test-folder",dest="test_folder",required=False,help="Input folder with audio files for testing")

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

if __name__ == "__main__":
    args = build_arg_parser().parse_args()
    input_folder = args.train_folder


    hmm_models = []

    for dirname in os.listdir(input_folder):

        digit_folder = os.path.join(input_folder,dirname)

        if not os.path.isdir(digit_folder):
            continue

        digit = digit_folder[-1]

        print(digit)

        for speaker in os.listdir(digit_folder):

            speaker_folder =  os.path.join(digit_folder,speaker)
            
            s = speaker_folder.split('\\')

            speaker_name = s[-1]

            print(speaker)

            for filename in [x for x in os.listdir(speaker_folder) if x.endswith('.wav')][:-1]:

                filepath = os.path.join(speaker_folder,filename)
                sampling_rate, audio_signal = wavfile.read(filepath)

                