#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Volkan
#
# Created:     10/11/2014
# Copyright:   (c) Volkan 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import re
import csv

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
        for i in range(1,4):
            print(i)
            filenamespecific = filename + disorder.upper() + str(i) + "\\denovo_strict_queryresult_" + disorder.lower() + str(i) + ".tsv"
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
                        if gene == "NOTCH1":
                            thisVariant = []
                            if True:
                                if True:
                                    if True:
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

                f.close()

        return allVariantScores

if __name__ == '__main__':
    readDeleteriousGenesFromMultiplePatients("NLES")
