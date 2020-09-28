import os
import argparse
import numpy as np
from scipy.io import wavfile
from python_speech_features import mfcc
from hmmlearn.hmm import GMMHMM

def loadData(input_folder):
    """
    Function to load recordings to train 
    """
    training_data = {}

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

            x = np.array([])

            for filename in [x for x in os.listdir(speaker_folder) if x.endswith('.wav')][:-1]:

                filepath = os.path.join(speaker_folder,filename)
                sampling_rate, audio_signal = wavfile.read(filepath)
                

def enroll_speaker

if __name__ == "__main__":
    pass