#!/usr/bin/env python

import string, random
DICT = 'unixdict.txt'

class Boggle:
    def __init__(self, size):
        self.size = size
        self.boggle = self.gen_boggle()
        self.neighbourlist = [[] for _ in self.boggle]
        self.board = self.boggle_board(self.boggle)
        self.answers = self.word_list(self.boggle)

    def gen_boggle(self):
        self.boggle= ''.join(random.choice(string.ascii_lowercase) for _ in range(self.size * self.size)) ## CATXANTXTREEEBXY
        return self.boggle

    def boggle_board(self, boggle):
        self.bog_board = ""
        for i in range(0,len(self.boggle)-self.size+1,self.size):
            self.bog_board += " ".join(self.boggle[i:i+self.size]) + "\n"
        return self.bog_board.strip()

    def word_path(self, word ,used=[],pos=None):
        if word:
            correct_neighbour = [neigh
                for neigh in (self.neighbourlist[pos] if pos is not None else range(self.size*self.size))
                if ((neigh not in used) and self.boggle[neigh]==word[0])]

            for i in correct_neighbour:
                used_copy=used[:]+[i]
                if len(word)==1:
                    if self.boggle[i]==word:
                        return (used_copy,)
                else:
                    for solution in  self.word_path(word[1:],used_copy,pos=i):
                        if solution:
                            return (solution,)
        return (False,)

    def word_list(self, boggle):
        wordlist=open(DICT).read().split()
        neighbours=(
                    (-1,-1),    (0,-1), (1,-1), ## left column
                    (-1,0),             (1,0),  ## same column
                    (-1,1),     (0,1),  (1,1)   ## next column
                    )

        neighbour_indexpairs = set(((i,j), (i+di,j+dj))
                        for i in range(self.size)
                        for j in range(self.size)
                        for di,dj in neighbours if  0<=dj+j<self.size and 0<=di+i<self.size
                        )

        neighbour_set=set((a*self.size+b,c*self.size+d) for (a,b),(c,d) in neighbour_indexpairs)
        [self.neighbourlist[char_index].append(b) for char_index,b in neighbour_set]

        letterpairs = set((self.boggle[a]+self.boggle[b]) for a,b in neighbour_set)

        words = set(word for word in wordlist
         if (word.lower()==word and
             len(word)>self.size-2 and
             all((word[i]+word[i+1] in letterpairs) for i in range(len(word)-1))
             )
         )
        return words


if __name__ == "__main__":
    bog = Boggle(4)
