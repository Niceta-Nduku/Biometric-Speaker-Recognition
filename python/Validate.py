import random
import Record as r
import features as mfcc
import trimmer
import numpy as np
from scipy.io import wavfile
from hmmlearn.hmm import GMMHMM
import utils


def record(folderToSave, speaker_name, environment="s"):

    prompt = get_digit_string(6)
    print("Prompt: {}".format(prompt))
    ready = input("\npress s to start\n")

    while(ready != 's'):
        ready = input("press s to start\n")

    fileToSave = "{folder}/{prompt}_{speaker}_{env}.wav".format(
        prompt=prompt, speaker=speaker_name, folder=folderToSave, env=environment)
    # TODO: skip saving step
    recorder = r.Recorder()
    recorder.start(RECORD_SECONDS=10, playback=False,
                   WAVE_OUTPUT_FILENAME=fileToSave)


def extract_features(filename, prompt, numfeatures=13):

    sampling_rate, audio_signal = wavfile.read(filename)

    feat = mfcc.getMFCC(audio_signal, sampling_rate,
                        trimSilence=False, removeSilence=True, NUM_FEAT=13)

    return feat


def score(speaker_hmm, ubm_hmm, prompt_features):

    score = 0

    ubm_score = ubm_hmm.score(prompt_features)
    speaker_score = speaker_hmm.score(prompt_features)

    return score


def get_digit_string(length):
    digits = '0123456789'
    string = ''.join((random.choice(digits) for i in range(length)))
    return string


def generateHMM(model, prompt, n_states=6 ,gaussians=64):

    covars = []
    means = []
    weights = []

    for d in prompt:  # for each state
        # get speaker GMM for digit
        gmm = model[d]
        # covars mean append gmm covars
        covars.append(gmm.covariances_)
        means.append(gmm.means_)
        weights.append(gmm.weights)
    
    covars = np.array(covars)
    means = np.array(means)
    weights = np.array(weights)

    # initialise hmm with variables and transition matrix
    hmm_model = GMMHMM(n_states, gaussians, init_params="cm", params="cmt")
    hmm_model.startprob_ = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    hmm_modeltransmat_ = np.array([
        [0.5, 0.5, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.5, 0.5, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.5, 0.5, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.5, 0.5],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.5]])
    hmm_model.covars_ = covars
    hmm_model.means_ = means
    hmm_model.weights_ = weights

    return hmm_model
 