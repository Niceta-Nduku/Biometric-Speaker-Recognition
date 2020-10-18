import os
import pickle
from scipy.io import wavfile
import features as mfcc
import sklearn.mixture as skm
from hmmlearn import hmm
import say_numbers_prompt as prompter
import Record as r
import utils
import enroll
import Validate

class speaker(object):

    def __init__(self,name="user",modelsfolder = "speaker_models/",num_features = 13):
        """[summary]

        Args:
            name (str, optional): [description]. Defaults to "user".
        """
        self.name = name
        self.password = "password"
        self.model_file = os.path.join(modelsfolder,name)
        self.speaker_model = None
        self.num_features = num_features

    def enroll(self,digit_ubms,recordings,):
        #record
        features = enroll.getSpeakerFeatures(recordings,self.num_features)
        self.speaker_model = enroll.adapt_all_digits(digit_ubms,features)
        #save model
        print("User {} enrolled".format(self.name))

    def verify(self,recording,digit_ubms,prompt = None):
        #record
        #get speaker digit models if None
        #extract features from prompt recording
        features = Validate.extract_features(recording,prompt,self.num_features)
        #genearate model for h0 
        h0_hmm = Validate.generateHMM(self.speaker_model,prompt)
        #genearate model for h1
        h1_hmm = Validate.generateHMM(digit_ubms,prompt)
        #get score
        score = Validate.score(h0_hmm,h1_hmm,features)




