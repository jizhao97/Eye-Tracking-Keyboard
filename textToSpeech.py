import vlc
import time
import gTTS

text = "Text to speech conversion"
mp2file = gTTS(text=text, lang='en', slow=False)
mp3file.save("textToSpeech.mp3")

sound = vlc.MediaPlayer("textToSpeech.mp3")
sound.play()

time.sleep(10)