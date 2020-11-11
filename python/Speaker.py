import os
import utils
import enroll
import numpy as np
import Validate


class speaker(object):

    def __init__(self, name="user", num_features=13):
        """[summary]

        Args:
            name (str, optional): [description]. Defaults to "user".
        """
        self.name = name
        self.speaker_model = None
        self.num_features = num_features
        self.threshold = 0

    def enroll(self, digit_ubms, recordings,ubm_type ='d', speaker_test_phrases=None ,alter_speaker_phrases=None):
        # record
        features = enroll.getSpeakerFeatures(recordings, self.num_features)
        self.speaker_model = enroll.adapt_all_digits(digit_ubms, features,ubm_type=ubm_type)

        if speaker_test_phrases!=None and  alter_speaker_phrases!=None:
            self.__setThreshold(digit_ubms, speaker_test_phrases ,alter_speaker_phrases)
            self.__saveToDevice()

        print("User {} enrolled".format(self.name))

    def verify(self, recording, digit_ubms, prompt=None,gaussians = 64,ubm_type='d'):

        features = Validate.extract_features(
            recording, prompt, self.num_features)

        h0_hmm = Validate.generateHMM(self.speaker_model, prompt,gaussians)

        h1_hmm = digit_ubms
        if ubm_type == 'd':
            h1_hmm = Validate.generateHMM(digit_ubms, prompt,gaussians)
        else:
            h1_mmm = digit_ubms

        score = Validate.score(h0_hmm, h1_hmm, features)

        return score

    def __setThreshold(self,ubm_model, speaker_test_phrases ,alter_speaker_phrases):

        llrpositive = []        
        for f in speaker_test_phrases:
            recording = f
            temp = f.split("\\")[-1]
            prompt = temp.split("_")[0]
            llr = self.verify(recording,ubm_model,prompt,coef=ubm_model.n_components)
            llrpositive.append(llr)
        
        llrnegative = []
        
        for f in alter_speaker_phrases:
            recording = f
            temp = f.split("\\")[-1]
            prompt = temp.split("_")[0]
            llr = self.verify(recording,ubm_model,prompt,coef=ubm_model.n_components)
            llrnegative.append(llr)

        FAR=[]
        FRR=[]

        thresholds = np.arange(-2000,2000,0.5)
        for t in range(len(thresholds)):
            FAR.append(np.mean(llrnegative>thresholds[t]))
            FRR.append(np.mean(llrpositive<thresholds[t]))

        x = np.array(FAR)
        y = np.array(FRR)

        eerthres =np.argmin(np.abs(x-y))
        eer = np.mean((x[eerthres],y[eerthres]))

        self.threshold = thresholds[eerthres]

    def __saveToDevice(self):
        #save model 
        #save threshold
        pass

    def getSizeOfModel(self):
        model_size = 0
        for i in range(10):
            w=self.speaker_model[str(i)].weights_
            m=self.speaker_model[str(i)].means_
            c=self.speaker_model[str(i)].covariances_
            model_size+=(w.size * w.itemsize)+(m.size * m.itemsize)+(c.size * c.itemsize)
        return model_size