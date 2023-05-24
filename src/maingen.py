# Author: Answer03 

import cv2 
import numpy as np
import random
from music21 import *

class musicpiece(object):
    def __init__(self):
        self.val=0

def reproduction(a,b):
    ret=musicpiece()
    ret.pcs=np.append(a.pcs[0:16],b.pcs[16:32])
    ret.pcs = [val % 27 for val in ret.pcs]
    ret.dely=np.append(a.dely[0:16],b.pcs[16:32])

    prob=random.random()
    if prob<=0.05:
        pos=random.randint(0,31)
        ret.pcs[pos]=random.randint(0,26)
        ret.dely[pos] = random.randint(0,1)
    prob = random.random()

    s = stream.Stream()
    for pc, dely in zip(ret.pcs, ret.dely):
        n = note.Note()
        n.pitch.midi = pc + 53  
        n.duration.quarterLength = 0.25 
        s.append(n)

    start_pos = random.randint(0, len(s.notes) - 4)
    end_pos = start_pos + 4
    melody_fragment = s.notes[start_pos:end_pos]

    transformation = random.choice(["transpose", "reflect"])

    fragment_notes = [note_obj for note_obj in melody_fragment]

    if transformation == "transpose":
        transpose_amount = random.randint(-5, 5) 
        transformed_fragment = []
        for note_obj in fragment_notes:
            transposed_note = note_obj
            transposed_note.pitch.midi += transpose_amount
            transformed_fragment.append(transposed_note)
    elif transformation == "reflect":
        transformed_fragment = fragment_notes[::-1]  

    transformed_s = s
    transformed_notes = list(transformed_s.notes.stream().elements)
    transformed_notes[start_pos:end_pos] = transformed_fragment
    transformed_s.notes.elements = tuple(transformed_notes)

    ret.pcs = [n.pitch.midi - 53 for n in transformed_s.notes]
    ret.dely = [1 if ret.pcs[i] == ret.pcs[i+1] else 0 for i in range(len(ret.pcs)-1)]


    return ret



harmy = [1.0,0.0,0.25,0.5,0.5,1.0,0.0,1.0,0.5,0.5,0.25,0.0]

def fitnes(piece1):
    cnt=0
    sum=0
    for i in range(31):
        if (piece1.pcs[i] != piece1.pcs[i+1]) or (piece1.dely[i]!=0):
            cnt=cnt+1
            dif=(piece1.pcs[i+1]-piece1.pcs[i]+36)%12
            sum=sum+1.0-harmy[dif]
    return sum/cnt

def cmp(pc1):
    return pc1.val

populrs = []
presumfit = []
sumfit=0
sumpopulrs=0

def randomselect():
    prob=random.random()*sumfit
    l=0
    r=sumpopulrs-1
    ans=0
    while l<=r:
        mid= (l+r)//2
        if prob <= presumfit[mid]:
            ans=mid
            r=mid-1
        else :
            l=mid+1
    return populrs[ans]


for i in range(100):
    prt1 = musicpiece()
    prt1.pcs=np.random.randint(0,high=27,size=32)
    prt1.dely=np.random.randint(0,high=2,size=32)
    prt1.val=fitnes(prt1)
    populrs.append(prt1)
    presumfit.append(0)
    sumpopulrs=sumpopulrs+1


Generations = 50
for tms in range(Generations):
    newpopulrs = []
    sumfit=0
    for i,va in enumerate(populrs):
        sumfit+= va.val
        if i==0:
            presumfit[i]=va.val
        else:
            presumfit[i]=presumfit[i-1]+va.val
    #print(presumfit)
    for i in range(100):
        father = randomselect()
        mother = randomselect()
        newanm = reproduction(father,mother)
        newanm.val=fitnes(newanm)
        newpopulrs.append(newanm)

    populrs = newpopulrs

for i,va in enumerate(populrs):
    print(va.val)
    print(va.pcs)
    print(va.dely)
