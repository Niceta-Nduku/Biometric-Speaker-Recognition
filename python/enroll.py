import getpass
import os
import argparse
import numpy as np
from scipy.io import wavfile
import python.features as mfcc
import sklearn.mixture as skm
from hmmlearn import hmm
import say_numbers_prompt as prompter

class enroll(object):
    """
    Class to entoll new speaker into the system
    """

    def __init__(self,name="user"):
        """[summary]

        Args:
            name (str, optional): [description]. Defaults to "user".
        """
        self.name = name
        self.password = "password"
        

    def setCredentials(self):
        self.name = input("Please enter name as \"LastName-FirtName\" with no spaces")
        if (len(name.split())>1):
            print("Please input name with no spaces")
            self.name = input("enter name as \"LastName-FirtName\" with no spaces")
        self.password = getpass.getpass(prompt='Enter secure password')

    def record(self,folderToSave):
        """
        Record 10 digits

        Args:
            folderToSave (str): path to save recordings
        """
        numbers = prompter.generate_number_sequence()

        print("\nWait a second after you see \"start..\" for each number")
        ready = input("\npress s to start\n")

        while(ready != 's'):
            ready = input("press s to start\n")

        x = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0}

        for i in numbers:
            print("Number to read: "+ i)
            recorder = r.Recorder()
            fileToSave = "{folder}/{digit}_{speaker}_{play}.wav".format(digit=i,play=x[i],speaker=self.name,folder=folderToSave)

            recorder.start(RECORD_SECONDS=5, playback=False,
                    WAVE_OUTPUT_FILENAME=fileToSave)
            x[i] +=1
        

    def getFeatures(self,speaker_folder):

        self.speaker_digit_features = {}

        # if not os.path.isdir(speaker_folder):
        #     continue #print error

        for digit in os.listdir(speaker_folder):

            digit_folder =  os.path.join(speaker_folder,digit)
            
            digit_features = []

            features = np.asarray([])

            for filename in [x for x in os.listdir(digit_folder) if x.endswith('.wav')][:5]:

                filepath = os.path.join(digit_folder,filename)
                sampling_rate, audio_signal = wavfile.read(filepath)

                feat = mfcc.getMFCC(audio_signal,sampling_rate)

                if features.size == 0:
                    features = feat
                else:
                    features = np.append([features, feat])

            digit_features.append(features)
            self.speaker_digit_features[digit] = digit_features
        return self.speaker_digit_features


    def adapt(self,ubm):
        
        for d in self.speaker_digit_features:
        
            x = self.speaker_digit_features[d]
            model = ubm[d].predict_proba(x[0])
            sp_digit_model[d] = model
        
        pass
    def save(self):
        pass
        




