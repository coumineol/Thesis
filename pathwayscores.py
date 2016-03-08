#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Volkan
#
# Created:     08/08/2014
# Copyright:   (c) Volkan 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os


def normalize(pathwayScorePairs):

    newPathwayScorePairs = []
    onlyScores = [score for pathway, score in pathwayScorePairs]
    maxScore = max(onlyScores)
    for gene, score in pathwayScorePairs:
        newPathwayScorePairs.append((gene, score/maxScore))
    return newPathwayScorePairs


def main(geneScorePairs):

    componentScorePairs = {}
    functionScorePairs = {}
    processScorePairs = {}
    allComponentsTemp = []
    allFunctionsTemp = []
    allProcessesTemp = []

    for gene in geneScorePairs:

        if isinstance(gene, str) and isinstance(geneScorePairs[gene], float):
            pass
        else:
            print("tur uyusmazligi")
            break

        filepath = "genes\\" + gene + ".tsv"
        if os.path.isfile(filepath):
            file = open(filepath)
        else:
            print("yok boyle bi dosya")
            break

        componentsForThisGene = []
        functionsForThisGene = []
        processesForThisGene = []

        lines = file.readlines()
        for line in lines[1:]:
            splitLine = line.split("\t")
            if splitLine[6] == "Component":
                componentsForThisGene.append(splitLine[5])
                allComponentsTemp.append(splitLine[5])
            elif splitLine[6] == "Function":
                functionsForThisGene.append(splitLine[5])
            elif splitLine[6] == "Process":
                processesForThisGene.append(splitLine[5])
            else:
                print("bu dosyada bi yanlislik var")
                break

        if componentsForThisGene == [] and functionsForThisGene == [] and processesForThisGene == []:
            break

        componentsForThisGene = list(set(componentsForThisGene))
        functionsForThisGene = list(set(functionsForThisGene))
        processesForThisGene = list(set(processesForThisGene))

        for component in componentsForThisGene:
            if component in componentScorePairs:
                componentScorePairs[component] += geneScorePairs[gene]
            else:
                componentScorePairs.update({component: geneScorePairs[gene]})
        for function in functionsForThisGene:
            if function in functionScorePairs:
                functionScorePairs[function] += geneScorePairs[gene]
            else:
                functionScorePairs.update({function: geneScorePairs[gene]})
        for process in processesForThisGene:
            if process in processScorePairs:
                processScorePairs[process] += geneScorePairs[gene]
            else:
                processScorePairs.update({process: geneScorePairs[gene]})

        file.close()

    componentScorePairs = sorted(componentScorePairs.items(), key=lambda x:x[1], reverse=True)
    functionScorePairs = sorted(functionScorePairs.items(), key=lambda x:x[1], reverse=True)
    processScorePairs = sorted(processScorePairs.items(), key=lambda x:x[1], reverse=True)
    componentScorePairs = normalize(componentScorePairs)
    functionScorePairs = normalize(processScorePairs)
    processScorePairs = normalize(processScorePairs)

    return componentScorePairs, functionScorePairs

if __name__ == '__main__':
    c, f = main([("ACE", 1.0), ("NOTCH1", -0.1), ("GAS6", 0.2)])
    print(f)
