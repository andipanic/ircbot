#!/usr/bin/env python

import string, random
from time import clock
DICT = 'unixdict.txt'

def word_path(word,used=[],pos=None):
    if word:
        correct_neighbour = [neigh
                             for neigh in (neighbourlist[pos] if pos is not None else range(dimension*dimension))
                             if ((neigh not in used) and boggle[neigh]==word[0])]

        for i in correct_neighbour:
            used_copy=used[:]+[i]
            if len(word)==1:
                if boggle[i]==word:
                    return (used_copy,)
            else:
                for solution in  word_path(word[1:],used_copy,pos=i):
                    if solution:
                        return (solution,)
    return (False,)

neighbours=(
    (-1,-1),    (0,-1), (1,-1), ## left column
    (-1,0),             (1,0),  ## same column
    (-1,1),     (0,1),  (1,1)   ## next column
    )

wordlist=open(DICT).read().split()

boggle= ''.join(random.choice(string.ascii_lowercase) for _ in range(4 * 4)) ## CATXANTXTREEEBXY
dimension=int(len(boggle)**0.5)

for i in range(0,len(boggle)-dimension+1,dimension):
    print " ".join(boggle[i:i+dimension])

neighbour_indexpairs = set(((i,j), (i+di,j+dj))
                        for i in range(dimension)
                        for j in range(dimension)
                        for di,dj in neighbours if  0<=dj+j<dimension and 0<=di+i<dimension
                        )

# change to one dimension
neighbour_set=set((a*dimension+b,c*dimension+d) for (a,b),(c,d) in neighbour_indexpairs)

neighbourlist = [[] for _ in boggle]

[neighbourlist[char_index].append(b) for char_index,b in neighbour_set]

t0=clock()

letterpairs = set((boggle[a]+boggle[b]) for a,b in neighbour_set)

words = set(word for word in wordlist
     if (word.lower()==word and
         len(word)>dimension-2 and
         all((word[i]+word[i+1] in letterpairs) for i in range(len(word)-1))
         )
     )
print len(words),'candidates'
t1=clock()

result = [word for word in words
       for solution in word_path(word)
       if solution]
result.sort()
result.sort(key=len, reverse=True)
print "\nTotal", len(result),"solutions."
print "\nFound in %.3f ms" % (1000*(clock()-t0)),
print "of which final check took %.3f ms" % (1000*(clock()-t1))
print '\t'.join(result)

