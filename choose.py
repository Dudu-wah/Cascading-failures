import random

def randomNodes(numberToChoose, maxNodes):
    nodesChosen = []
    for current in range(numberToChoose):
        nodesChosen.append(random.randrange(0, maxNodes, 1))

    return nodesChosen


def highestDegreesNodes(graph, numberOfNodes):
    degreesDict = dict(graph.degree)
    degreesDict = {k: v for k, v in sorted(degreesDict.items(), key=lambda item: item[1])}
    degreesList = list(zip(degreesDict.keys(), degreesDict.values()))
    nodesAndLoads = {}

    for index in range (len(degreesList), len(degreesList) - numberOfNodes, -1):
        nodesAndLoads[degreesList[index-1][0]] = degreesList[index-1][1]

    return nodesAndLoads