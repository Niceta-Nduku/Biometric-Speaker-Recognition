
import numpy as np
from sklearn import preprocessing
from scipy.signal import butter, sosfilt, sosfreqz, medfilt
from scipy.spatial import distance
from python_speech_features import base, sigproc
import matplotlib.pyplot as plt

WINLEN = 0.025
WINSTEP = 0.01


def getMFCC(audio_signal, sample_rate, single_phrase=False, mutliple_phrases=False, NUM_FEAT=13, ENERGY=True, Delta=False, Filter=False):

    if(Filter):
        audio_signal = butter_bandpass_filter(
            audio_signal, 300, 3000, sample_rate, order=5)

    if (mutliple_phrases):
        audio_signal = power_vad(
            audio_signal, sample_rate, 20, 20, dev=2.1, mutliple_phrases=True)

    mfcc_features = base.mfcc(audio_signal, sample_rate, winlen=WINLEN,
                              winstep=WINSTEP, numcep=19, winfunc=np.hamming, appendEnergy=ENERGY)

    if (single_phrase):
        start, stop = mfcc_vad(mfcc_features, sample_rate,winlen = sample_rate*WINLEN,winstep = sample_rate*WINSTEP)

        mfcc_features = mfcc_features[start:stop]

    features = mfcc_features

    if Delta:
        delta_feat = base.delta(mfcc_features, 2)
        delta_delta_feat = base.delta(delta_feat, 2)

        features = [mfcc_features, delta_feat, delta_delta_feat]
        features = np.concatenate(features, axis=1)

    features = preprocessing.scale(mfcc_features)

    return features


def power_vad(audio_signal, samplerate, startframes=10, endframes=10, dev=3, single_phrase=False, mutliple_phrases=False):

    winlen = 0.025
    FFT = 512
    winfunc = np.hamming
    framelen = winlen*samplerate

    frames = sigproc.framesig(audio_signal, framelen, framelen, winfunc)
    numOfFrames, sizeOfFrame = frames.shape

    powerspec = sigproc.logpowspec(frames, FFT)
    energy = np.sum(powerspec, 1)
    energy = medfilt(energy, 11)

    first_samples = np.concatenate(
        (energy[:startframes], energy[-endframes:]), axis=None)
    mean = np.mean(first_samples)
    std = np.std(first_samples)
    indexes = np.array([])

    temp = []
    for i in range(len(energy)):
        d = (abs(energy[i] - mean))/std
        if(d > dev):
            if(len(indexes) == 0):
                indexes = [i]
            else:
                indexes = np.append(indexes, i)
        temp.append(d)

    if(single_phrase):
        start = int((indexes[0])*framelen)
        stop = int((indexes[-2])*framelen)
        print(indexes[-1])
        cleaned_signal = audio_signal[start:stop]
    elif(mutliple_phrases):
        cleaned_signal = sigproc.deframesig(
            frames[indexes[2:]], 0, framelen, framelen, winfunc)
    else:
        raise ValueError("Type of phrase not set")

    return cleaned_signal


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], analog=False, btype='band', output='sos')
    return sos


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    sos = butter_bandpass(lowcut, highcut, fs, order=order)
    y = sosfilt(sos, data)
    return y


def mfcc_vad(mfcc_features, sampling_rate,winlen,winstep):

    num_frames, num_feats = mfcc_features.shape

    fn = (0.5*sampling_rate - (winlen) + (winstep))/winstep

    mfcc_y = np.mean(mfcc_features[-int(fn):], axis=0)
    cos = []

    for i in range(num_frames):
        cos.append(1-distance.cosine(mfcc_features[i], mfcc_y))

    cos = np.array(cos, dtype='object')

    T = np.mean(cos[-int(fn):])
    m = np.argmin(cos)

    A = 0
    for i in range(m, 0, -1):
        if cos[i] > T:
            A = i
            break
    B = 0
    for j in range(m, len(cos)-1):
        if cos[j] > T:
            B = j
            break

    return A, B
