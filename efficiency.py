from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt

def writeToFile(efficienciesList, initialNodeCount, tolerance, preferentialAttachment, removeType):
    filePath = f"EfficienciesData/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{preferentialAttachment}PA.txt"
    file = open(filePath, "a+")
    file.write(f"{efficienciesList}\n")
    file.close()

def averagesPlot(filePath):
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

    fig, ax = plt.subplots()

    ax.set_title("Average network efficiency")
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Global efficiency [%]")
    #plt.ylim((0, 101))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.plot(iterations, listOfAverages)

    # plt.show()
    plt.savefig("aaaa/efficiency.png")

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

def strFromFileToLists(filePath):
    file = open(filePath, "r")
    lists = []
    
    for line in file:
        numbersStr = line[1:-2].split(",")
        list = [float(num.strip()) for num in numbersStr]
        lists.append(list)
        
    file.close()

    return lists

def attackOrFailureAccumulator(efficiency, removeType, initialNodeCount, tolerance, preferentialAttachment):
    filePath = f"AttackOrFailures/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{preferentialAttachment}PA.txt"
    file = open(filePath, "a+")
    file.write(f"{efficiency}\n")
    file.close()

def attackOrFailurePlot(filePath, percentStep):
    file = open(filePath, "r")

    efficienciesList = file.readlines()

    fig, ax = plt.subplots()

    ax.set_title("Attack / Failures")
    ax.set_xlabel("Initial nodes removed [%]")
    ax.set_ylabel("Network efficiency [%]")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.plot(percentStep, efficienciesList)

    plt.show()
