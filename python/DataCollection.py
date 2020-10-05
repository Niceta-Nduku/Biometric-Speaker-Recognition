import Record as r
import say_numbers_prompt as prompter
import sys
import time
import os
import Validate
from enroll import enroll

# digit prompter
SECONDS = 30
DATA_FOLDER = "data/"
ALL_DIGITS = "digits"


if (len(sys.argv) > 1):
    print ("Hello "+sys.argv[1])
else:
    print("Invalid input")

Speaker_id = sys.argv[1]

speaker_folder = Speaker_id+"/"
folderToSave = DATA_FOLDER+speaker_folder+ALL_DIGITS

if not os.path.isdir(folderToSave):
    print("Directory "+folderToSave+" does not exist")
    exit()

print("\n\nYou will be given 10 numbers(0-9) repeated 5 times in random order.\n\n"
    "Read the numbers with yout normal speaking voice but with a very short break between numbers")

new_speaker = enroll.enroll(Speaker_id)

new_speaker.record(folderToSave)

print("Thank you.\n\n You will now be prompted with a 6 digit string.")

ready = input("\npress s to start\n")

while(ready != 's'):
    ready = input("press s to start\n")




