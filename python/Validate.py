import random
import Record as r
import features as mfcc
import trimmer
import numpy as np
from scipy.io import wavfile
from hmmlearn.hmm import GMMHMM
import utils

def extract_features(filename, prompt, numfeatures=13):

    sampling_rate, audio_signal = wavfile.read(filename)

    feat = mfcc.getMFCC(audio_signal, sampling_rate, single_phrase=False,
                        mutliple_phrases=True, NUM_FEAT=13, ENERGY=True, Delta=False)

    return feat


def score(speaker_model, ubm, prompt_features):

    ubm_score = ubm.score(prompt_features)
    speaker_score = speaker_model.score(prompt_features)
    
    llr = (speaker_score - ubm_score)

    return llr


def generateHMM(model, prompt, gaussians, n_states=6):

    covars = []
    means = []
    weights = []

    for d in prompt:  # for each state
        # get speaker GMM for digit
        gmm = model[d]
        # covars mean append gmm covars
        covars.append(gmm.covariances_)        
        means.append(gmm.means_)
        weights.append(gmm.weights_)

    covars = np.array(covars)
    means = np.array(means)
    weights = np.array(weights)

    # initialise hmm with variables and transition matrix
    hmm_model = GMMHMM(n_states, gaussians, init_params="cm", params="cmt")
    hmm_model.startprob_ = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    hmm_model.transmat_ = np.array([
        [0.5, 0.5, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.5, 0.5, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.5, 0.5, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.5, 0.5],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])
    hmm_model.covars_ = covars
    hmm_model.means_ = means
    hmm_model.weights_ = weights

    return hmm_model
