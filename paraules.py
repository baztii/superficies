

class WORD:
    def __init__(self, word : str):
        self.word = word
        self.length = len(word)

    def validWord(self) -> bool: # returns if the word is valid
        for w in self.word:
            if self.word.count(w.lower()) + self.word.count(w.upper()) != 2:
                return False
        
        return True
    
    def reverseWord(self): # the word is reversed
        self.word = self.word[::-1]
    
    def oppositeChar(self, c : str) -> str: # returns the opposite of a letter
        return c.upper() if c.islower() else c.lower()
    
    def replaceChar(self, oldC : str, newC : str): # replaces the character oldC with newC to the word
        self.word.replace(oldC, newC)
        self.word.replace(self.opposite(oldC), self.opposite(newC))
    
    def insertPair(self, c1 : str, c2 : str, pos : int): # inserts two characters to the word
        self.word = self.word[:pos] + c1 + c2 + self.word[pos:]
        self.length += 2
    
    def erasePair(self, c1 : str, c2 : str): # errase two characters to the word
        pos1 = self.word.find(c1)
        pos2 = self.word.rfind(c2)

        if pos1 == -1 or pos2 == -1:
            return
        
        if pos1 < pos2:
            self.word = self.word[:pos1] + self.word[pos1+1:pos2] + self.word[pos2+1:]
        else:
            self.word = self.word[:pos2] + self.word[pos2+1:pos1] + self.word[pos1+1:]
            
    def setWord(self, word : str): # the word is the value of word
        self.word = word

    def invertPos(self, where): # a character or a position of the word is inverted 
        w = self.word[where] if type(where) == int else where
        idxMaj = self.word.find(w.upper())
        idxMin = self.word.find(w.lower())

        if idxMaj == -1 or idxMin == -1:
            self.word.replace(w,self.opposite(w))
        else:
            self.word[idxMaj] = w.lower()
            self.word[idxMin] = w.upper()
    
    def invertWord(self): # all the word is inverted
        for i in range(self.length):
            self.word[i] = self.oppositeChar(self.word[i])

    def cycleWord(self, step : int): # cycles the word the number of steps clockwise
        step %= self.length
        self.word = self.word[step:] + self.word[step::-1]

class SCHEMA:
    def __init__(self, wordSet : list[str]):
        self.wordSet = []
        for s in wordSet:
            self.wordSet.append(WORD(s))
    






def main():
    w = WORD("")

def gameloop():
    pass



if __name__ == "__main__":
    main()



