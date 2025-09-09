from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt

def nodeCount(nodesList):
    fig, ax = plt.subplots()
    ax.set_title("Node count")
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Number of nodes")
    iterations = [i for i in range(len(nodesList))]

    ax.set_xticks(iterations)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.plot(iterations, nodesList)
    plt.savefig("Graphs/Node Count x iterations.png")

def largestComponentsNodeCount(nodesList):
    fig, ax = plt.subplots()
    ax.set_title("Node count in largest component")
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Number of nodes")
    iterations = [i for i in range(len(nodesList))]

    ax.set_xticks(iterations)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.plot(iterations, nodesList)
    plt.savefig("Graphs/Node Count x iterations.png")

def networkEfficiency(efficienciesList):
    fig, ax = plt.subplots()
    ax.set_title("Network efficiency")
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Global efficiency [%]")
    iterations = [i for i in range(len(efficienciesList))]

    ax.set_xticks(iterations)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.plot(iterations, efficienciesList)
    plt.savefig("Graphs/Efficiency x iterations.png")

def writeNodesToFile(nodesList, largestComponentsNodesList, initialNodeCount, tolerance, preferentialAttachment, removeType, probability, powerLawParameter):
    filePath = f"ConfigurationModel/NodesData/TotalNodeCount/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{powerLawParameter}gamma.txt"
    file = open(filePath, "a+")
    file.write(f"{nodesList}\n")
    file.close()

    filePath = f"ConfigurationModel/NodesData/LargestComponentsNodeCount/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{powerLawParameter}gamma.txt"
    file = open(filePath, "a+")
    file.write(f"{largestComponentsNodesList}\n")
    file.close()

def nodeCountAverages(totalCountPath, largestComponentPath):
    fileTotalCount = open(totalCountPath, "r")
    fileLargestComponentCount = open(largestComponentPath, "r")
    totalNodesList = normalizeData(totalCountPath)
    largestComponentsNodesList = normalizeData(largestComponentPath)

    listOfAveragesTotal = []
    listOfAveragesLargestComponent = []
    iterations = [i for i in range(len(max(totalNodesList, key=len)))]
    for iteration in iterations:
        totalNodeCountInIteration = 0
        averageTotalNodeCount = 0

        largestComponentNodeCountInIteration = 0
        largestComponentNodeCount = 0
        for totalList in totalNodesList:
            if iteration < len(totalList):
                totalNodeCountInIteration += 1
                averageTotalNodeCount += totalList[iteration]

        averageTotalNodeCount = round(averageTotalNodeCount / totalNodeCountInIteration, 2)
        listOfAveragesTotal.append(averageTotalNodeCount)

        for largestComponentList in largestComponentsNodesList:
            if iteration < len(largestComponentList):
                largestComponentNodeCountInIteration += 1
                largestComponentNodeCount += largestComponentList[iteration]

        largestComponentNodeCount = round(largestComponentNodeCount / largestComponentNodeCountInIteration, 2)
        listOfAveragesLargestComponent.append(largestComponentNodeCount)

    fileTotalCount.close()
    fileLargestComponentCount.close()

    fig, ax = plt.subplots()

    ax.set_title("Average node count")
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Number of nodes [%]")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.plot(iterations, listOfAveragesTotal)

    plt.savefig("aaaa/total.png")

    fig2, ax2 = plt.subplots()

    ax2.set_title("Average node count in largest component")
    ax2.set_xlabel("Iterations")
    ax2.set_ylabel("Number of nodes [%]")
    ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.plot(iterations, listOfAveragesLargestComponent)

    plt.savefig("aaaa/largestComponent.png")

def strFromFileToLists(filePath):
    file = open(filePath, "r")
    lists = []
    
    for line in file:
        numbersStr = line[1:-2].split(",")
        list = [float(num.strip()) for num in numbersStr]
        lists.append(list)
        
    file.close()

    return lists

def normalizeData(filePath):
    dataList = strFromFileToLists(filePath)
    normalizedLists = []

    for list in dataList:
        normalizedList = []
        initialData = list[0]

        for data in list:
            normalizedList.append(100 * data / initialData)

        normalizedLists.append(normalizedList)

    return normalizedLists