import random

class Verify(object):

    def record(self):
        

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