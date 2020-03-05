
from eyeTrackingKeyboard import *
from Completer import *
#GUIobj = GUI("")
#main
m = Completer()#if the file exists it will load in memory otherwise create it
#m.addentry("chummendy")#adding an entry to dictionary
#m.loadDictionary("dict.txt")

m.increasePriority("c","cabinet")
m.increasePriority("c","center")
m.increasePriority("c","comments")
m.increasePriority("c","chummendy")

print(m.predict("c", 10))#getting a prediction

m.addWordSuggestion("i","am")
m.addWordSuggestion("am","chummendy")
m.increaseWordSuggestionPriority("i","am")
m.increaseWordSuggestionPriority("am","chummendy")
print(m.predictNextWord("i",10))
print(m.predictNextWord("am",10))
m.update()