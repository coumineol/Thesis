import listifyCsv

def findCommonGenes(variantListDra, variantListEses, variantListMae, variantListNles):
    geneListDra = []
    for variant in variantListDra:
        geneListDra.append(variant[2])

    geneListEses = []
    for variant in variantListEses:
        geneListEses.append(variant[2])

    geneListMae = []
    for variant in variantListMae:
        geneListMae.append(variant[2])

    geneListNles = []
    for variant in variantListNles:
        geneListNles.append(variant[2])

    allGenesList = geneListDra + geneListEses + geneListMae + geneListNles
    print(allGenesList.count("NOTCH1"))
    #allGenesList = list(set(allGenesList))

    commonGenesList = []
    for gene in allGenesList:
        if gene in geneListDra and gene in geneListEses and gene in geneListMae and gene in geneListNles:
            commonGenesList.append(gene)

    return commonGenesList

    """common genleri bulmak icin sadece de novolardan degil butun varyantlardan faydalansam?"""


if __name__ == '__main__':
    variantListDra, variantListEses, variantListMae, variantListNles = listifyCsv.listifyCsvDeNovoMild()
    myList = findCommonGenes(variantListDra, variantListEses, variantListMae, variantListNles)