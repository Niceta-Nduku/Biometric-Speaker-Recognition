import random
import Record as r
import features as mfcc

class Verify(object):

    def __init__(self,name="user"):
        self.name = name

    def record(self,folderToSave,environment="s"):
        
        prompt =self.get_digit_string(6)
        print("Prompt: {}".format(prompt))
        ready = input("\npress s to start\n")

        while(ready != 's'):
            ready = input("press s to start\n")

        fileToSave = "{folder}/{prompt}_{speaker}_{env}.wav".format(prompt=prompt,speaker=self.name,folder=folderToSave,env=environment)

        recorder = r.Recorder()
        recorder.start(RECORD_SECONDS=15, playback=False,
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