import time
import pickle
from ubm_model import UBM
import Speaker

#variables 
#variables 
num_coef = [32,64,128,256,512]
nFeatures = 13

_start = time.process_time()
def tic():
    global _start
    _start = time.process_time()

def toc():
    return time.process_time()-_start

#Files for testing

voice_commands_files = pickle.load(open("ubm_data.f","rb"))

#train UBM
for n in num_coef:
    ubm_model = UBM(num_coef = n)
    tic()
    ubm_model.loadtrainingfeatures(voice_commands_files)
    ubm_model.trainUBM()
    print("Time taken to train model if size {}: {}".format(n,toc()))
    final_ubm = ubm_model.getUBM()
    pickle.dump(final_ubm,open("UBM_{}".format(n),"wb"))
