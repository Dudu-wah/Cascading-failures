from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt

def calculateAverageNodeCounts(totalCountPath, largestComponentPath):
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

    return iterations, listOfAveragesTotal, listOfAveragesLargestComponent

def plotNodeCount(nodesPathsList, labels):
    fig1, ax1 = plt.subplots()
    ax1.set_title("Average node count")
    ax1.set_xlabel("Iterations")
    ax1.set_ylabel("Number of nodes [%]")
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

    fig2, ax2 = plt.subplots()
    ax2.set_title("Average node count in largest component")
    ax2.set_xlabel("Iterations")
    ax2.set_ylabel("Number of nodes [%]")
    ax2.xaxis.set_major_locator(MaxNLocator(integer=True))

    labelCounter = 0
    for paths in nodesPathsList:
        iterations, listOfAveragesTotal, listOfAveragesLargestComponent = calculateAverageNodeCounts(paths[0], paths[1])
        ax1.plot(iterations, listOfAveragesTotal, label=labels[labelCounter][0])
        ax2.plot(iterations, listOfAveragesLargestComponent, label=labels[labelCounter][1])
        labelCounter += 1

    ax1.legend()
    ax2.legend()
    fig1.savefig("aaaa/total.png")
    fig2.savefig("aaaa/largestComponent.png")


def calculateAverageEfficiencies(filePath):
    file = open(filePath, "r")
    efficienciesList = normalizeData(filePath)

    listOfAverages = []
    iterations = [i for i in range(len(max(efficienciesList, key=len)))]
    for iteration in iterations:
        efficienciesInIteration = 0
        averageEfficiency = 0

        for list in efficienciesList:
            if iteration < len(list):
                efficienciesInIteration += 1
                averageEfficiency += list[iteration]

        averageEfficiency = round(averageEfficiency / efficienciesInIteration, 2)
        listOfAverages.append(averageEfficiency)

    file.close()

    return iterations, listOfAverages

def plotEfficiencies(efficienciesPathsList, labels):
    fig, ax = plt.subplots()
    ax.set_title("Average network efficiency")
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Global efficiency [%]")
    #plt.ylim((0, 101))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    labelCounter = 0
    for path in efficienciesPathsList:
        iterations, listOfAverages = calculateAverageEfficiencies(path)
        ax.plot(iterations, listOfAverages, label=labels[labelCounter])
        labelCounter += 1

    plt.legend()
    plt.savefig("aaaa/efficiency.png")

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

removeType = "20%LargestHubs"
initialNodeCount = 1000
tolerance = 0.4
#probability = 0.2

filePath1 = f"ErdosRenyi/NodesData/TotalNodeCount/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{0.1*100}%.txt"
filePath2 = f"ErdosRenyi/NodesData/LargestComponentsNodeCount/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{0.1*100}%chance.txt"
filePath3 = f"ErdosRenyi/NodesData/TotalNodeCount/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{0.2*100}%.txt"
filePath4 = f"ErdosRenyi/NodesData/LargestComponentsNodeCount/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{0.2*100}%chance.txt"
filePath5 = f"ErdosRenyi/NodesData/TotalNodeCount/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{0.4*100}%.txt"
filePath6 = f"ErdosRenyi/NodesData/LargestComponentsNodeCount/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{0.4*100}%chance.txt"
filePath7 = f"ErdosRenyi/NodesData/TotalNodeCount/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{0.5*100}%.txt"
filePath8 = f"ErdosRenyi/NodesData/LargestComponentsNodeCount/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{0.5*100}%chance.txt"

labels = [["10% chance", "10% chance"], ["20% chance", "20% chance"], ["40% chance", "40% chance"], ["50 chance", "50% chance"]]

nodesPathsList = [[filePath1, filePath2], [filePath3, filePath4], [filePath5, filePath6], [filePath7, filePath8]]

efilePath1 = f"ErdosRenyi/efficienciesData/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{0.1*100}%chance.txt"
efilePath2 = f"ErdosRenyi/efficienciesData/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{0.2*100}%chance.txt"
efilePath3 = f"ErdosRenyi/efficienciesData/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{0.4*100}%chance.txt"
efilePath4 = f"ErdosRenyi/efficienciesData/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{0.5*100}%chance.txt"

eLabels = ["10% chance", "20% chance", "40% chance", "50% chance"]

efficienciesPathsList = [efilePath1, efilePath2, efilePath3, efilePath4]

plotNodeCount(nodesPathsList, labels)
plotEfficiencies(efficienciesPathsList, eLabels)