import sys
import time
import os
import Validate as ver
import enroll as en
import Record as r

# digit prompter
SECONDS = 30
DATA_FOLDER = "data/"
ALL_DIGITS = "digits"
PHRASES ="phrases"


if (len(sys.argv) > 1):
    print ("\nHello "+sys.argv[1])
else:
    print("Invalid input")

Speaker_id = sys.argv[1]

speaker_folder = Speaker_id+"/"
folderToSave = DATA_FOLDER+speaker_folder+ALL_DIGITS

if not os.path.isdir(folderToSave):
    print("Directory "+folderToSave+" does not exist")
    exit()

print("\n\nYou will be given 10 numbers(0-9) repeated 5 times in random order.\n\n"
    "Read the numbers with you2 normal speaking voice but with a very short break between numbers")

new_speaker = en.enroll(Speaker_id)

start = time.time()
new_speaker.record(folderToSave)
stop = time.time()

print("\n\nRecording took {seconds}".format(seconds=(stop-start)))


print("Thank you.\n\n You will now be prompted with random digit strings.")

folderToSave_prompt =  DATA_FOLDER+speaker_folder+PHRASES
promted = ver.Verify(Speaker_id)

start = time.time()
for i in range(5):
    
    ready = input("Recording for no noise {} \npress s to start\n".format(i))

    while(ready != 's'):
        ready = input("press s to start\n")

    promted.record(folderToSave_prompt, environment="s")


for i in range(4):
    
    ready = input("Recording for noisy environment {} \npress s to start\n".format(i))

    while(ready != 's'):
        ready = input("press s to start\n")

    promted.record(folderToSave_prompt,environment="n")

print("Starting imposter recordings")

prompts = ["173488","387038","593777"]
environment="im"

for prompt in prompts:
    print("Prompt: {}".format(prompt))
    ready = input("\npress s to start\n")

    while(ready != 's'):
        ready = input("press s to start\n")

    fileToSave = "{folder}/{prompt}_{speaker}_{env}.wav".format(prompt=prompt,speaker=Speaker_id,folder=folderToSave_prompt,env=environment)

    recorder = r.Recorder()
    recorder.start(RECORD_SECONDS=12, playback=False,
            WAVE_OUTPUT_FILENAME=fileToSave)



