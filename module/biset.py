
from module.paraInterface import *
import json
import random

class biset(paraInterface):
    def __init__(self):
        self.MWU = json.load(open('tmp/idiom.json', 'r', encoding='UTF8'))
        self.keys = [key for key in self.MWU]

    def synonymIfExists(self, sentence):
        words = []
        for (word, t) in self.tag(sentence):
            if self.paraphraseable(t) and word not in ["i","I"]:
                # print(word)
                words.append(word)
        
        return words

    def useBiset(self, sentence):
        synonym = self.synonymIfExists(sentence)
        wordlist = []
        for word in self.keys:
            for syn in synonym:
                if word == syn:
                    wordlist.append(sentence.replace(word, self.MWU[word]))
                    
        random.shuffle(wordlist)

        return wordlist[:5]


    # def bisetData(self, sentence):
    #     synonym = self.synonymIfExists(sentence)
    #     length = len(synonym)
    #     if length > 0:
    #         words = "'%%" + synonym[0] + "%%'"
    #         if length > 1:
    #             for i in range(1,length):
    #                 words += " and meaning like "
    #                 words += "'%%" + synonym[i] + "%%'"

    #         sql     = "select sentence from TS.idiom where meaning like " + words

    #         data = self.db.executeAll(sql)
    #         self.db.commit()

    #         if data:
    #             words = []
    #             for i in data:
    #                 words.append(i['sentence'].replace('\xa0', ' '))

    #             return words
    #         else:
    #             return []
    #     else:
    #         return []

# run Flask app
if __name__ == "__main__":
    translate = biset()
    # translate.bisetData("Every man has a knack for rolling.")


