# Import the required module for text  
# to speech conversion - using google's API
# and playing back the audio

from gtts import gTTS 
from playsound import playsound
from pathlib import Path
import shutil
import os
import time



SAVE = False
def texttospeech(string1):
    fmt = '.mp3'
        # Language in which you want to convert
    language = 'en'
        # Passing the text and language to the engine,
        # here we have marked slow=False. Which tells
        # the module that the converted audio should
        # have a high speed
    string = string1
    myobj = gTTS(text=string, lang=language, slow=False)
    filename = string + ".mp3"
    directory = "C:/490 final/AudioFolder"
    finalnet=os.path.join(directory, filename)
    if os.path.exists(finalnet) == 0:
        myobj.save(finalnet)
    playsound(finalnet)
    #os.remove(filenet)
    time.sleep(1)
#if __name__ == "__main__":
    #texttospeech()
