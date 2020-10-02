import getpass
import os
import argparse
import numpy as np
from scipy.io import wavfile
import python.features as mfcc
import sklearn.mixture as skm
from hmmlearn import hmm

class enroll():

    def __init__(self):
        self.name = "User"
        self.password = "admin"
        pass
    def setCredentials(self):
        self.name = input("Please enter name as \"LastName-FirtName\" with no spaces")
        if (len(name.split())>1):
            print("Please input name with no spaces")
            self.name = input("enter name as \"LastName-FirtName\" with no spaces")
        self.password = getpass.getpass(prompt='Enter secure password')

    def record(self):
        #release promp
        pass

    def getFeatures(self,speaker_folder):

        speaker_features = {}

        # if not os.path.isdir(speaker_folder):
        #     continue #print error

        for digit in os.listdir(speaker_folder):

            digit_folder =  os.path.join(speaker_folder,digit)
            
            digit_features = []

            features = np.asarray(())

            for filename in [x for x in os.listdir(digit_folder) if x.endswith('.wav')][:5]:

                filepath = os.path.join(digit_folder,filename)
                sampling_rate, audio_signal = wavfile.read(filepath)

                feat = mfcc.getMFCC(audio_signal,sampling_rate)

                if features.size == 0:
                    features = feat
                else:
                    features = np.vstack((features, feat))

            digit_features.append(features)
            speaker_features[digit] = digit_features


    def adapt(self):
        #get digit ubm
        #predict
        
        pass
    def save(self):
        pass
        




