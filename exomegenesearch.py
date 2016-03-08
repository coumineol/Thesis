#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Volkan
#
# Created:     23/11/2013
# Copyright:   (c) Volkan 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
from collections import Counter
import random
import numpy, scipy, matplotlib, sklearn

f = open("C:\\Users\\Volkan\\Desktop\\Msc\\Common\\allproteincodinggenes.txt")
lines = f.readlines()
listofgenes = []
for i in range(len(lines)):
    listofgenes.append(lines[i][:-1])
f.close()

#belli bir hastadaki bir varyantin detaylari
def readVariantFromSinglePatient():
    f = open("E:\\genomedata\\MAE16\\denovo_mild_queryresult_MAE16.tsv")
    lines = f.readlines()
    print(lines[26].split("\t"))
    f.close()

#belli bir hastalik grubundaki hastalarin snp iceren genleri bulup dosyaya yaz, bir hastada ayni gende birden fazla varsa bir kere say
def readGenesWithSnpFromMultiplePatients():
    g = open("C:\\Users\\Volkan\\Desktop\\Msc\\Sunum\\Exome sequencing\\Exome_server\\snpnlesexomegenes_denovo.txt", "w")
    filename = "E:\\genomedata\\"
    for i in range(1,50):
        print(i)
        filenamespecific = filename + "NLES" + str(i) + "\\denovo_mild_queryresult_nles" + str(i) + ".tsv"
        if os.path.isfile(filenamespecific):
            genesinthispatient = []
            f = open(filenamespecific)
            lines = f.readlines()
            for line in lines:
                splitline = line.split("\t")
                for gene in listofgenes:
                    if gene in splitline:
                        if splitline[3] == "snp":
                            genesinthispatient.append(gene)
            newsetgenesinthispatient = set(genesinthispatient)
            newlistgenesinthispatient = list(newsetgenesinthispatient)
            for gene in newlistgenesinthispatient:
                g.write(gene)
                g.write("\n")
            f.close()
    g.close()

def findDifferentialOccurence():
    h = open("C:\\Users\\Volkan\\Desktop\\Msc\\Sunum\\Exome sequencing\\Exome_server\\snpmaeexomegenes_denovo.txt")
    genes1 = h.readlines()
    h.close()
    h = open("C:\\Users\\Volkan\\Desktop\\Msc\\Sunum\\Exome sequencing\\Exome_server\\snpdraexomegenes_denovo.txt")
    genes2 = h.readlines()
    h.close()
    h = open("C:\\Users\\Volkan\\Desktop\\Msc\\Sunum\\Exome sequencing\\Exome_server\\snpnlesexomegenes_denovo.txt")
    genes3 = h.readlines()
    h.close()
    h = open("C:\\Users\\Volkan\\Desktop\\Msc\\Sunum\\Exome sequencing\\Exome_server\\snpesesexomegenes_denovo.txt")
    genes4 = h.readlines()
    h.close()
    geness = genes1 + genes2 + genes3 + genes4
    print(len(geness))
    othercounter = Counter(geness)
    dracounter = Counter(genes2)
    for i in dracounter:
        dracounter[i] = (100/31)*(dracounter[i])
    for i in othercounter:
        othercounter[i] = (100/120)*(othercounter[i])
    dracounter.subtract(othercounter)
    print(othercounter)

#butun hastalardaki damaging mutasyonlarin oldugu genleri ve sayilarini, ve hangilerinin epilepsi geni oldugunu bul
def countDeleteriousEpilepsyGenes():
    h = open("C:\\Users\\Volkan\\Desktop\\Msc\\Exome sequencing\\Exome_server\\damagingexomegenesall.txt")
    genes = h.readlines()
    h.close()
    h = open("C:\\Users\\Volkan\\Desktop\\Msc\\Common\\Epilepsigenleri.txt")
    epilepsyGenes = h.readlines()
    h.close()
    for gene in genes5:
        for epgene in epilepsyGenes:
            if gene == epgene:
                print(gene)
    allcounter = Counter(genes)


def findRatioOfEpilepsyGenes(allcounter):
    f = open("C:\\Users\\Volkan\\Desktop\\Msc\\Common\\Epilepsigenleri.txt")
    lines1 = f.readlines()
    f.close()
    countepilepsyrelated = 0
    sumall = 0
    sumepilepsyrelated = 0
    for gene in lines1:
        if gene in geness:
            sumepilepsyrelated = sumepilepsyrelated + allcounter[gene]
            countepilepsyrelated = countepilepsyrelated + 1
            print(gene)
            print(allcounter[gene])
    print(sumepilepsyrelated/countepilepsyrelated)
    for gene in allcounter:
        sumall = sumall + allcounter[gene]
    print(sumall/len(allcounter))

    setgeness = set(geness)
    listgeness = list(setgeness)
    listofrandomaverages = []
    for i in range(1000):
        sumrandom = 0
        for gene in [listgeness[i] for i in random.sample(range(len(listgeness)), 13)]:
            sumrandom = sumrandom + allcounter[gene]
        averagerandom = sumrandom/13
        listofrandomaverages.append(averagerandom)
    counter = 0
    for average in listofrandomaverages:
        if average > ((sumepilepsyrelated/countepilepsyrelated)):
            counter = counter + 1
    print(counter)

#??? tekrar incele
def findSnpsInEpilepsyGenes():
    f = open("C:\\Users\\Volkan\\Desktop\\Msc\\Common\\Epilepsivekanalgenleri.txt")
    lines1 = f.readlines()
    print(lines1)
    f.close()
    for i in range(16,17):
        filename = "E:\\genomedata\\"
        filenamespecific = filename + "MAE" + str(i) + "\\denovo_mild_queryresult_MAE" + str(i) + ".tsv"
        if os.path.isfile(filenamespecific):
            f = open(filenamespecific)
            lines2 = f.readlines()
            for line2 in lines2:
                seperatedline = line2.split("\t")
                for j in range(1):
                    if seperatedline[3] == "snp":
                        print(i)
                        print(seperatedline)
            f.close()

def readDamagingGenesPathways():
    f = open("C:\\Users\\Volkan\\Desktop\\Msc\\Exome sequencing\\Exome_server\\damagingexomegenesall_pathways.txt")
    lines = f.readlines()
    f.close()
    print(Counter(lines))

if __name__ == '__main__':

