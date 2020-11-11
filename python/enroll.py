from scipy.io import wavfile
import features as mfcc
import sklearn.mixture as skm
import say_numbers_prompt as prompter
import Record as r
import utils
import numpy as np


def record(speaker_name,folderToSave):
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
        fileToSave = "{folder}/{digit}_{speaker}_{play}.wav".format(digit=i,play=x[i],speaker=speaker_name,folder=folderToSave)

        recorder.start(RECORD_SECONDS=5, playback=False,
                WAVE_OUTPUT_FILENAME=fileToSave)
        x[i] +=1
    #should return array of recordings
    
def getSpeakerFeatures(speaker_file,numfeatures = 13):
    
    speaker_features = {}
    
    length = len(speaker_file) #number of digits(words)

    for d in range(length):
        
        utterances = len(speaker_file[d])

        digit_features = []
        
        for i in range(utterances):
            
            sampling_rate, audio_signal = wavfile.read(speaker_file[d][i])
            feat = mfcc.getMFCC(audio_signal, sampling_rate, single_phrase=True, mutliple_phrases = False, NUM_FEAT=numfeatures, ENERGY = True , Delta = False)

            digit_features.append(feat)
            
        speaker_features[str(d)] = np.array(digit_features,dtype=object)
    return speaker_features   

def adapt_all_digits(ubm,speaker_features,ubm_type = 'd'):
    speaker_model ={}
    if ubm_type == 'd':
        for i in range(10):
            s_gmm = ubm[str(i)]
            for u in speaker_features[str(i)]:
                s_gmm = utils.map_adaptation(s_gmm, u, max_iterations = 10, likelihood_threshold = 1e-20, relevance_factor = 16)
            speaker_model[str(i)] = s_gmm
    else:
        s_gmm = ubm
        for i in range(10):            
            for u in speaker_features[str(i)]:
                s_gmm = utils.map_adaptation(s_gmm, u, max_iterations = 10, likelihood_threshold = 1e-20, relevance_factor = 16)
            speaker_model[str(i)] = s_gmm

    return speaker_model

def setThreshld():
    
    pass
