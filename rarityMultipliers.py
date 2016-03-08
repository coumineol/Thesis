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

import listifyCsv
import findCommonGenes

def findGammaParameters(variantList, geneList, priorAlpha, priorBeta):
    allParameters = []

    for gene in geneList:
        alpha = priorAlpha
        beta = priorBeta
        alpha += [item[2] for item in variantList].count(gene)
        beta += len(variantList) #bu yanlis. bir gendeki iki mutasyonu bir mutasyon olarak kabul etmek gerekiyor!
        allParameters.append([alpha, beta])

    return allParameters


def gammaToScores(parameters):
    penalties = []
    for gene in parameters:
        penalties.append(gene[0]/gene[1])

    return ([(1/penalty) for penalty in penalties])

def rarityMultipliers(variantList, geneList, priorAlpha, priorBeta):
    parameters = findGammaParameters(variantList, geneList, priorAlpha, priorBeta)
    return gammaToScores(parameters)


if __name__ == '__main__':
    variantListDra, variantListEses, variantListMae, variantListNles = listifyCsv.listifyCsvDeNovoMild()
    variantList = variantListDra + variantListEses + variantListMae + variantListNles

    geneList = findCommonGenes.findCommonGenes(variantListDra, variantListEses, variantListMae, variantListNles)

    parameters = findGammaParameters(variantList, geneList, 1.0/3.0, 0.0)
    penalties = frequencyPenalty(parameters)

    for i in range(len(geneList)):
        print(geneList[i] + ": " + str(penalties[i]))
