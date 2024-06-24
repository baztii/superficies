######################### COMPACTE I CONNEX ###########################################


class WORD:
    def __init__(self, word : str):
        self.word = word
        self.length = len(word)

    def __str__(self):
        return self.word

    def reverseWord(self, start : int = -1, end : int = -1): # the word is reversed
        if start == -1: start = 0
        if end == -1: end = self.length-1

        self.word = self.word[:start] + self.word[end:start-1:-1] + self.word[end+1:]
    
    def oppositeChar(self, c : str) -> str: # returns the opposite of a letter
        return c.upper() if c.islower() else c.lower()
    
    def replaceChar(self, oldC : str, newC : str): # replaces the character oldC with newC to the word
        self.word = self.word.replace(oldC, newC)
        self.word = self.word.replace(self.oppositeChar(oldC), self.oppositeChar(newC))
    
    def insertPair(self, c1 : str, c2 : str, pos : int): # inserts two consecutive characters to the word
        self.word = self.word[:pos] + c1 + c2 + self.word[pos:]
        self.length += 2
    
    def erasePair(self, c1 : str, c2 : str): # erase two consecutives characters from the word
        pos1 = self.word.find(c1)
        pos2 = self.word.rfind(c2)

        if pos1 == -1 or pos2 == -1 or (pos1+1 != pos2 and pos1-1 != pos2):
            return
        
        if pos1 < pos2:
            self.word = self.word[:pos1] + self.word[pos1+1:pos2] + self.word[pos2+1:]
        else:
            self.word = self.word[:pos2] + self.word[pos2+1:pos1] + self.word[pos1+1:]
        
        self.length -= 2
            
    def setWord(self, word : str): # the word is the value of word
        self.word = word
        self.length = len(word)

    def invertPos(self, where): # a character or a position of the word is inverted 
        w = self.word[where] if type(where) == int else where
        idxMaj = self.word.find(w.upper())
        idxMin = self.word.find(w.lower())

        if idxMaj == -1 or idxMin == -1:
           self.word = self.word.replace(w,self.oppositeChar(w))
        else:
            self.word = self.word[:idxMaj] + w.lower() + self.word[idxMaj+1:]
            self.word = self.word[:idxMin] + w.upper() + self.word[idxMin+1:]

    def invertWord(self, start : int = -1, end : int = -1): # the word[start..end] or all the word is inverted

        if start == -1: start = 0
        if end == -1: end = self.length-1

        for i in range(start, end+1):
            self.word = self.word[:i] + self.oppositeChar(self.word[i]) + self.word[i+1:]

    def cycleWord(self, step : int): # cycles the word the number of steps clockwise
        step %= self.length
        self.word = self.word[step:] + self.word[:step]

class SCHEMA:
    def __init__(self, wordSet : list[str]):
        self.wordSet = []
        self.alphabetMin = [chr(i) for i in range(ord('a'), ord('z')+1)]
        self.alphabetMaj = [chr(i) for i in range(ord('A'), ord('Z')+1)]
        self.usages = {}

        for w in self.alphabetMin:
            self.usages[w] = 0

        for w in self.alphabetMaj:
            self.usages[w] = 0

        for s in wordSet:
            self.wordSet.append(WORD(s))
            for w in s:
                self.usages[w] += 1
    
    def __str__(self):
        s = '['
        for word in self.wordSet:
            s = s + word.word + ', '
        
        s = s[:-2]
        s += ']'
        return s

    def oppositeChar(self, c : str) -> str: # returns the opposite of a letter
        return c.upper() if c.islower() else c.lower()

    def validSchema(self) -> bool: # returns if the schema is valid
        for c in self.usages:
            if self.usages[c] not in {0,2}: return False

        for w in self.wordSet:
            if len(w.word) < 2: return False

        return True
    
    def compact(self): # erases the empty words
        i = 0
        while i < len(self.wordSet):
            if len(self.wordSet[i].word) == 0: del self.wordSet[i]
            else: i+=1
        
        if len(self.wordSet) == 0:
            self.wordSet = [WORD("")]

    def cut(self, idx : int, pos : int): # cuts a word from the schema
        c = ''
        for c in self.alphabetMin:
            if self.usages[c] == 0 and self.usages[self.oppositeChar(c)] == 0: break
        
        self.usages[c] = 1
        self.usages[self.oppositeChar(c)] = 1
        
        w = self.wordSet[idx]

        w1 = WORD(w.word[:pos] + c)
        w2 = WORD(self.oppositeChar(c) + w.word[pos:])

        del self.wordSet[idx]

        self.wordSet.append(w1)
        self.wordSet.append(w2)

    def paste(self, idx1 : int, idx2 :int): # pastes two words from the schema
        w1 = self.wordSet[idx1].word
        w2 = self.wordSet[idx2].word

        if w1[-1] != self.oppositeChar(w2[0]): return

        self.usages[w1[-1]] -= 1
        self.usages[w2[0]] -= 1

        w = WORD(w1[:-1] + w2[1:])

        if idx1 < idx2:
            del self.wordSet[idx2]
            del self.wordSet[idx1]
        else:
            del self.wordSet[idx1]
            del self.wordSet[idx2]

        self.wordSet.append(w)

    def relabel(self, oldC : str, newC : str): # relables the instances of oldC with newC
        self.usages[newC], self.usages[self.oppositeChar(newC)] = self.usages[oldC], self.usages[self.oppositeChar(oldC)]
        self.usages[oldC], self.usages[self.oppositeChar(oldC)] = 0,0

        for idx in range(len(self.wordSet)):
            self.wordSet[idx].replaceChar(oldC, newC)

    def reorient(self, c : str): # changes all the occurences of c with opposite(c)
        self.usages[c], self.usages[self.oppositeChar(c)] = self.usages[self.oppositeChar(c)], self.usages[c]

        for idx in range(len(self.wordSet)):
            self.wordSet[idx].invertPos(c)

    def permute(self, idx : int, step : int): # permutes a word w = w1:w2 to w = w2:w1 where len(w1) = step
        self.wordSet[idx].cycleWord(step)

    def invert(self, idx : int, start : int = -1, end : int = -1): # w = a1..an -> w = An..A1
        self.wordSet[idx].reverseWord(start,end)
        for c in self.wordSet[idx].word[start:end+1]:
            self.usages[c] -= 1
            self.usages[self.oppositeChar(c)] += 1

        self.wordSet[idx].invertWord(start, end)

    def erase(self, idx : int, c : str): # changes the word w = w1.a.A.w2 to w = w1.w2  
        self.usages[c] = self.usages[self.oppositeChar(c)] = 0
        self.wordSet[idx].erasePair(c, self.oppositeChar(c))

    def clean(self): # cleans the schema
        for idx, word in enumerate(self.wordSet):
            i = 0
            while i+1 < len(word.word):
                if word.word[i] == self.oppositeChar(word.word[i+1]):
                    self.erase(idx,word.word[i])
                    i -= 1
                    if i < 0: i = 0
                else:
                    i += 1

        self.compact()

    def insert(self, idx : int, c : str, pos : int): # inverse operation of erase (c not used)
        self.usages[c] = 1
        self.usages[self.oppositeChar(c)] = 1

        self.wordSet[idx].insertPair(c, self.oppositeChar(c), pos)

    def fusion(self): # the schema becomes a one-word schema (important connexion!)
        if (len(self.wordSet) < 2): return

        c = ''
        i = 0
        word = self.wordSet[0]
        for i, c in enumerate(word.word):
            if word.word.count(c) + word.word.count(self.oppositeChar(c)) != 2:
                break
        
        idx = 0
        for idx, w in enumerate(self.wordSet[1:]):
            if w.word.count(c) != 0 or w.word.count(self.oppositeChar(c)) != 0:
                break
        else: return

        idx += 1

        j = self.wordSet[idx].word.find(c)

        if j != -1:
            self.permute(0,i)
            self.permute(idx,j)
            self.invert(0)
            self.paste(0,idx)
            return
        
        j = self.wordSet[idx].word.find(self.oppositeChar(c))

        self.permute(0,-len(self.wordSet[0].word)+i+1)
        self.permute(idx, j)
        self.paste(0,idx)

        self.fusion()

    def connexSum(self, i : int, j : int):
        self.wordSet[i].setWord(self.wordSet[i].word + self.wordSet[j].word)
        del self.wordSet[j]

    def proj(self) -> int: # identification of all the projective parts (kP²)
        k = 0
        i = j = 0
        while i < len(self.wordSet[0].word):
            j = i+1
            while j < len(self.wordSet[0].word):
                if self.wordSet[0].word[i] == self.wordSet[0].word[j]:
                    k += 1
                    self.invert(0,i+1,j-1)
                    self.wordSet[0].word = self.wordSet[0].word[i] + self.wordSet[0].word[j] + self.wordSet[0].word[:i] + self.wordSet[0].word[i+1:j] + self.wordSet[0].word[j+1:]
                    i += 1
                    j = i
                j+=1
            i+=1

        self.clean()

        return k

    def torus(self, start : int) -> int: # identifaction of all the torus parts (nT²)

        if start == len(self.wordSet[0].word):
            return 0

        iMin = 0
        jMin = len(self.wordSet[0].word)

        for i in range(start,len(self.wordSet[0].word)):
            for j in range(i+1, len(self.wordSet[0].word)):
                if self.wordSet[0].word[i] == self.oppositeChar(self.wordSet[0].word[j]):
                    if j - i < jMin - iMin:
                        iMin, jMin = i, j
        
        k = int((iMin + jMin)/2)
        l = 0

        for inc in range(1,len(self.wordSet[0].word)):
            if iMin-inc >= 0 and self.wordSet[0].word[iMin-inc] == self.oppositeChar(self.wordSet[0].word[k]):
                l = iMin-inc
                break
            
            if jMin+inc < len(self.wordSet[0].word) and self.wordSet[0].word[jMin+inc] == self.oppositeChar(self.wordSet[0].word[k]):
                l = jMin+inc
                break

        w = self.wordSet[0].word

        if l > jMin:
            y1 = w[start:iMin]
            y2 = w[iMin+1:k]
            y3 = w[k+1:jMin]
            y4 = w[jMin+1:l]
            y5 = w[l+1:]
            self.wordSet[0].word = w[:start] + w[iMin] + w[k] + w[jMin] + w[l] + y1 + y4 + y3 + y2 + y5
        
        else:
            y1 = w[start:l]
            y2 = w[l+1:iMin]
            y3 = w[iMin+1:k]
            y4 = w[k+1:jMin]
            y5 = w[jMin+1:]
            self.wordSet[0].word = w[:start] + w[l] + w[iMin] + w[k] + w[jMin] + y1 + y4 + y3 + y2 + y5

        self.clean()

        return 1 + self.torus(start+4)
        
    def solve(self): # the schema becomes the fundamental one // Cal veure que passa amb l'usage
        self.clean()
        self.fusion()

        k = self.proj()
        n = self.torus(2*k)

        print(self)

        if k == 0 and n == 0:
            print(f"La superfície descrita és una esfera")
        elif k != 0:
            print(f"La superfície descrita són {k+2*n} plans projectius")
        else:
            print(f"La superfície descrita són {n} tors")
            
def main():
    s1 = SCHEMA(["abcdabcdeeffghgihi"])
    s2 = SCHEMA(["abABcdCDee"])
    s3 = SCHEMA(["abcabc"])
    s4 = SCHEMA(["abcdcAbD"])  
    s5 = SCHEMA(["abbcAddC"])
    s6 = SCHEMA(["abcdACBD"])
    s7 = SCHEMA(["abABcdCD"])
    s8 = SCHEMA(["abcadBefcEdF"])
    s1.solve()
    s2.solve()
    s3.solve()
    s4.solve()
    s5.solve()
    s6.solve()
    s7.solve()
    s8.solve()

def gameloop():
    pass

if __name__ == "__main__":
    main()



