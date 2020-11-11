import time
import pickle
from ubm_model import UBM
import Speaker

#variables 
num_coef = 64
nFeatures = 13

collected_test_files = pickle.load(open("test_phrases.f","rb"))
noise_test_files = pickle.load(open("noisy_phrases.f","rb"))
imposter_test_files = pickle.load(open("imposter_phrases.f","rb"))

collected_Speakers = ["Speaker1","Speaker2","Speaker3","Speaker4","Speaker5","Speaker6","Speaker7","Speaker8","Speaker9"]

speakers = collected_Speakers