import tkinter as tk
import tkinter.font as tkFont
import threading, clipboard, os, re
from configparser import ConfigParser
from Completer import *
from audioConverter import*
#import vlc, time, gTTS
class GUI(threading.Thread):
    def button_click(self, buttonNum, eye = 0, trigger=False):#TODO change eye=0

        if  trigger == True:
            for i in range(9):
                self.button[i].configure(bg= self.orig_color)

            self.button[buttonNum].configure(bg= "yellow")
            return
        else:
            for i in range(9):
                self.button[i].configure(bg= self.orig_color)

        if self.btn_str[4].get() == "Ready to Begin":
            texttospeech("Ready to Begin")
            predictedWords = genericWords(6)
            self.btn_str[4].set(
                predictedWords[0] + "\t" + predictedWords[1] + "\t" + predictedWords[2] + "\t" + predictedWords[
                    3] + "\t" + predictedWords[4] + "\t" + predictedWords[5] + "\n>")
            return
        if buttonNum == 4:
            self.middleButton_click()
            return

        userStr = self.btn_str[4].get()[self.btn_str[4].get().rfind(">") + 1:]  # gets just the user string
        print("\nbutton_click(btnNum= " + str(buttonNum) + " ,windowposition=" + str(self.windowPosition))
        print("str:\"" + userStr + "\"")

        #train the predictor
        prevWord=""
        lastWord=""
        whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        str_sentence = ''.join(filter(whitelist.__contains__, userStr))

        if str_sentence[-1:] == " ":
            str_sentence = str_sentence[:-1]
            secondLastSpace = str_sentence[:-1].rfind(" ")
            lastWord=str_sentence[secondLastSpace + 1:]
            if str_sentence[secondLastSpace] == " ":
                str_sentence = str_sentence[0:secondLastSpace]
                secondLastSpace = str_sentence[:-1].rfind(" ")
                prevWord=str_sentence[secondLastSpace + 1:]
                self.predictor.addWordSuggestion(prevWord,lastWord)
        else:
            wordIndex = str_sentence[:-1].rfind(" ")
            if wordIndex > 0:
                str_sentence = str_sentence[wordIndex + 1:]
                #find the incompete word typed

        #if showing letters
        if self.windowPosition == 1:  # char window
            if self.parser.getint('settings', 'eyeMode') == 1:  # one eye
                userStr = userStr + self.btn_str[buttonNum].get()
                if len(userStr) != 0:
                    singleletter = userStr[len(userStr) - 1]
                    texttospeech(singleletter)
                predictedWords =genericWords(7)
                letters = genericLetters(7)
                if userStr != "" and userStr.rfind(" ") < 0:
                    predictedWords = self.predictor.predict(userStr, 8)
                    letters = sorted(self.predictor.predictNextLetter(userStr, 8))
                elif userStr.rfind(" ") == len(userStr) - 1:
                    print("")
                else:
                    predictedWords = self.predictor.predict(userStr[userStr.rfind(" ") + 1:], 8)
                    letters = sorted(self.predictor.predictNextLetter(userStr[userStr.rfind(" ") + 1:], 8))

                middleBox = ""
                if predictedWords ==None:
                    middleBox = ">" + userStr
                else:
                    for i in range(len(predictedWords)):
                        middleBox = middleBox + predictedWords[i] + "\t"
                    middleBox = middleBox[:-1] + "\n>" + userStr

                box = [letters[0], letters[1], letters[2], letters[3], middleBox, letters[4], letters[5], letters[6],
                       letters[7]]
                for i in range(9):
                    self.btn_str[i].set(box[i])
            elif eye < 0:  # two eyes, left closed

                userStr = userStr + self.btn_str[buttonNum].get()[:self.btn_str[buttonNum].get().index(" | ")+1]

                predictedWords = genericWords(7)
                letters = genericLetters(15)
                if userStr != "" and userStr.rfind(" ") < 0:
                    predictedWords = self.predictor.predict(userStr, 8)
                    letters = sorted(self.predictor.predictNextLetter(userStr, 16))
                elif userStr.rfind(" ") == len(userStr) - 1:
                    print("")
                else:
                    predictedWords = self.predictor.predict(userStr[userStr.rfind(" ") + 1:], 8)
                    letters = sorted(self.predictor.predictNextLetter(userStr[userStr.rfind(" ") + 1:], 16))

                middleBox = ""
                if predictedWords == None:
                    middleBox = ">" + userStr
                else:
                    for i in range(len(predictedWords)):
                        middleBox = middleBox + predictedWords[i] + "\t"
                    middleBox = middleBox[:-2] + "\n>" + userStr
                box = [letters[0] + " | " + letters[1], letters[2] + " | " + letters[3],
                       letters[4] + " | " + letters[5], letters[6] + " | " + letters[7], middleBox,
                       letters[8] + " | " + letters[9], letters[10] + " | " + letters[11],
                       letters[12] + " | " + letters[13], letters[14] + " | " + letters[15]]
                for i in range(9):
                    self.btn_str[i].set(box[i])
            elif eye > 0:  # two eyes, right closed
                print("str1:\"" + userStr + "\"")
                userStr = userStr + self.btn_str[buttonNum].get()[self.btn_str[buttonNum].get().index(" | ") + 3:]
                print("str2:\"" + userStr + "\"")
                predictedWords = genericWords(7)
                letters = genericLetters(15)
                if userStr != "" and userStr.rfind(" ") < 0:
                    predictedWords = self.predictor.predict(userStr, 8)
                    letters = sorted(self.predictor.predictNextLetter(userStr, 16))
                elif userStr.rfind(" ") == len(userStr) - 1:
                    print("")
                else:
                    predictedWords = self.predictor.predict(userStr[userStr.rfind(" ") + 1:], 8)
                    letters = sorted(self.predictor.predictNextLetter(userStr[userStr.rfind(" ") + 1:], 16))

                middleBox = ""
                if predictedWords == None:
                    middleBox = ">" + userStr
                else:
                    for i in range(len(predictedWords)):
                        middleBox = middleBox + predictedWords[i] + "\t"

                middleBox = middleBox[:-2] + "\n>" + userStr  # + self.btn_str[buttonNum].get()[-1:]
                box = [letters[0] + " | " + letters[1], letters[2] + " | " + letters[3],
                       letters[4] + " | " + letters[5], letters[6] + " | " + letters[7], middleBox,
                       letters[8] + " | " + letters[9], letters[10] + " | " + letters[11],
                       letters[12] + " | " + letters[13], letters[14] + " | " + letters[15]]
                for i in range(9):
                    self.btn_str[i].set(box[i])
        elif self.windowPosition == 2:
            self.windowPosition = 1
            if self.parser.getint('settings', 'eyeMode') == 1:
                if userStr.rfind(" ")<0:
                    userStr= self.btn_str[buttonNum].get()+" "
                else:
                    userStr=userStr[0:userStr.rfind(" ")+1]+ self.btn_str[buttonNum].get()+" "
                if len(userStr) != 0:
                    texttospeech(self.btn_str[buttonNum].get())
                predictedWords = self.predictor.predictNextWord(str_sentence, 6)
                letters = genericLetters(7)
                middleBox = ""

                if predictedWords ==None:
                    middleBox = ">" + userStr
                else:
                    for i in range(len(predictedWords)):
                        middleBox = middleBox + predictedWords[i] + "\t"
                    middleBox = middleBox[:-2] + "\n>" + userStr

                box = [letters[0], letters[1], letters[2], letters[3], middleBox, letters[4], letters[5], letters[6],
                       letters[7]]

                for i in range(9):
                    self.btn_str[i].set(box[i])
            elif eye < 0:
                if userStr.rfind(" ") < 0:
                    if self.btn_str[buttonNum].get().rfind(" | ") < 0:  ##########################
                        print("gotya")
                        userStr = self.btn_str[buttonNum].get()[:] + " "
                    else:
                        userStr = self.btn_str[buttonNum].get()[:self.btn_str[buttonNum].get().index(" | ")] + " "
                else:
                    print("str0.5:\"" + userStr + "\"")
                    if self.btn_str[buttonNum].get().rfind(" ") > 0:
                        userStr = userStr[:userStr.rfind(" ") + 1] + self.btn_str[buttonNum].get()[:self.btn_str[buttonNum].get().rfind(" | ")] + " "
                    else:
                        userStr = userStr[:userStr.rfind(" ") + 1] + self.btn_str[buttonNum].get() + " "
                print("str1.5:\"" + userStr + "\"")
                predictedWords = self.predictor.predict(str_sentence,6)
                letters = sorted(self.predictor.predictNextLetter(str_sentence,14))
                middleBox = ""
                if predictedWords ==None:
                    middleBox = ">" + userStr
                else:
                    for i in range(7):
                        middleBox = middleBox + predictedWords[i] + "\t"
                    middleBox = middleBox[:-2] + "\n>" + userStr
                box = [letters[0] + " | " + letters[1], letters[2] + " | " + letters[3],
                       letters[4] + " | " + letters[5], letters[6] + " | " + letters[7], middleBox,
                       letters[6] + " | " + letters[7], letters[8] + " | " + letters[9],
                       letters[10] + " | " + letters[11], letters[12] + " | " + letters[13]]
                for i in range(9):
                    self.btn_str[i].set(box[i])
            elif eye > 0:
                if userStr.rfind(" ")<0:
                    if self.btn_str[buttonNum].get().rfind(" | ") < 0:##########################
                        print("gotya")
                        userStr = self.btn_str[buttonNum].get()[:] + " "
                    else:
                        userStr= self.btn_str[buttonNum].get()[self.btn_str[buttonNum].get().index(" | ") + 3:] + " "
                else:
                    print("str0.5:\"" + userStr + "\"")
                    if self.btn_str[buttonNum].get().rfind(" ")>0:
                        userStr = userStr[:userStr.rfind(" ")+1]+ self.btn_str[buttonNum].get()[self.btn_str[buttonNum].get().rfind(" | ") + 3:] + " "
                    else:
                        userStr = userStr[:userStr.rfind(" ") + 1] + self.btn_str[buttonNum].get() + " "

                print("str2:\"" + userStr + "\"")
                predictedWords = self.predictor.predict(str_sentence,6)
                letters = sorted(self.predictor.predictNextLetter(str_sentence,14))
                middleBox = ""
                if predictedWords == None:
                    middleBox = ">" + userStr
                else:
                    for i in range(len(predictedWords)):
                        middleBox = middleBox + predictedWords[i] + "\t"
                    middleBox = middleBox[:-2] + "\n>" + userStr
                box = [letters[0] + " | " + letters[1], letters[2] + " | " + letters[3],
                       letters[4] + " | " + letters[5], letters[6] + " | " + letters[7], middleBox,
                       letters[6] + " | " + letters[7], letters[8] + " | " + letters[9],
                       letters[10] + " | " + letters[11], letters[12] + " | " + letters[13]]
                for i in range(9):
                    self.btn_str[i].set(box[i])
            return
        elif self.windowPosition == 3:
            if buttonNum == 0:
                userStr=userStr+" "
                self.btn_str[4].set(">"+userStr)
                if len(userStr) != 0:
                    texttospeech("Space")
            elif buttonNum == 1:
                userStr = userStr[:-1]
                self.btn_str[4].set(">" + userStr)
                if len(userStr) != 0:
                    texttospeech("BackSpace")
            elif buttonNum == 2:
                clipboard.copy(userStr)
                self.middleButton_click()
                if len(userStr) != 0:
                    texttospeech("COPY")
            elif buttonNum == 3:#TODO text-to-speech
                #mp2file = gTTS(text=usrStr, lang='en', slow=False)
                #mp3file.save("./textToSpeech.mp3")

                #sound = vlc.MediaPlayer("textToSpeech.mp3")
                #sound.play()

                #time.sleep(10)
                self.middleButton_click()
            elif buttonNum == 4:
                self.windowPosition = 5
                texttospeech("Middle Button Press")
                self.middleButton_click()
            elif buttonNum == 5 and self.parser.getint('settings', 'eyeMode')==1:
                if len(userStr) != 0:
                    texttospeech("Extras")
                self.windowPosition=1
                self.btn_str[0].set(".")
                self.btn_str[1].set(",")
                self.btn_str[2].set("?")
                self.btn_str[3].set("!")
                self.btn_str[4].set(">" + self.btn_str[4].get()[self.btn_str[4].get().index(">") + 1:])
                self.btn_str[5].set("@")
                self.btn_str[6].set("$")
                self.btn_str[7].set("+")
                self.btn_str[8].set("=")
            elif buttonNum == 5:
                self.btn_str[0].set(". | ,")
                self.btn_str[1].set("? | !")
                self.btn_str[2].set("@ | $")
                self.btn_str[3].set("+ | =")
                self.btn_str[4].set(">" + self.btn_str[4].get()[self.btn_str[4].get().index(">") + 1:])
                self.btn_str[5].set("/ | \"")
                self.btn_str[6].set("\\ | ;")
                self.btn_str[7].set(": | '")
                self.btn_str[8].set("( | )")
            elif buttonNum == 6:#TODO A-Z remaining
                if len(userStr) != 0:
                    texttospeech("A to Z")
                if self.parser.getint('settings', 'eyeMode')==1:
                    letters = genericLetters(7)
                    if userStr != "" and userStr.rfind(" ") < 0:
                        predictedWords = self.predictor.predict(userStr, 8)
                        letters = sorted(self.predictor.predictNextLetter(userStr, 8))
                    alphabet = "abcdefghijklmnopqrstuvwxyz"
                    predictedLetters=list(alphabet[len(letters):])

                    self.windowPosition += 1
                    self.btn_str[0].set(predictedLetters[0])
                    self.btn_str[1].set(predictedLetters[1])
                    self.btn_str[2].set(predictedLetters[2])
                    self.btn_str[3].set(predictedLetters[3])
                    self.btn_str[4].set(">" + self.btn_str[4].get()[self.btn_str[4].get().index(">") + 1:])
                    self.btn_str[5].set(predictedLetters[4])
                    self.btn_str[6].set(predictedLetters[5])
                    self.btn_str[7].set(predictedLetters[6])
                    self.btn_str[8].set(predictedLetters[7])

                else:
                    letters = genericLetters(15)
                    if userStr != "" and userStr.rfind(" ") < 0:
                        predictedWords = self.predictor.predict(userStr, 8)
                        letters = sorted(self.predictor.predictNextLetter(userStr, 16))
                    alphabet = "abcdefghijklmnopqrstuvwxyz"
                    predictedLetters = list(alphabet[len(letters):])

                    self.windowPosition += 1

                    self.btn_str[0].set(predictedLetters[0])
                    self.btn_str[1].set(predictedLetters[1])
                    self.btn_str[2].set(predictedLetters[2])
                    self.btn_str[3].set(predictedLetters[3])
                    self.btn_str[4].set(">" + self.btn_str[4].get()[self.btn_str[4].get().index(">") + 1:])
                    self.btn_str[5].set(predictedLetters[4])
                    self.btn_str[6].set(predictedLetters[5])
                    self.btn_str[7].set(predictedLetters[6])
                    self.btn_str[8].set(predictedLetters[7])

            elif buttonNum == 7 and self.parser.getint('settings', 'eyeMode')==1:
                if len(userStr) != 0:
                    texttospeech("zero to four")
                self.windowPosition = 1
                self.btn_str[0].set("0")
                self.btn_str[1].set("1")
                self.btn_str[2].set("2")
                self.btn_str[3].set("3")
                self.btn_str[4].set(">" + self.btn_str[4].get()[self.btn_str[4].get().index(">") + 1:])
                self.btn_str[5].set("4")
                self.btn_str[6].set("")
                self.btn_str[7].set("")
                self.btn_str[8].set("")
            elif buttonNum == 7:
                self.windowPosition = 1
                self.btn_str[0].set("0 | 1")
                self.btn_str[1].set("2 | 3")
                self.btn_str[2].set("4 | 5")
                self.btn_str[3].set("6 | 7")
                self.btn_str[4].set(">" + self.btn_str[4].get()[self.btn_str[4].get().index(">") + 1:])
                self.btn_str[5].set("8 | 9")
                self.btn_str[6].set("")
                self.btn_str[7].set("")
                self.btn_str[8].set("")
            elif buttonNum == 8 and self.parser.getint('settings', 'eyeMode')==1:
                if len(userStr) != 0:
                    texttospeech("five to nine")
                self.windowPosition = 1
                self.btn_str[0].set("5")
                self.btn_str[1].set("6")
                self.btn_str[2].set("7")
                self.btn_str[3].set("8")
                self.btn_str[4].set(">" + self.btn_str[4].get()[self.btn_str[4].get().index(">") + 1:])
                self.btn_str[5].set("9")
                self.btn_str[6].set("")
                self.btn_str[7].set("")
                self.btn_str[8].set("")
            elif buttonNum == 8:
                self.windowPosition = 4
                self.middleButton_click()


        elif self.windowPosition == 4:
            if self.parser.getint('settings', 'eyeMode') == 1:
                self.btn_str[4].set(self.btn_str[4].get()+self.btn_str[buttonNum].get())
            elif eye<0:
                self.btn_str[4].set(self.btn_str[4].get() + self.btn_str[buttonNum].get())
            else:
                self.btn_str[4].set(self.btn_str[4].get() + self.btn_str[buttonNum].get())
            self.windowPosition = 1
            self.middleButton_click()
        return

    def middleButton_click(self, skip = False):
        texttospeech("Middle Button")
        print("MIDDLE BUTTON")
        if self.windowPosition >= 3 and skip == False:
            print("MIDDLE BUTTON RESET")
            self.windowPosition = 1
        elif skip == False:
            self.windowPosition =self.windowPosition + 1
        userStr = self.btn_str[4].get()[self.btn_str[4].get().rfind(">") + 1:]  # gets just the user string

        if self.windowPosition == 1:
            if self.parser.getint('settings', 'eyeMode') == 1:  # one word per button
                predictedWords = genericWords(7)
                letters = genericLetters(7)
                if userStr != "" and userStr.rfind(" ") < 0:
                    predictedWords = self.predictor.predict(userStr, 8)
                    letters = sorted(self.predictor.predictNextLetter(userStr, 8))
                elif userStr.rfind(" ") == len(userStr) - 1:
                    print("")
                else:
                    predictedWords = self.predictor.predict(userStr[userStr.rfind(" ") + 1:], 8)
                    letters = sorted(self.predictor.predictNextLetter(userStr[userStr.rfind(" ") + 1:], 8))

                middleBox = ""
                if predictedWords ==None:
                    middleBox = ">" + userStr
                else:
                    for i in range(len(predictedWords)):
                        middleBox = middleBox + predictedWords[i] + "\t"
                    middleBox = middleBox[:-2] + "\n>" + self.btn_str[4].get()[self.btn_str[4].get().rfind(">") + 1:]

                box = [letters[0], letters[1], letters[2], letters[3], middleBox, letters[4], letters[5], letters[6],
                       letters[7]]
                for i in range(9):
                    self.btn_str[i].set(box[i])
            else:  # two words per button####################################################################################
                predictedWords = genericWords(7)
                letters = genericLetters(15)
                if userStr != "" and userStr.rfind(" ") < 0:
                    predictedWords = self.predictor.predict(userStr, 8)
                    letters = sorted(self.predictor.predictNextLetter(userStr, 16))
                elif userStr.rfind(" ") == len(userStr) - 1:
                    print("")
                else:
                    predictedWords = self.predictor.predict(userStr[userStr.rfind(" ") + 1:], 8)
                    letters = sorted(self.predictor.predictNextLetter(userStr[userStr.rfind(" ") + 1:], 16))

                middleBox = ""
                if predictedWords ==None:
                    middleBox = ">" + userStr
                else:
                    for i in range(len(predictedWords)):
                        middleBox = middleBox + predictedWords[i] + "\t"
                    middleBox = middleBox[:-2] + "\n>" + self.btn_str[4].get()[self.btn_str[4].get().rfind(">") + 1:]

                box = [letters[0] + " | " + letters[1], letters[2] + " | " + letters[3],
                       letters[4] + " | " + letters[5], letters[6] + " | " + letters[7], middleBox,
                       letters[8] + " | " + letters[9], letters[10] + " | " + letters[11],
                       letters[12] + " | " + letters[13], letters[14] + " | " + letters[15]]
                for i in range(9):
                    self.btn_str[i].set(box[i])
        elif self.windowPosition == 2:

            if self.parser.getint('settings', 'eyeMode') == 1:  # one word per button

                predictedWords = genericWords(7)
                if userStr != "" and userStr.rfind(" ") < 0:
                    predictedWords = self.predictor.predict(userStr, 8)
                elif userStr.rfind(" ") == len(userStr) - 1:
                    print("")
                else:
                    predictedWords = self.predictor.predict(userStr[userStr.rfind(" ") + 1:], 8)

                if predictedWords==None:
                    box = ["", "", "", "","Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>" + userStr, "","", "", ""]
                elif len(predictedWords) >= 8:
                    box = [predictedWords[0], predictedWords[1], predictedWords[2], predictedWords[3], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           predictedWords[4], predictedWords[5], predictedWords[6], predictedWords[7]]
                elif len(predictedWords) == 7:
                    box = [predictedWords[0], predictedWords[1], predictedWords[2], predictedWords[3], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           predictedWords[4], predictedWords[5], predictedWords[6], ""]
                elif len(predictedWords) == 6:
                    box = [predictedWords[0], predictedWords[1], predictedWords[2], predictedWords[3], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           predictedWords[4], predictedWords[5], "", ""]
                elif len(predictedWords) == 5:
                    box = [predictedWords[0], predictedWords[1], predictedWords[2], predictedWords[3], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           predictedWords[4], "", "", ""]
                elif len(predictedWords) == 4:
                    box = [predictedWords[0], predictedWords[1], predictedWords[2], predictedWords[3], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr, "",
                           "", "", ""]
                elif len(predictedWords) == 3:
                    box = [predictedWords[0], predictedWords[1], predictedWords[2], "", "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr, "", "", "", ""]
                elif len(predictedWords) == 2:
                    box = [predictedWords[0], predictedWords[1], "", "", "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr, "", "", "", ""]
                elif len(predictedWords) == 1:
                    box = [predictedWords[0], "", "", "", "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr, "", "", "", ""]
                else:
                    box = ["", "", "", "", "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr, "", "", "", ""]
                for i in range(9):
                    self.btn_str[i].set(box[i])
            else:  # two words per button
                predictedWords = genericWords(15)
                if userStr != "" and userStr.rfind(" ") < 0:
                    predictedWords = self.predictor.predict(userStr, 15)
                elif userStr.rfind(" ") == len(userStr) - 1:
                    print("")
                else:
                    predictedWords = self.predictor.predict(userStr[userStr.rfind(" ") + 1:], 15)
                box=["", "", "", "","Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>" + self.btn_str[4].get()[self.btn_str[4].get().rfind(">") + 1:] + userStr, "","", "", ""]

                if predictedWords==None:
                    box = ["", "", "", "","Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>" + self.btn_str[4].get()[self.btn_str[4].get().rfind(">") + 1:] + userStr, "","", "", ""]
                elif len(predictedWords) >= 16:
                    box = [predictedWords[0]+" | "+predictedWords[1],predictedWords[2]+" | "+predictedWords[3], predictedWords[4]+" | "+predictedWords[5], predictedWords[6]+" | "+predictedWords[7], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           predictedWords[8]+" | "+predictedWords[9], predictedWords[10]+" | "+predictedWords[11], predictedWords[12]+" | "+predictedWords[13], predictedWords[14]+" | "+predictedWords[15]]
                elif len(predictedWords) == 15:
                    box = [predictedWords[0]+" | "+predictedWords[1],predictedWords[2]+" | "+predictedWords[3], predictedWords[4]+" | "+predictedWords[5], predictedWords[6]+" | "+predictedWords[7], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           predictedWords[8]+" | "+predictedWords[9], predictedWords[10]+" | "+predictedWords[11], predictedWords[12]+" | "+predictedWords[13], predictedWords[14]]
                elif len(predictedWords) == 14:
                    box = [predictedWords[0]+" | "+predictedWords[1],predictedWords[2]+" | "+predictedWords[3], predictedWords[4]+" | "+predictedWords[5], predictedWords[6]+" | "+predictedWords[7], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           predictedWords[8]+" | "+predictedWords[9], predictedWords[10]+" | "+predictedWords[11], predictedWords[12], predictedWords[13]]
                elif len(predictedWords) == 13:
                    box = [predictedWords[0]+" | "+predictedWords[1],predictedWords[2]+" | "+predictedWords[3], predictedWords[4]+" | "+predictedWords[5], predictedWords[6]+" | "+predictedWords[7], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           predictedWords[8]+" | "+predictedWords[9], predictedWords[10], predictedWords[11], predictedWords[12]]
                elif len(predictedWords) == 12:
                    box = [predictedWords[0]+" | "+predictedWords[1],predictedWords[2]+" | "+predictedWords[3], predictedWords[4]+" | "+predictedWords[5], predictedWords[6]+" | "+predictedWords[7], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           predictedWords[8], predictedWords[9], predictedWords[10], predictedWords[11]]
                elif len(predictedWords) == 11:
                    box = [predictedWords[0]+" | "+predictedWords[1],predictedWords[2]+" | "+predictedWords[3], predictedWords[4]+" | "+predictedWords[5], predictedWords[6], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           predictedWords[7], predictedWords[8], predictedWords[9], predictedWords[10]]
                elif len(predictedWords) == 10:
                    box = [predictedWords[0]+" | "+predictedWords[1],predictedWords[2]+" | "+predictedWords[3], predictedWords[4], predictedWords[5], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           predictedWords[6], predictedWords[7], predictedWords[8], predictedWords[9]]
                elif len(predictedWords) == 9:
                    box = [predictedWords[0]+" | "+predictedWords[1],predictedWords[2], predictedWords[3], predictedWords[4], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           predictedWords[5], predictedWords[6], predictedWords[7], predictedWords[8]]
                elif len(predictedWords) == 8:
                    box = [predictedWords[0],predictedWords[1], predictedWords[2], predictedWords[3], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           predictedWords[4], predictedWords[5], predictedWords[6], predictedWords[7]]
                elif len(predictedWords) == 7:
                    box = [predictedWords[0],predictedWords[1], predictedWords[2], predictedWords[3], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           predictedWords[4], predictedWords[5], predictedWords[6], ""]
                elif len(predictedWords) == 6:
                    box = [predictedWords[0],predictedWords[1], predictedWords[2], predictedWords[3], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           predictedWords[4], predictedWords[5], "", ""]
                elif len(predictedWords) == 5:
                    box = [predictedWords[0],predictedWords[1], predictedWords[2], predictedWords[3], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           predictedWords[4], "", "",""]
                elif len(predictedWords) == 4:
                    box = [predictedWords[0],predictedWords[1], predictedWords[2], predictedWords[3], "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           "","","",""]
                elif len(predictedWords) == 3:
                    box = [predictedWords[0]+" | "+predictedWords[1],predictedWords[2], "", "", "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           "","","",""]
                elif len(predictedWords) == 2:
                    box = [predictedWords[0],predictedWords[1], "", "", "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           "","","",""]
                elif len(predictedWords) == 1:
                    box = [predictedWords[0],"", "", "", "Space\tA-Z(remaining)\t0-9\t.,?!@$+=\t\tBackspace\tCopy\tText-to-Speech\n>"+userStr,
                           "", "", "", ""]
                for i in range(9):
                    self.btn_str[i].set(box[i])

        elif self.windowPosition == 3:
            if self.parser.getint('settings', 'eyeMode') == 1:  # one word per button
                self.btn_str[0].set("Space")
                self.btn_str[1].set("Backspace")
                self.btn_str[2].set("Copy text")
                self.btn_str[3].set("Text-to-Speech")
                self.btn_str[4].set(">" + self.btn_str[4].get()[self.btn_str[4].get().index(">") + 1:])
                self.btn_str[5].set(".,?!@$+=")
                self.btn_str[6].set("A-Z(remaining)")
                self.btn_str[7].set("0-4")
                self.btn_str[8].set("5-9")
            else:
                self.btn_str[0].set("Space")
                self.btn_str[1].set("Backspace")
                self.btn_str[2].set("Copy text")
                self.btn_str[3].set("Text-to-Speech")
                self.btn_str[4].set(">" + self.btn_str[4].get()[self.btn_str[4].get().index(">") + 1:])
                self.btn_str[5].set(".,?!@$+=/\"\\;:'( )")
                self.btn_str[6].set("A-Z(remaining)")
                self.btn_str[7].set("0-9")
                self.btn_str[8].set("")
        return


    def cameraCalabrationUpdate(self, message):
        msg = "Calibrating you camera! \n\nPlease look "
        if message == "U":
            msg = msg + "up."
        elif message == "D":
            msg = msg + "down."
        elif message == "R":
            msg = msg + "to your right."
        elif message == "L":
            msg = msg + "to your left."
        elif message == "DONE":
            letters = sorted(genericLetters(15))
            letters = [letters[0] + " | " + letters[1], letters[2] + " | " + letters[3],
                       letters[4] + " | " + letters[5], letters[6] + " | " + letters[7], "Ready to Begin",
                       letters[6] + " | " + letters[7], letters[8] + " | " + letters[9],
                       letters[10] + " | " + letters[11], letters[12] + " | " + letters[13]]
            for i in range(9):
                self.btn_str[i].set(letters[i])
            return
        self.btn_str[4].set(msg)


    def callback(self):
        self.root.quit()

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def changeModeSettings(self):
        if self.parser.getint('settings', 'eyeMode') == 1:
            self.parser.set('settings', 'eyeMode', '2')
            texttospeech("Change to fast mode")
        else:
            self.parser.set('settings', 'eyeMode', '1')
            texttospeech("Change to slow mode")
        self.parser.write(open('./eyeTrackingKeyboard_settings.ini', 'w'))

        self.windowPosition=4
        self.middleButton_click()

    def fontDecrease(self):
        self.parser.set('settings', 'Font', str(self.parser.getint('settings', 'Font') - 4))
        self.parser.write(open('./eyeTrackingKeyboard_settings.ini', 'w'))

        self.myFont = tkFont.Font(size=self.parser.getint('settings', 'Font'))
        self.button[0]['font'] = self.myFont
        self.button[1]['font'] = self.myFont
        self.button[2]['font'] = self.myFont
        self.button[3]['font'] = self.myFont
        self.button[4]['font'] = self.myFont
        self.button[5]['font'] = self.myFont
        self.button[6]['font'] = self.myFont
        self.button[7]['font'] = self.myFont
        self.button[8]['font'] = self.myFont

    def deleteHistory(self):
        texttospeech("History Deleted")
        os.remove("./wordBak.txt")
        os.remove("./sentenceBak.txt")
        #self.predictor=self.predictor()

    def fontIncrease(self):
        texttospeech("Font Increased")
        self.parser.set('settings', 'Font', str(self.parser.getint('settings', 'Font') + 4))
        self.parser.write(open('./eyeTrackingKeyboard_settings.ini', 'w'))

        self.myFont = tkFont.Font(size=self.parser.getint('settings', 'Font'))
        self.button[0]['font'] = self.myFont
        self.button[1]['font'] = self.myFont
        self.button[2]['font'] = self.myFont
        self.button[3]['font'] = self.myFont
        self.button[4]['font'] = self.myFont
        self.button[5]['font'] = self.myFont
        self.button[6]['font'] = self.myFont
        self.button[7]['font'] = self.myFont
        self.button[8]['font'] = self.myFont

    def run(self, calabrationMSG = ""):
        self.predictor = Completer()
        self.predictor.loadDictionary("dict.txt")

        self.parser = ConfigParser()
        self.parser.read("./eyeTrackingKeyboard_settings.ini")

        self.windowPosition = 1
        self.root = tk.Tk()
        self.btn_str = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(),
                        tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.button = [9]
        self.lastWord = ""
        self.root.title("ELEC 490: Eye Tracking Keybaord")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.geometry("%dx%d+0+0"%(600,300))
        #self.root.winfo_screenwidth(),self.root.winfo_screenheight()#fullscreen

        menubar=tk.Menu(self.root)
        filemenu=tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Increase font",command=self.fontIncrease)
        filemenu.add_command(label="Decrease font",command=( self.fontDecrease))
        filemenu.add_command(label="Enable fast mode (2 words/button)", command=(self.changeModeSettings))
        filemenu.add_command(label="Delete word prediction history", command=(self.deleteHistory))#TODO
        filemenu.add_command(label="Exit",command=( self.root.quit))
        menubar.add_cascade(label="Preferences",menu=filemenu)
        self.root.config(menu=menubar)
        # Create & Configure frame/grid
        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=1)
        frame = tk.Frame(self.root)

        frame.grid(row=0, column=0, sticky='NSEW')

        self.button = [tk.Button(frame, textvariable=self.btn_str[0], command=lambda: self.button_click(0)),
                  tk.Button(frame, textvariable=self.btn_str[1], command=lambda: self.button_click(1)),
                  tk.Button(frame, textvariable=self.btn_str[2], command=lambda: self.button_click(2)),
                  tk.Button(frame, textvariable=self.btn_str[3], command=lambda: self.button_click(3)),
                  tk.Button(frame, textvariable=self.btn_str[4],wraplength=400, command=lambda: self.button_click(4)),
                  tk.Button(frame, textvariable=self.btn_str[5], command=lambda: self.button_click(5)),
                  tk.Button(frame, textvariable=self.btn_str[6], command=lambda: self.button_click(6)),
                  tk.Button(frame, textvariable=self.btn_str[7], command=lambda: self.button_click(7)),
                  tk.Button(frame, textvariable=self.btn_str[8], command=lambda: self.button_click(8))]
        self.orig_color=self.button[0].cget("background")
        self.myFont = tkFont.Font(size=self.parser.getint('settings', 'Font'))

        self.button[0]['font']=self.myFont
        self.button[1]['font'] = self.myFont
        self.button[2]['font'] = self.myFont
        self.button[3]['font'] = self.myFont
        self.button[4]['font'] = self.myFont
        self.button[5]['font']=self.myFont
        self.button[6]['font'] = self.myFont
        self.button[7]['font'] = self.myFont
        self.button[8]['font'] = self.myFont

        # Button Grid
        tk.Grid.rowconfigure(frame, 0, weight=1)
        tk.Grid.columnconfigure(frame, 0, weight=1)
        self.button[0].grid(row=0, column=0, sticky='NSEW')
        tk.Grid.rowconfigure(frame, 0, weight=1)
        tk.Grid.columnconfigure(frame, 1, weight=1)
        self.button[1].grid(row=0, column=1, columnspan=2, sticky='NSEW')
        tk.Grid.rowconfigure(frame, 0, weight=1)
        tk.Grid.columnconfigure(frame, 3, weight=1)
        self.button[2].grid(row=0, column=3, sticky='NSEW')

        tk.Grid.rowconfigure(frame, 1, weight=1)
        tk.Grid.columnconfigure(frame, 0, weight=1)
        self.button[3].grid(row=1, column=0, rowspan=2, sticky='NSEW')
        tk.Grid.rowconfigure(frame, 1, weight=1)
        tk.Grid.columnconfigure(frame, 1, weight=1)
        self.button[4].grid(row=1, column=1, columnspan=2, rowspan=2, sticky='NSEW')
        tk.Grid.rowconfigure(frame, 1, weight=1)
        tk.Grid.columnconfigure(frame, 3, weight=1)
        self.button[5].grid(row=1, column=3, rowspan=2, sticky='NSEW')

        tk.Grid.rowconfigure(frame, 3, weight=1)
        tk.Grid.columnconfigure(frame, 0, weight=1)
        self.button[6].grid(row=3, column=0, sticky='NSEW')
        tk.Grid.rowconfigure(frame, 2, weight=1)
        tk.Grid.columnconfigure(frame, 2, weight=1)
        self.button[7].grid(row=3, column=1, columnspan=2, sticky='NSEW')
        tk.Grid.rowconfigure(frame, 3, weight=1)
        tk.Grid.columnconfigure(frame, 3, weight=1)
        self.button[8].grid(row=3, column=3, sticky='NSEW')

        self.btn_str[0].set("a")
        if calabrationMSG != "":
            self.btn_str[4].set("Calibrating you camera! \n\nPlease look up.")
        else:
            if self.parser.getint('settings', 'eyeMode') == 1:  # one word per button
                letters = sorted(genericLetters(7))
                letters = [letters[0], letters[1], letters[2], letters[3], "Ready to Begin", letters[4], letters[5],
                           letters[6], letters[7]]
                for i in range(9):
                    self.btn_str[i].set(letters[i])
            else:  # two words per button
                if calabrationMSG == "":
                    letters = sorted(genericLetters(15))
                    letters = [letters[0] + " | " + letters[1], letters[2] + " | " + letters[3],
                               letters[4] + " | " + letters[5], letters[6] + " | " + letters[7], "Ready to Begin",
                               letters[6] + " | " + letters[7], letters[8] + " | " + letters[9],
                               letters[10] + " | " + letters[11], letters[12] + " | " + letters[13]]
                    for i in range(9):
                        self.btn_str[i].set(letters[i])

        self.root.mainloop()

