import csv
from copy import deepcopy
import itertools

def listifyCsvDeNovoMild():
    file = "C:\\Users\\Volkan\\Desktop\\Msc\\Exome sequencing\\Exome_server\\denovomilddrasnpscores.csv"
    variantListDra = []
    f = open(file, "r")
    csv_file = csv.reader(f)
    for row in csv_file:
        variantListDra.append(list(row))
    f.close

    file = "C:\\Users\\Volkan\\Desktop\\Msc\\Exome sequencing\\Exome_server\\denovomildesessnpscores.csv"
    variantListEses = []
    f = open(file, "r")
    csv_file = csv.reader(f)
    for row in csv_file:
        variantListEses.append(list(row))
    f.close

    file = "C:\\Users\\Volkan\\Desktop\\Msc\\Exome sequencing\\Exome_server\\denovomildmaesnpscores.csv"
    variantListMae = []
    f = open(file, "r")
    csv_file = csv.reader(f)
    for row in csv_file:
        variantListMae.append(list(row))
    f.close

    file = "C:\\Users\\Volkan\\Desktop\\Msc\\Exome sequencing\\Exome_server\\denovomildnlessnpscores.csv"
    variantListNles = []
    f = open(file, "r")
    csv_file = csv.reader(f)
    for row in csv_file:
        variantListNles.append(list(row))
    f.close

    return variantListDra, variantListEses, variantListMae, variantListNles

def listifyCsvDeNovoStrict():
    file = "C:\\Users\\Volkan\\Desktop\\Msc\\Exome sequencing\\Exome_server\\denovostrictdrasnpscores.csv"
    variantListDra = []
    f = open(file, "r")
    csv_file = csv.reader(f)
    for row in csv_file:
        variantListDra.append(list(row))
    f.close

    file = "C:\\Users\\Volkan\\Desktop\\Msc\\Exome sequencing\\Exome_server\\denovostrictesessnpscores.csv"
    variantListEses = []
    f = open(file, "r")
    csv_file = csv.reader(f)
    for row in csv_file:
        variantListEses.append(list(row))
    f.close

    file = "C:\\Users\\Volkan\\Desktop\\Msc\\Exome sequencing\\Exome_server\\denovostrictmaesnpscores.csv"
    variantListMae = []
    f = open(file, "r")
    csv_file = csv.reader(f)
    for row in csv_file:
        variantListMae.append(list(row))
    f.close

    file = "C:\\Users\\Volkan\\Desktop\\Msc\\Exome sequencing\\Exome_server\\denovostrictnlessnpscores.csv"
    variantListNles = []
    f = open(file, "r")
    csv_file = csv.reader(f)
    for row in csv_file:
        variantListNles.append(list(row))
    f.close

    return variantListDra, variantListEses, variantListMae, variantListNles

if __name__ == '__main__':
    variantListDra, variantListEses, variantListMae, variantListNles = listifyCsvDeNovoStrict()


