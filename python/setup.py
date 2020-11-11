from ubm_model import UBM
import os

digits = ['0','1','2','3','4','5','6','7','8','9']

def train_Model(training_file_location,ubm_location):

    voice_commands_files = sortUBMData(training_file_location)

    ubm_model = UBM(num_coef = 128)
    ubm_model.loadtrainingfeatures(voice_commands_files)
    ubm_model.trainDigitUBM()
    ubm_model.save(ubm_location)

def sortUBMData(training_file_location):

    common_voice = training_file_location

    common_voice_speakers ={}

    #get speakers with > 5 utterances
    for f in digits:
        file = os.path.join(common_voice,f)
        recordings = os.listdir(file)
        speakers = []
        for r in recordings:
            s = r.split("_")                     
            if(int(s[2][0])==4):
                speakers.append(s[0])
        common_voice_speakers[f] = speakers
        
    voice_commands_files ={}
    i = 0
    for f in digits:
        file = os.path.join(common_voice,f)
        recordings = os.listdir(file)
        train = []
        n = int(len(common_voice_speakers[f])*0.1)
        
        for r in [x for x in os.listdir(file) if x.endswith('.wav')][:-1]:
            s = r.split("_")
            s = s[0]
        
            if s in common_voice_speakers[f][0:-1]:
                x= os.path.join(file,r)
                train.append(x)
        voice_commands_files[f] = train
        i+=1
    return voice_commands_files




if __name__ == "__main__":

    