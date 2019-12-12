import json

class MWU():
    def __init__(self):
        self.MWU = json.load(open('tmp/MWU.json', 'r', encoding='UTF8'))
        self.keys = [key for key in self.MWU]

    def useMWU(self, sentence):
        wordlist = []
        for word in self.keys:
            if word in sentence:
                wordlist.append(sentence.replace(word, self.MWU[word]))
        
        return wordlist[:5]

    # def makeMWU(self):
    #     nonOverlapKey = []
    #     nonOverlapValue = []
    #     for word in self.keys:
    #         thisWord = self.MWU[word]
    #         Append = True
    #         find = 0
    #         if word == thisWord:
    #             print(word)
        #     for word2 in self.keys:
        #         if word2 == thisWord:
        #             print(word2)
        #             Append = False
        #             break
        #         elif thisWord == self.MWU[word2]:
        #             find += 1
        #             if find > 1:
        #                 Append = False
        #                 break
        #     if Append == True:
        #         nonOverlapKey.append(word)
        #         nonOverlapValue.append(thisWord)

        # for i in range(0, len(nonOverlapKey)-1):
        #     print('"'+nonOverlapValue[i]+'" : "'+nonOverlapKey[i]+'"  ,')
                
                


if __name__ == "__main__":
    w = MWU()
    # w.makeMWU()
    # print(w.useMWU("I want to get there as well."))