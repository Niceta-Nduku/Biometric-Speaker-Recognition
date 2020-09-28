import pyaudio
import wave
from scipy.io import wavfile

class Recorder(object):

    def __init__(self, CHUNK = 1024, FORMAT = pyaudio.paInt16, CHANNELS = 2, RATE = 16000):
        """
        Initialize recorder

        Args:
            CHUNK (int, optional): [description]. Defaults to 1024.
            FORMAT ([type], optional): bits. Defaults to 16 (pyaudio.paInt16).
            CHANNELS (int, optional): number of channels. Defaults to 2.
            RATE (int, optional): sample rate. Defaults to 16000.
        """
        self.CHUNK = CHUNK
        self.FORMAT = FORMAT
        self.CHANNELS = CHANNELS
        self.RATE = RATE
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,output=True,frames_per_buffer=CHUNK)
        self.frames = []

    def start(self,RECORD_SECONDS = 5, wait_to_stop = False, playback = False):
        print("Recording...")

        if(wait_to_stop):
            while(True):
                data = self.stream.read(self.CHUNK)
                # self.stream.write(data)
                self.frames.append(data)

        else:
            for i in range(0, int(self.RATE / self.CHUNK * RECORD_SECONDS)):
                data = self.stream.read(self.CHUNK)
                self.frames.append(data)

        if(playback):
            self.save()
            self.play()
            
        self.stop()

        
    def stop(self):
        """
        Stop recording
        """
        print("Stopping..")
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


    def save(self,WAVE_OUTPUT_FILENAME = "output.wav"):
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def play(self,WAVE_INPUT_FILENAME = "output.wav"):
        print("Playing back..")
        wf = wave.open(WAVE_INPUT_FILENAME, 'rb')
        data = wf.readframes(self.CHUNK)

        while data != '':
            self.stream.write(data)
            data = wf.readframes(self.CHUNK)

        wf.close()
        self.stop()

if __name__ == "__main__":


    recorder = Recorder()

    ready = input("press s to start\n")

    while(not ready):
        continue

    recorder.start(playback=True)
    


