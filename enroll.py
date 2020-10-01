import threading
import time
import getpass

class enroll():

    def __init__(self):
        self.name = "User"
        self.password = "admin"
        pass
    def setCredentials(self):
        self.name = input("Please enter name as \"LastName-FirtName\" with no spaces")
        if (len(name.split())>1):
            print("Please input name with no spaces")
            self.name = input("enter name as \"LastName-FirtName\" with no spaces")
        self.password = getpass.getpass(prompt='Enter secure password')

    def record(self):
        #release promp
        pass
    def adapt(self):
        pass
    def save(self):
        pass
        




