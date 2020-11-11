import time
import pickle
from ubm_model import UBM
import Speaker

#variables 
nFeatures = 13

_start = time.process_time()
def tic():
    global _start
    _start = time.process_time()

def toc():
    return time.process_time()-_start

collected_files = pickle.load(open("collected_enrollment_data.f","rb"))
free_spoken_files = pickle.load(open("free_speech_enrollment_data.f","rb"))

collected_Speakers = ["Speaker1","Speaker2","Speaker3","Speaker4","Speaker5","Speaker6","Speaker7","Speaker8","Speaker9"]

speakers = collected_Speakers
enrollment_files = collected_files

final_ubm = pickle.load(open("UBM_64","rb"))

# #enroll speakers
for s in speakers:
    #new speaker
    tic()
    user = Speaker.speaker(name=s,num_features=nFeatures)
    user.enroll(final_ubm,enrollment_files[s])
    print("Time taken to enroll speaker {}: {}".format(s,toc()))
    

