#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Volkan
#
# Created:     04/06/2014
# Copyright:   (c) Volkan 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import re
import itertools
from copy import deepcopy
import os
import numpy as np
import listifyCsv as lc
import findCommonGenes as fcg
import analyzeDeleteriousness as ad
import rarityMultipliers as rm
import pathwayscores as ps
import matplotlib.pyplot as plt

def onlyAllThreeScoresSpecified(variantList):
    newList = []
    for variant in variantList:
        if re.findall(r"\(.*\)", variant[8]) != [] and re.findall(r"\(.*\)", variant[9]) != [] and re.findall(r"\(.*\)", variant[10]) != []:
            if variant[8] != "not_computable_was(-1)" and variant[9] != "unknown(0)":
                newList.append(variant)
    return newList


def filterByGene(variantList, geneList):
    newList = []
    for variant in variantList:
        if variant[2] in geneList:
            newList.append(variant)
    return newList


def addRarityScores(variantList, geneList, rarityArray):
    newList = []
    for variant in variantList:
        idx = geneList.index(variant[2])
        variant.append(rarityArray[idx])
        newList.append(variant)
    return newList


def addStrictnessScores(variantList, strictList, strictMultiplier): #tek bir hastalik icin variantList ve strictList girilmeli
    newVariantList = [variant[1:] for variant in variantList]
    newStrictList = [variant[1:] for variant in strictList]
    newList = []
    for variant in newVariantList:
        if variant[:10] in newStrictList:
            variant.append(strictMultiplier)
        else:
            variant.append(1.0)
        newList.append(variant)
    return newList


def finalScores(gene, firstGroup, secondGroup, patientCountFirst, patientCountSecond):
    #bu iki kisim, ayni gendeki birden fazla mutasyonu tek mutasyon olarak saymak icin

    firstGroupFiltered = []
    secondGroupFiltered = []

    for variantList in firstGroup:
        variantsInOneFile = []
        for variant in variantList:
            variantsInOnePatient = []
            if variant[1] == gene:
                variantsInOneFile.append((variant[0], variant[-1]*variant[-2]*variant[-3]))
        firstGroupFiltered.append(variantsInOneFile)

    for variantList in secondGroup:
        variantsInOneFile = []
        for variant in variantList:
            variantsInOnePatient = []
            if variant[1] == gene:
                variantsInOneFile.append((variant[0], variant[-1]*variant[-2]*variant[-3]))
        secondGroupFiltered.append(variantsInOneFile)

    firstCounter = 0
    for variantList in firstGroupFiltered:
        for key, group in itertools.groupby(variantList, lambda x: x[0]):
            firstCounter += max([i[1] for i in group])

    secondCounter = 0
    for variantList in secondGroupFiltered:
        for key, group in itertools.groupby(variantList, lambda x: x[0]):
            secondCounter += max([i[1] for i in group])

    return (firstCounter/patientCountFirst - secondCounter/patientCountSecond)


def main():
    variantListDraMild, variantListEsesMild, variantListMaeMild, variantListNlesMild = lc.listifyCsvDeNovoMild()
    variantListMild = deepcopy(variantListDraMild + variantListEsesMild + variantListMaeMild + variantListNlesMild)
    variantListDraStrict, variantListEsesStrict, variantListMaeStrict, variantListNlesStrict = lc.listifyCsvDeNovoStrict()
    variantListStrict = deepcopy(variantListDraStrict + variantListEsesStrict + variantListMaeStrict + variantListNlesStrict)

    variantListDraMild = onlyAllThreeScoresSpecified(variantListDraMild)
    variantListEsesMild = onlyAllThreeScoresSpecified(variantListEsesMild)
    variantListMaeMild = onlyAllThreeScoresSpecified(variantListMaeMild)
    variantListNlesMild = onlyAllThreeScoresSpecified(variantListNlesMild)
    variantListMild = onlyAllThreeScoresSpecified(variantListMild)

    geneList = fcg.findCommonGenes(variantListDraMild, variantListEsesMild, variantListMaeMild, variantListNlesMild)
    geneList.sort()

    rarityArray = rm.rarityMultipliers(variantListMild, geneList, 1000., 0.001)
    scoresArray = ad.scoresOneDim(variantListMild, "KernelPCA", 8, "poly", 2, 4.86, -22)

    for i in range(len(variantListDraMild)):
        variantListDraMild[i].append(float(scoresArray[i]))
    for i in range(len(variantListDraMild), len(variantListDraMild)+len(variantListEsesMild)):
        variantListEsesMild[i-len(variantListDraMild)].append(float(scoresArray[i]))
    for i in range(len(variantListDraMild)+len(variantListEsesMild), len(variantListDraMild)+len(variantListEsesMild)+len(variantListMaeMild)):
        variantListMaeMild[i-len(variantListDraMild)-len(variantListEsesMild)].append(float(scoresArray[i]))
    for i in range(len(variantListDraMild)+len(variantListEsesMild)+len(variantListMaeMild), len(variantListDraMild)+len(variantListEsesMild)+len(variantListMaeMild)+len(variantListNlesMild)):
        variantListNlesMild[i-len(variantListDraMild)-len(variantListEsesMild)-len(variantListMaeMild)].append(float(scoresArray[i]))
    for i in range(len(variantListMild)):
        variantListMild[i].append(float(scoresArray[i]))

    variantListDraMild = filterByGene(variantListDraMild, geneList)
    variantListEsesMild = filterByGene(variantListEsesMild, geneList)
    variantListMaeMild = filterByGene(variantListMaeMild, geneList)
    variantListNlesMild = filterByGene(variantListNlesMild, geneList)

    variantListDraMild = addRarityScores(variantListDraMild, geneList, rarityArray)
    variantListEsesMild = addRarityScores(variantListEsesMild, geneList, rarityArray)
    variantListMaeMild = addRarityScores(variantListMaeMild, geneList, rarityArray)
    variantListNlesMild = addRarityScores(variantListNlesMild, geneList, rarityArray)

    variantListDraMild = addStrictnessScores(variantListDraMild, variantListDraStrict, 1.1)
    variantListEsesMild = addStrictnessScores(variantListEsesMild, variantListEsesStrict, 1.1)
    variantListMaeMild = addStrictnessScores(variantListMaeMild, variantListMaeStrict, 1.1)
    variantListNlesMild = addStrictnessScores(variantListNlesMild, variantListNlesStrict, 1.1)

    """
    for i in range(0,20):
        print(variantListEsesMild[i][-1])
    """
    ##########
    patientCountFirst = 0
    patientCountSecond = 0

    patientIdsDra = []
    for variant in variantListDraMild:
        patientIdsDra.append(variant[0])
    patientIdsDra = list(set(patientIdsDra))
    patientCountFirst += len(patientIdsDra)
    print(len(patientIdsDra))

    patientIdsEses = []
    for variant in variantListEsesMild:
        patientIdsEses.append(variant[0])
    patientIdsEses = list(set(patientIdsEses))
    patientCountSecond += len(patientIdsEses)
    print(len(patientIdsEses))

    patientIdsMae = []
    for variant in variantListMaeMild:
        patientIdsMae.append(variant[0])
    patientIdsMae = list(set(patientIdsMae))
    patientCountSecond += len(patientIdsMae)
    print(len(patientIdsMae))

    patientIdsNles = []
    for variant in variantListNlesMild:
        patientIdsNles.append(variant[0])
    patientIdsNles = list(set(patientIdsNles))
    patientCountFirst += len(patientIdsNles)
    print(len(patientIdsNles))
    print("!?!")
    ##########

    differentials = []
    geneScorePairs = {}
    for gene in geneList:
        filename = "C:\\Users\\Volkan\\Desktop\\Msc\\Exome sequencing\\Exome_server\\newCodeFiles\\genes\\" + str(gene) + ".tsv"
        if os.path.isfile(filename):
            pass
        else:
            continue
        score = finalScores(gene, [variantListDraMild, variantListNlesMild], [variantListEsesMild, variantListMaeMild], patientCountFirst, patientCountSecond)
        differentials.append(score)
        geneScorePairs[gene] = score

    maxScore = max(geneScorePairs.values())
    for gene in geneScorePairs:
        geneScorePairs[gene] = geneScorePairs[gene]/maxScore
    print(sorted(geneScorePairs.items(), key=lambda x:x[1], reverse=True))

    """
    array = np.array(differentials)
    plt.hist(differentials, bins=20)
    plt.show()

    componentScorePairs, functionScorePairs = ps.main(geneScorePairs)
    print(componentScorePairs)
    """

if __name__ == '__main__':
    main()