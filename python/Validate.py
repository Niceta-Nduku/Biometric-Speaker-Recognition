import random
import Record as r
import features as mfcc

class Verify(object):

    def __init__(self,name="user"):
        self.name = name

    def record(self,fileToSave):
        
        prompt =self.get_digit_string(6)
        print("Prompt: {}".format(prompt))
        recorder = r.Recorder()
        recorder.start(RECORD_SECONDS=10, playback=False,
                WAVE_OUTPUT_FILENAME=fileToSave)


    def verifyCredentials(self):
        pass
    def extract_features(self):
        pass
    def verifySpeaker(self):
        pass
    
    def get_digit_string(self,length):
        digits = '0123456789'
        string = ''.join((random.choice(digits) for i in range(length)))
        return string