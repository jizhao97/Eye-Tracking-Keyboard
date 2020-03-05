# Completer Include it and create a

import sys
from itertools import groupby

class Completer:

    def __init__(self):
        try:
            dictionary = open("wordBak.txt", "r")
        except:
            print("No word Backup Found!\nCreating New One")
            dictionary = open("wordBak.txt", "w")
        try:
            sentenceDictionary = open("sentenceBak.txt", "r")
        except:
            print("No sentence Backup Found!\nCreating New One")
            sentenceDictionary = open("sentenceBak.txt", "w")

        markov = {'a': {}}
        self.Markov = markov
        sentenceMarkov = {'a': {}}
        self.SentenceMarkov = sentenceMarkov

        if dictionary.readable():
            dictionary.seek(0)
            f1 = dictionary.read()
            f1 = f1.rsplit("\n")

            for line in f1:
                val = line.split("=")
                if val.__len__() == 3:
                    if val[0] in self.Markov.keys():
                        self.Markov[val[0]][val[1]] = int(val[2])
                    else:
                        self.Markov[val[0]] = {val[1]: int(val[2])}

        dictionary.close()

        if sentenceDictionary.readable():
            sentenceDictionary.seek(0)
            f1 = sentenceDictionary.read()
            f1 = f1.rsplit("\n")

            for line in f1:
                val = line.split("=")
                if val.__len__() == 3:
                    if val[0] in self.SentenceMarkov.keys():
                        self.SentenceMarkov[val[0]][val[1]] = int(val[2])
                    else:
                        self.SentenceMarkov[val[0]] = {val[1]: int(val[2])}
        sentenceDictionary.close()

    def update(self):
        file = open("wordBak.txt", "w")

        for key in self.Markov.keys():
            for word, value in self.Markov[key].items():
                file.write(key + "=" + word + "=" + str(value) + "\n")
        file.close()

        file = open("sentenceBak.txt", "w")

        for word in self.SentenceMarkov.keys():
            for nextWord, value in self.SentenceMarkov[word].items():
                file.write(word + "=" + nextWord + "=" + str(value) + "\n")
        file.close()

    def addEntry(self, word):  # used to enter word in the dictionary beware it will modify the dictionary file also
        for i, character in enumerate(word):
            key = ''
            for j in range(i + 1):
                key = key + word.__getitem__(j)
            if key in self.Markov.keys():
                self.Markov[key][word] = 0
            else:
                self.Markov[key] = {}

    def addWordSuggestion(self, word, wordToSuggest):
        if word in self.SentenceMarkov.keys():
            if wordToSuggest in self.SentenceMarkov[word].keys():
                print("", end = '')
            else:
                self.SentenceMarkov[word][wordToSuggest] = 0
        else:
            self.SentenceMarkov[word] = {wordToSuggest: 0}

    def loadDictionary(self, file):
        try:
            dictionary = open(file, "r")
        except:
            sys.stderr.write("File Access Failed '%s'.\n" % file)
            sys.exit(1)

        dictionary.seek(0)
        f1 = dictionary.read()
        f1 = f1.rsplit("\n")
        for word in f1:
            self.addEntry(word)
            self.addWordSuggestion(word, "")
        self.update()
        dictionary.close

    def predict(self, toComplete, suggestionCount):  # used to predict word
        if toComplete in self.Markov.keys():
            result = []
            count = 0
            for word, value in sorted(self.Markov[toComplete].items(), key=lambda item: item[1], reverse=True):
                result.append(word)
                count += 1
                if count >= suggestionCount:
                    return result
            return result
        else:
            return

    def predictNextWord(self, currentWord, suggestionCount):
        if currentWord in self.SentenceMarkov.keys():
            result = []
            count = 0
            for word, value in sorted(self.SentenceMarkov[currentWord].items(), key=lambda item: item[1], reverse=True):
                result.append(word)
                count += 1
                if count >= suggestionCount:
                    return result
            return result
        else:
            return

    def increasePriority(self, key, word):
        if key in self.Markov.keys():
            if word in self.Markov[key].keys():
                self.Markov[key][word] += 1
            else:
                print("Invalid Word Supplied")
        else:
            print("Invalid Key Supplied")

    def increaseWordSuggestionPriority(self, word, wordToSuggest):
        if word in self.SentenceMarkov.keys():
            if wordToSuggest in self.SentenceMarkov[word].keys():
                self.SentenceMarkov[word][wordToSuggest] += 1
            else:
                print("Invalid Suggestion Word Supplied")
        else:
            print("Invalid Word Supplied")

    def predictNextLetter(self, toComplete1, suggestionCount):  # used to predict word
        resultfinal = []
        result1 = ["e", "t", "a", "i", "n", "o", "s", "h", "r", "d", "l", "u", "c", "m", "f", "w", "y", "g", "p", "b",
               "v", "k", "q", "j", "x", "z"]
        if toComplete1 in self.Markov.keys():
            results = []
            finalresult = []
            count = 0
            count1=0
            result1 = ["e", "t", "a", "i", "n", "o", "s", "h", "r", "d", "l", "u", "c", "m", "f", "w", "y", "g", "p", "b",
               "v", "k", "q", "j", "x", "z"]
            for word, value in sorted(self.Markov[toComplete1].items(), key=lambda item: item[1], reverse=True):
                wordLength = len(toComplete1)
                if wordLength < len(word) and word[wordLength] not in results:
                    results.append(word[wordLength])
                    count += 1
                if count >= suggestionCount:
                    return results
            i = 0
            j = 0
            k = 0
            while (i < 1):
                if len(results) <=  suggestionCount:
                    if result1[j] not in results:
                        results.append(result1[j])
                    j+=1
                else:
                    break
            if len(results) == 0:
                for k in range(0,suggestionCount):
                    results.append(result1[k])
                    
            return results

        else:
            for k in range(0,suggestionCount):
                    resultfinal.append(result1[k])
            return resultfinal

def genericLetters( count):
    result1 = ["e", "t", "a", "i", "n", "o", "s", "h", "r", "d", "l", "u", "c", "m", "f", "w", "y", "g", "p", "b",
               "v", "k", "q", "j", "x", "z"]
    answer = []
    countKey = 0
    while (countKey <= count):
        answer.append(result1[countKey])
        countKey += 1
    return answer

def genericWords( count):
    result1 = ["I", "He", "She", "You", "It", "Hello", "They", "My", "Yours", "Theirs","Too","To","My","His","Her"]
    answer = []
    countKey = 0
    while (countKey <= count - 1):
        answer.append(result1[countKey])
        countKey += 1
    return answer
