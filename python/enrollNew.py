import Speaker
from ubm_model import UBM
import os
import pwd


def enroll(user,UBM_location,enrollment_files,user_model_location,alter_speakers):
    #if UBM no in location, system is not set up run set up
    #if ubm is in location 
    ubm_model = UBM(num_coef = 128)
    ubm_model.load(UBM_location)
    user = Speaker.speaker(name=user,num_features=13)

    #check if enrollment files are present
    user.enroll(ubm_model,enrollment_files,)


if __name__ == "__main__":

    username = pwd.getpwuid(os.getuid())[0]
    path = "/lib/x86_64-linux-gnu/security/"
    user_model_location = path + username
    UBM_location = ""

    #run record for enrollment
    #
    #enroll(username,UBM_location,enrollment_files,user_model_location)
    #delete enrollment recordings