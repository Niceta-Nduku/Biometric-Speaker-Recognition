import pyaudio
import wave
from scipy.io import wavfile

class Recorder(object):

    def __init__(self, CHUNK = 1024, FORMAT = pyaudio.paInt16, CHANNELS = 1, RATE = 16000):
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

    def start(self,RECORD_SECONDS = 5, wait_to_stop = False, playback = False, WAVE_OUTPUT_FILENAME = "output.wav"):
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
            self.save(WAVE_OUTPUT_FILENAME)
            self.play()
            
        self.stop()
        self.save(WAVE_OUTPUT_FILENAME)

    def save(self,output_file):
        wf = wave.open(output_file, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def play(self,WAVE_INPUT_FILENAME = "output.wav"):
        """
            Play audio
        Args:
            WAVE_INPUT_FILENAME (str, optional): [description]. Defaults to "output.wav".
        """
        print("Playing back..")
        wf = wave.open(WAVE_INPUT_FILENAME, 'rb')
        data = wf.readframes(self.CHUNK)

        while len(data) > 0:
            self.stream.write(data)
            data = wf.readframes(self.CHUNK)

    def stop(self):
        """
        Stop recording
        """
        print("Stopping..")
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
    

if __name__ == "__main__":


    recorder = Recorder()
    fileToSave = input("Enter file to save to:\n")
    seconds = input("enter seconds: ")
    ready = input("press s to start\n")

    while(ready != 's'):
        ready = input("press s to start\n")

    recorder.start(RECORD_SECONDS=int(seconds),playback=True,WAVE_OUTPUT_FILENAME=fileToSave)
    


