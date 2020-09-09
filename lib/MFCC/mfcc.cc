// -----------------------------------------------------------------------------
//  A simple MFCC extractor using C++ STL and C++11
// -----------------------------------------------------------------------------
//
//  Copyright (C) 2016 D S Pavan Kumar
//  dspavankumar [at] gmail [dot] com
//  Modified by Niceta Nduku September 2020
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <http://www.gnu.org/licenses/>.

#include "mfcc.h"

    MFCC::MFCC(int sampFreq = 16000, int nCep = 12, int winLength = 25, int frameShift = 10, int numFilt = 40, double lf = 50,
         double hf = 6500) {
        fs = sampFreq;             // Sampling frequency
        numCepstra = nCep;                 // Number of cepstra
        numFilters = numFilt;              // Number of Mel warped filters
        preEmphCoef = 0.97;                 // Pre-emphasis coefficient
        lowFreq = lf;                   // Filterbank low frequency cutoff in Hertz
        highFreq = hf;                   // Filterbank high frequency cutoff in Hertz
        numFFT = fs <= 20000 ? 512 : 2048;   // FFT size
        winLengthSamples = winLength * fs / 1e3;  // winLength in milliseconds
        frameShiftSamples = frameShift * fs / 1e3; // frameShift in milliseconds

        numFFTBins = numFFT / 2 + 1;
        powerSpectralCoef.assign(numFFTBins, 0);
        prevsamples.assign(winLengthSamples - frameShiftSamples, 0);

        initFilterbank();
        initHamDct();
        compTwiddle();
    }

    std::string MFCC::processFrame(int16_t *samples, size_t N) {
        // Add samples from the previous frame that overlap with the current frame
        // to the current samples and create the frame.
        frame = prevsamples;
        for (int i = 0; i < N; i++)
            frame.push_back(samples[i]);
        prevsamples.assign(frame.begin() + frameShiftSamples, frame.end());

        preEmphHam();
        computePowerSpec();
        applyLMFB();
        applyDct();

        return v_d_to_string(mfcc);
    }

    int MFCC::process(std::ifstream &wavFp, std::ofstream &mfcFp) {
        // Read the wav header    
        wavHeader hdr;
        int headerSize = sizeof(wavHeader);
        wavFp.read((char *) &hdr, headerSize);

        // Check audio format
        if (hdr.AudioFormat != 1 || hdr.bitsPerSample != 16) {
            std::cerr << "Unsupported audio format, use 16 bit PCM Wave" << std::endl;
            return 1;
        }
        // Check sampling rate
        if (hdr.SamplesPerSec != fs) {
            std::cerr << "Sampling rate mismatch: Found " << hdr.SamplesPerSec << " instead of " << fs << std::endl;
            return 1;
        }

        // Check sampling rate
        if (hdr.NumOfChan != 1) {
            std::cerr << hdr.NumOfChan << " channel files are unsupported. Use mono." << std::endl;
            return 1;
        }

        //remove silence


        // Initialise buffer
        uint16_t bufferLength = winLengthSamples - frameShiftSamples;
        int16_t *buffer = new int16_t[bufferLength];
        int bufferBPS = (sizeof buffer[0]);

        // Read and set the initial samples        
        wavFp.read((char *) buffer, bufferLength * bufferBPS);
        for (int i = 0; i < bufferLength; i++)
            prevsamples[i] = buffer[i];
        delete[] buffer;

        // Recalculate buffer size
        bufferLength = frameShiftSamples;
        buffer = new int16_t[bufferLength];

        // Read data and process each frame
        wavFp.read((char *) buffer, bufferLength * bufferBPS);
        while (wavFp.gcount() == bufferLength * bufferBPS && !wavFp.eof()) {
            mfcFp << processFrame(buffer, bufferLength);
            wavFp.read((char *) buffer, bufferLength * bufferBPS);
        }
        delete[] buffer;
        buffer = nullptr;
        return 0;
    }

