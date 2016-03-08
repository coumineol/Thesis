#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Volkan
#
# Created:     14/04/2014
# Copyright:   (c) Volkan 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import re
import csv
import random
import numpy as np
import scipy
import copy
import matplotlib
import matplotlib.pyplot as plt
import showcolorgraph
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
#from sklearn import preprocessing
#from sklearn import decomposition
#from sklearn.manifold import Isomap
#from sklearn.manifold import LocallyLinearEmbedding
#from sklearn.manifold import SpectralEmbedding


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)


def reduceDim(array, method, siftScale, thisKernel, thisDegree, thisGamma, thisCoef0):
    reducedArray = copy.deepcopy(array)

    reducedArray[:,2] = 1 - reducedArray[:,2]

    reducedArray[:,2] = np.power(reducedArray[:,2], siftScale)

    noise0 = np.random.normal(0,0.001,len(reducedArray))
    noise1 = np.random.normal(0,0.001,len(reducedArray))
    noise2 = np.random.normal(0,0.001,len(reducedArray))
    reducedArray[:,0] = reducedArray[:,0] + noise0
    reducedArray[:,1] = reducedArray[:,1] + noise1
    reducedArray[:,2] = reducedArray[:,2] + noise2

    if method == "PCA":
        newPca = decomposition.PCA(n_components=1)
        reducedArray = newPca.fit_transform(reducedArray)
        principalVector = newPca.components_

    elif method == "Isomap":
        isomap = Isomap(n_neighbors=25, n_components=1)
        reducedArray = isomap.fit_transform(reducedArray)

    elif method == "LLE":
        lle = LocallyLinearEmbedding(n_neighbors=50, n_components=1)
        reducedArray = lle.fit_transform(reducedArray)

    elif method == "LE":
        lapmaps = SpectralEmbedding(n_components=1, affinity='nearest_neighbors', gamma=None)
        reducedArray = lapmaps.fit_transform(reducedArray)

    elif method == "KernelPCA":
        kpca = decomposition.KernelPCA(n_components=1, kernel=thisKernel, degree=thisDegree, gamma=thisGamma, coef0=thisCoef0)
        reducedArray = kpca.fit_transform(reducedArray)

    reducedArray -= np.min(reducedArray)
    reducedArray /= np.max(reducedArray)

    #reducedArray'in yonunu kontrol edip gerekliyse duzeltmek icin
    labelsArray = labelVariants(array)
    zerosSum = 0
    threesSum = 0
    zerosLen = 0
    threesLen = 0
    for i in range(len(labelsArray)):
        if labelsArray[i] == 0.0:
            zerosLen += 1
            zerosSum += reducedArray[i]
        if labelsArray[i] == 3.0:
            threesLen += 1
            threesSum += reducedArray[i]
    if (zerosSum/zerosLen) > (threesSum/threesLen):
        reducedArray = 1 - reducedArray
    print(len(reducedArray))

    #kullanilan yontemin hata payini olcmek icin ama bos yere iki defa dimreduce yapiliyor.
    """
    reducedArray2, transformedArray = reduceTransform(array, method, siftScale, thisKernel, thisDegree)
    print(len(transformedArray))
    print(len(labelsArray))
    performance = meanError(transformedArray, labelsArray, siftScale)
    print(performance)
    """
    return reducedArray


def reduceTransform(array, method, siftScale, thisKernel, thisDegree, thisGamma, thisCoef0):
    reducedArray = copy.deepcopy(array)

    reducedArray[:,2] = 1 - reducedArray[:,2]

    reducedArray[:,2] = np.power(reducedArray[:,2], siftScale)

    noise0 = np.random.normal(0,0.001,len(array))
    noise1 = np.random.normal(0,0.001,len(array))
    noise2 = np.random.normal(0,0.001,len(array))
    reducedArray[:,0] = reducedArray[:,0] + noise0
    reducedArray[:,1] = reducedArray[:,1] + noise1
    reducedArray[:,2] = reducedArray[:,2] + noise2

    scaledNoisedArray = copy.deepcopy(reducedArray)

    if method == "PCA":
        newPca = decomposition.PCA(n_components=1)
        reducedArray = newPca.fit_transform(reducedArray)
        transformedArray = newPca.inverse_transform(reducedArray)
        principalVector = newPca.components_

    elif method == "KernelPCA":
        #kpca = decomposition.KernelPCA(n_components=1, fit_inverse_transform=True, kernel=thisKernel, degree=thisDegree, gamma=thisGamma, coef0=thisCoef0)
        kpca = decomposition.KernelPCA(n_components=1, fit_inverse_transform=True, kernel=thisKernel, coef0=thisCoef0)
        reducedArray = kpca.fit_transform(reducedArray)
        transformedArray = kpca.inverse_transform(reducedArray)

    reducedArray -= np.min(reducedArray)
    reducedArray /= np.max(reducedArray)

    #reducedArray'in yonunu kontrol edip gerekliyse duzeltmek icin
    #bir problem var!!!
    #deepcopy kullaninca duzeldi galiba...
    labelsArray = labelVariants(array)
    zerosSum = 0
    threesSum = 0
    zerosLen = 0
    threesLen = 0
    for i in range(len(labelsArray)):
        if labelsArray[i] == 0.0:
            zerosLen += 1
            zerosSum += reducedArray[i]
        if labelsArray[i] == 3.0:
            threesLen += 1
            threesSum += reducedArray[i]
    #print(zerosLen)
    #print(threesLen)
    if (zerosSum/zerosLen) > (threesSum/threesLen):
        reducedArray = 1 - reducedArray
    #print(len(reducedArray))

    #print(principalVector)
    return reducedArray, transformedArray, scaledNoisedArray
    #return reducedArray, transformedArray, scaledNoisedArray, principalVector


def reduceTransformByMean(array, siftScale):
    reducedArray = copy.deepcopy(array)

    reducedArray[:,2] = 1 - reducedArray[:,2]
    reducedArray[:,2] = np.power(reducedArray[:,2], siftScale)

    noise0 = np.random.normal(0,0.001,len(array))
    noise1 = np.random.normal(0,0.001,len(array))
    noise2 = np.random.normal(0,0.001,len(array))
    reducedArray[:,0] = reducedArray[:,0] + noise0
    reducedArray[:,1] = reducedArray[:,1] + noise1
    reducedArray[:,2] = reducedArray[:,2] + noise2

    averageScores = np.zeros(len(array))

    transformedArray = np.zeros_like(array)

    for i in range(0, len(array)):
        averageScores[i] = (reducedArray[i,0] + reducedArray[i,1] + reducedArray[i,2]) / 3
        transformedArray[i,0], transformedArray[i,1], transformedArray[i,2] = averageScores[i], averageScores[i], averageScores[i]

    reducedArray = averageScores

    return reducedArray, transformedArray


def readDeleteriousGenesFromMultiplePatients(disorder=None):
    #g = open("C:\\Users\\Volkan\\Desktop\\Msc\\Exome sequencing\\Exome_server\\damagingsnpdraexomegenes_homoz.txt", "w")

    if disorder == None:
        return None

    elif not isinstance(disorder, str):
        return None

    elif disorder == "deneme":
        return None

    else:
        f = open("C:\\Users\\Volkan\\Desktop\\Msc\\Common\\allproteincodinggenes.txt")
        lines = f.readlines()
        listofgenes = []
        for i in range(len(lines)):
            listofgenes.append(lines[i][:-1])
        f.close()

        allVariantScores = []
        filename = "E:\\genomedata\\"
        counter = 0
        for i in range(1,52):
            print(i)
            filenamespecific = filename + disorder.upper() + str(i) + "\\homoz_mild_queryresult_" + disorder.lower() + str(i) + ".tsv"
            if os.path.isfile(filenamespecific):
                f = open(filenamespecific)
                lines = f.readlines()

                idx1, idx2, idx3 = None, None, None
                line = lines[0]
                splitline = line.split("\t")
                regex = r'Condel.*PATIENT_GATK_calls'
                for element in splitline:
                    found = re.findall(regex, element)
                    if len(found) == 1:
                        idx1 = splitline.index(found[0])
                        break
                regex = r'PolyPhen.*PATIENT_GATK_calls'
                for element in splitline:
                    found = re.findall(regex, element)
                    if len(found) == 1:
                        idx2 = splitline.index(found[0])
                        break
                regex = r'SIFT.*PATIENT_GATK_calls'
                for element in splitline:
                    found = re.findall(regex, element)
                    if len(found) == 1:
                        idx3 = splitline.index(found[0])
                        break
                if idx1 == None or idx2 == None or idx3 == None:
                    continue

                for line in lines:
                    splitline = line.split("\t")
                    for gene in listofgenes:
                        if gene in splitline and splitline[3] == "snp":
                            thisVariant = []
                            if (splitline[idx1] != "" or splitline[idx2] != "" or splitline[idx3] != "") and (splitline[idx1] != "?" or splitline[idx2] != "?" or splitline[idx3] != "?"):
                                if not (splitline[idx1] == "" and splitline[idx2] == "unknown(0)" and splitline[idx3] == ""):
                                    if not (splitline[idx1] == "not_computable_was(-1)" and splitline[idx2] == "" and splitline[idx3] == ""):
                                        thisVariant.append(str(counter))
                                        thisVariant.append(str(i))
                                        thisVariant.append(gene)
                                        thisVariant.append(str(splitline[0]))
                                        thisVariant.append(str(splitline[1]))
                                        thisVariant.append(str(splitline[2]))
                                        thisVariant.append(splitline[4])
                                        thisVariant.append(splitline[5])
                                        thisVariant.append(splitline[idx1])
                                        thisVariant.append(splitline[idx2])
                                        thisVariant.append(splitline[idx3])
                                        allVariantScores.append(thisVariant)
                                        counter += 1
                                        print(thisVariant)
                                        break
                f.close()

        return allVariantScores

def listify(file):
    variantList = []
    f = open(file, "r")
    csv_file = csv.reader(f)
    for row in csv_file:
        variantList.append(list(row))
    f.close

    return variantList

def parseToArray(variantList):
    scoresList = []
    for variant in variantList:
        if re.findall(r"\(.*\)", variant[8]) != [] and re.findall(r"\(.*\)", variant[9]) != [] and re.findall(r"\(.*\)", variant[10]) != []:
            if variant[8] != "not_computable_was(-1)" and variant[9] != "unknown(0)":
                scoresList.append(variant[8:])

    scoresListAsFloat = []
    for variant in scoresList:
        newVariant = []
        for score in variant:
            x = float((re.findall(r'\(.*\)', score))[0][1:-1])
            newVariant.append(x)
        scoresListAsFloat.append(newVariant)

    newArray = np.asarray(scoresListAsFloat)

    return newArray


def labelVariants(array):
    labelsArray = []
    for i in range(0,len(array)):
        counter = 0.0
        if array[i,0] >= 0.469:
            counter += 1.0

        if array[i,1] >= 0.375:
            counter += 1.0

        if array[i,2] < 0.05:
            counter += 1.0
        elif array[i,2] == 0.05:
            coinFlip = random.random()
            if coinFlip > 0.5:
                counter += 1

        labelsArray.append(counter)

    return labelsArray


def meanError(transformedArray, labels, siftScaling):
    mainCounter = 0

    for i in range(len(transformedArray)):
        variantCounter = 0
        if transformedArray[i][0] > 0.469:
            variantCounter += 1.0
        if transformedArray[i][1] > 0.375:
            variantCounter += 1.0
        if transformedArray[i][2] > (0.95 ** siftScaling):
            variantCounter += 1.0
        error = abs(labels[i] - variantCounter)
        mainCounter += error

    return (mainCounter / len(transformedArray))


def euclidDistancesDifference(originalArray, transformedArray):
    totalDifference = 0

    for i in range(len(originalArray)):
        differenceArray = originalArray[i] - transformedArray[i]
        totalDifference += np.linalg.norm(differenceArray)

    return (totalDifference / len(originalArray))


def measurePerformance(array):
    tempArray = array
    labelsArray = labelVariants(array)
    matplotlib.rcParams['font.family'] = 'serif'
    matplotlib.rcParams['font.serif'] = 'Times New Roman'
    matplotlib.rcParams['font.size'] = 14

    """
    condel = array[:,0]
    polyphen = array[:,1]
    sift = array[:,2]
    plt.hist(condel, bins=20, color='black')
    plt.xlabel('Condel Score')
    plt.ylabel('Variant Count')
    plt.show()
    plt.hist(polyphen, bins=20, color='black')
    plt.xlabel('PolyPhen Score')
    plt.ylabel('Variant Count')
    plt.show()
    plt.hist(np.power((1-sift), 8), bins=20, color='black')
    plt.xlabel('SIFT Score')
    plt.ylabel('Variant Count')
    plt.show()
    """
    """
    degree = 2
    gamma = 4.86
    coef0 = 1.2
    #reducedArray, transformedArray, scaledNoisedArray = reduceTransform(tempArray, "KernelPCA", 8, "sigmoid", degree, gamma, coef0)
    #reducedArray, transformedArray, scaledNoisedArray = reduceTransform(tempArray, "KernelPCA", 8, "sigmoid", 1, 1, coef0)
    plt.hist(reducedArray, bins=20, color='black')
    plt.xlabel('Reduced Score')
    plt.ylabel('Variant Count')
    plt.show()
    print(reducedArray)
    """
    ############################################################################
    """
    #KPCA'yi test et, grafik cizdir
    sigma = 8
    degree = 2
    gammas = []
    coefs = []
    deltas = []
    ds = []
    for coef0 in np.linspace(1,1.5,20):
        for gamma in range(0,1):
            try:
                reducedArray, transformedArray, scaledNoisedArray = reduceTransform(tempArray, "KernelPCA", sigma, "sigmoid", degree, gamma, coef0)
                performance1 = meanError(transformedArray, labelsArray, 8)
                performance2 = euclidDistancesDifference(array, transformedArray)
                tempArray = array
                reducedArray, transformedArray, scaledNoisedArray = reduceTransform(tempArray, "KernelPCA", sigma, "sigmoid", degree, gamma, coef0)
                performance3 = meanError(transformedArray, labelsArray, 8)
                performance4 = euclidDistancesDifference(array, transformedArray)
                tempArray = array
                reducedArray, transformedArray, scaledNoisedArray = reduceTransform(tempArray, "KernelPCA", sigma, "sigmoid", degree, gamma, coef0)
                performance5 = meanError(transformedArray, labelsArray, 8)
                performance6 = euclidDistancesDifference(array, transformedArray)
                tempArray = array
                reducedArray, transformedArray, scaledNoisedArray = reduceTransform(tempArray, "KernelPCA", sigma, "sigmoid", degree, gamma, coef0)
                performance7 = meanError(transformedArray, labelsArray, 8)
                performance8 = euclidDistancesDifference(array, transformedArray)
                tempArray = array
                reducedArray, transformedArray, scaledNoisedArray = reduceTransform(tempArray, "KernelPCA", sigma, "sigmoid", degree, gamma, coef0)
                performance9 = meanError(transformedArray, labelsArray, 8)
                performance10 = euclidDistancesDifference(array, transformedArray)
                tempArray = array
                delta = (performance1+performance3+performance5+performance7+performance9)/5
                d = (performance2+performance4+performance6+performance8+performance10)/5
                print([degree, gamma, coef0, delta, d])
                gammas.append(gamma)
                coefs.append(coef0)
                deltas.append(delta)
                ds.append(d)
            except:
                print("---")
    gammas = np.asarray(gammas)
    coefs = np.asarray(coefs)
    deltas = np.asarray(deltas)
    ds = np.asarray(ds)
    print(coefs.size)
    print(deltas.size)
    #showcolorgraph.showColorGraph(deltas)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    #plt.axis([0.5, 30.5, 0.25, 0.45])
    ax.scatter(coefs, deltas, color='black')
    ax.set_xlabel('c', size=20)
    ax.set_ylabel(r'$\delta$', size=20)
    plt.show()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #plt.axis([0.5, 30.5, 0.25, 0.45])
    ax.scatter(coefs, ds, color='black')
    ax.set_xlabel('c', size=20)
    ax.set_ylabel('d', size=20)
    plt.show()
    """

################################################################################

    """
    sigmas = []
    performances = []
    for sigma in range(1,31):
        reducedArray, transformedArray, scaledNoisedArray, principalVector = reduceTransform(tempArray, "PCA", sigma, "rbf", 1, 1, 0)
        performance1 = meanError(transformedArray, labelsArray, sigma)
        performance2 = euclidDistancesDifference(array, transformedArray)
        print([sigma, performance1, performance2])
        sigmas.append(sigma)
        performances.append(performance1)
        tempArray = array
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.axis([0.5, 30.5, 0.25, 0.45])
    ax.scatter(sigmas, performances, color='black')
    ax.set_xlabel(r'$\sigma$', size=20)
    ax.set_ylabel(r'$\delta$', size=20)
    plt.show()
    """

################################################################################
    """
    neighbors = []
    errors = []
    for i in range(41,100):
        reducedArray = array
        lle = LocallyLinearEmbedding(n_neighbors=i, n_components=1)
        reducedArray = lle.fit_transform(reducedArray)
        neighbors.append(i)
        errors.append(1000000*lle.reconstruction_error_)
        print(lle.reconstruction_error_)
        print(i)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #plt.axis([5, 105, 0.06, 0.11])
    ax.scatter(neighbors, errors, color='black')
    ax.set_xlabel('neighbor', size=16)
    ax.set_ylabel('error', size=16)
    plt.show()
    """
################################################################################

    #reducedArray, transformedArray, scaledNoisedArray = reduceTransform(tempArray, "KernelPCA", 8, "rbf", 1, 4.75, 1)
    reducedArray, transformedArray = reduceTransformByMean(tempArray, 8)
    #lapmaps = SpectralEmbedding(n_components=1, n_neighbors=40)
    #reducedArray = lapmaps.fit_transform(array)
    reducedArray = np.asarray(reducedArray)
    reducedArray -= np.min(reducedArray)
    reducedArray /= np.max(reducedArray)
    performance1 = meanError(transformedArray, labelsArray, 8)
    performance2 = euclidDistancesDifference(tempArray, transformedArray)
    print(performance1, performance2)
    #mutasyonlarin indirgenmis puanlarini, orijinal hallerinin aldigi puanlara gore (0-3) 4 farkli array'e ekliyorum
    allArray = []
    zerosArray = []
    onesArray = []
    twosArray = []
    threesArray = []
    for i in range(0,426):
        if labelsArray[i] == 0.0:
            zerosArray.append(reducedArray[i])
        elif labelsArray[i] == 1.0:
            onesArray.append(reducedArray[i])
        elif labelsArray[i] == 2.0:
            twosArray.append(reducedArray[i])
        elif labelsArray[i] == 3.0:
            threesArray.append(reducedArray[i])
        allArray.append(reducedArray[i])
    zerosArray = np.asarray(zerosArray)
    onesArray = np.asarray(onesArray)
    twosArray = np.asarray(twosArray)
    threesArray = np.asarray(threesArray)

    plt.hist(reducedArray, bins=20, color='black')
    #plt.hist(reducedArray, bins=20, range=[0.0, 1.0], color='black')
    plt.xlabel('Reduced Score')
    plt.ylabel('Variant Count')
    plt.show()

    """
    principalVectorCondel = principalVector[0][0]
    principalVectorPolyphen = principalVector[0][1]
    principalVectorSift = principalVector[0][2]

    condel = transformedArray[:,0]
    polyphen = transformedArray[:,1]
    sift = transformedArray[:,2]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #ax = fig.add_subplot(111)
    ax.scatter(condel, polyphen, sift, color='black')
    ax.set_xlabel('Condel')
    ax.set_ylabel('PolyPhen')
    ax.set_zlabel('SIFT')
    #a = Arrow3D([0,principalVectorCondel],[0,principalVectorPolyphen],[0,principalVectorSift], mutation_scale=20, lw=1, arrowstyle="-|>", color="k")
    #ax.add_artist(a)
    plt.show()
    """

    fig = plt.figure()
    plt.axis([np.min(reducedArray)-0.05, np.max(reducedArray)+0.05, -0.1, 3.1])
    plt.xticks(np.arange(0.0, 1.2, 0.2))
    plt.yticks(np.arange(0.0, 4.0, 1.0))
    for i in range(0,426):
        if labelsArray[i] == 0.0:
            plt.scatter(reducedArray[i], labelsArray[i], c=(0,1,0), marker='o', s=150, alpha=0.9)
        elif labelsArray[i] == 1.0:
            plt.scatter(reducedArray[i], labelsArray[i], c=(0.33,0.67,0), marker='o', s=150, alpha=0.9)
        elif labelsArray[i] == 2.0:
            plt.scatter(reducedArray[i], labelsArray[i], c=(0.67,0.33,0), marker='o', s=150, alpha=0.9)
        elif labelsArray[i] == 3.0:
            plt.scatter(reducedArray[i], labelsArray[i], c=(1,0,0), marker='o', s=150, alpha=0.9)
        else:
            plt.scatter(reducedArray[i], labelsArray[i], c=(0,0,0), marker='o', s=150, alpha=0.9)
    plt.xlabel('Reduced Score')
    plt.ylabel('Degree of Deleteriousness')
    plt.show()


def scoresOneDim(variantList, method, siftScale, thisKernel, thisDegree, thisGamma, thisCoef0):
    array = parseToArray(variantList)
    reducedArray = reduceDim(array, method, siftScale, thisKernel, thisDegree, thisGamma, thisCoef0)
    return reducedArray


if __name__ == '__main__':
    measurePerformance(parseToArray(listify("C:\\Users\\Volkan\\Desktop\\Msc\\Exome sequencing\\Exome_server\\denovomilddrasnpscores.csv")))
    #scoresOneDim(listify("C:\\Users\\Volkan\\Desktop\\Msc\\Exome sequencing\\Exome_server\\denovomilddrasnpscores.csv"), "PCA", 6, "rbf", 4)
    #readDeleteriousGenesFromMultiplePatients("DRA")