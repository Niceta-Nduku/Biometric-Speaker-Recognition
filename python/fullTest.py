import time
import pickle
from ubm_model import UBM
import Speaker

_start = time.process_time()
def tic():
    global _start
    _start = time.process_time()

def toc():
    return time.process_time()-_start

#Files for testing

collected_files = pickle.load(open("collected_enrollment_data.f","rb"))
free_spoken_files = pickle.load(open("free_speech_enrollment_data.f","rb"))
voice_commands_files = pickle.load(open("ubm_data.f","rb"))
collected_test_files = pickle.load(open("test_phrases.f","rb"))
noise_test_files = pickle.load(open("noisy_phrases.f","rb"))
imposter_test_files = pickle.load(open("imposter_phrases.f","rb"))

collected_Speakers = noise_test_files = ["Speaker1","Speaker2","Speaker3","Speaker4","Speaker5","Speaker6","Speaker7","Speaker8","Speaker9"]

speakers = collected_Speakers
enrollment_files = collected_files

#train UBM
ubm_model = UBM(num_coef = 64)
tic()
ubm_model.loadtrainingfeatures(voice_commands_files)
print("Time taken to train model {}".format(toc()))
final_ubm = ubm_model.getUBM()


# #enroll & verify speakers
# for s in speakers:
#     #new speaker
#     user = Speaker.speaker(name=s,num_features=nFeatures)
#     user.enroll(final_ubm,enrollment_files[s])


# #verify 


