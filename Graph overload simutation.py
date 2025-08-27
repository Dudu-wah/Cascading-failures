import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import choose, efficiency, evolution
import sys

def calculateLoads(graph):
    nodesLoad = nx.betweenness_centrality(graph)             
    return nodesLoad

def firstFailure(simulations, tolerance, initialNodeCount, preferentialAttachment, removeType, generator, probability, degreeSequence, numberOfNodesToRemove=None):
    for simulation in range(simulations):
        #print("Simulação:", simulation)

        graph = chooseGraphGenerator(generator, initialNodeCount, preferentialAttachment, probability, degreeSequence)
        hubs = choose.highestDegreesNodes(graph, 3)
        #print("Largest hubs:", hubs)

        if removeType == "RandomFailures":
            nodes = choose.randomNodes(numberOfNodesToRemove, initialNodeCount)

        elif removeType == "LargestHub":
            nodes = choose.highestDegreesNodes(graph, 1)

        elif removeType == "3LargestHubs":
            nodes = choose.highestDegreesNodes(graph, 3)

        elif removeType == "5LargestHubs":
            nodes = choose.highestDegreesNodes(graph, 5)

        else:
            print("Create new folder for this case!")
            return 0

        #degreeDistribution(graph, "initial degree histogram", "Initial")

        initialLoad = calculateLoads(graph)
        
        graph.remove_nodes_from(nodes)

        newLoad = calculateLoads(graph)

        overloadCheck(graph, initialLoad, newLoad, tolerance, initialNodeCount, preferentialAttachment, removeType)

    #printResults(graph)

    return graph

def removeNodeFromInitialLoadList(initialLoad, newLoad):
    newInitialLoad = initialLoad.copy()

    for node in initialLoad:
        if node not in newLoad:
            newInitialLoad.pop(node, None)

    return newInitialLoad

def overloadCheck(graph, startingLoad, newLoad, tolerance, initialNodeCount, preferentialAttachment, removeType):
    nodesToRemove = []
    efficienciesList = []
    nodeCountList = []
    nodesInLargestComponentList = []
    iteration = 0

    while len(nodesToRemove) != 0 or iteration == 0:
        #print(iteration)

        currentEfficiency = round(nx.global_efficiency(graph) * 100, 2)
        efficienciesList.append(currentEfficiency)

        currentNodeCount = graph.number_of_nodes()
        nodeCountList.append(currentNodeCount)
        
        nodesInLargestComponent = len(max(nx.connected_components(graph), key=len))
        nodesInLargestComponentList.append(nodesInLargestComponent)

        nodesToRemove = []
        initialLoad = removeNodeFromInitialLoadList(startingLoad, newLoad)

        for node in initialLoad:
                if newLoad[node] >= initialLoad[node] * (1 + tolerance) and newLoad[node] != 0:
                    nodesToRemove.append(node)

        graph.remove_nodes_from(nodesToRemove)

        iteration += 1
        startingLoad = newLoad
        newLoad = calculateLoads(graph)

    if removeType == "Attack" or removeType == "Failures":
        efficiency.attackOrFailureAccumulator(currentEfficiency, removeType, initialNodeCount, tolerance, preferentialAttachment)

    else:
        #evolution.networkEfficiency(efficienciesList)
        #evolution.nodeCount(nodeCountList)
        #evolution.largestComponentsNodeCount(nodesInLargestComponentList)
        efficiency.writeToFile(efficienciesList, initialNodeCount, tolerance, preferentialAttachment, removeType)
        evolution.writeNodesToFile(nodeCountList,nodesInLargestComponentList,initialNodeCount,tolerance,preferentialAttachment,removeType)

    return graph

def degreeDistribution(graph, fileName, time):
    fig, ax = plt.subplots()

    histogram = nx.degree_histogram(graph)
    degrees = [i for i in range(len(histogram))]

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax.bar(degrees, histogram)
    ax.set_title(f"{time} degree histogram")
    ax.set_xlabel("Degree")
    ax.set_ylabel("# of Nodes")

    plt.savefig(f"Graphs/{fileName}.png")

def printResults(graph):
    print("The new graph has", len(list(graph.nodes)), "nodes")
    print("Highest degree nodes:", choose.highestDegreesNodes(graph, 3))

    print("New graph has", nx.number_connected_components(graph), "components")
    largestComponent = max(nx.connected_components(graph), key=len)
    print("Largest component has", len(largestComponent), "nodes")

    degreeDistribution(graph, "final degree histogram", "Final")

def attackOrFailuresProgression(tolerance, initialNodeCount, preferentialAttachment, removeType, simulations):
    for simulation in range(simulations):
        print("Simulação:", simulation)

        graph = nx.barabasi_albert_graph(initialNodeCount, preferentialAttachment)
        hubs = choose.highestDegreesNodes(graph, 3)
        print("Largest hubs:", hubs)

        for percentageRemoved in range(0, initialNodeCount, 100/initialNodeCount):
            if removeType == "Failures":
                nodes = choose.randomNodes(int(percentageRemoved * initialNodeCount), initialNodeCount)

            elif removeType == "Attack":
                nodes = choose.highestDegreesNodes(graph, int(percentageRemoved * initialNodeCount))

            else:
                print("Create new folder for this case!")
                return 0

            initialLoad = calculateLoads(graph)
            
            graph.remove_nodes_from(nodes)

            newLoad = calculateLoads(graph)

            overloadCheck(graph, initialLoad, newLoad, tolerance, initialNodeCount, preferentialAttachment, removeType)

def chooseGraphGenerator(generator, initialNodeCount, preferentialAttachment, probability, degreeSequence):
    if generator == "barabasiAlbert":
        graph = nx.barabasi_albert_graph(initialNodeCount, preferentialAttachment)
    
    elif generator == "erdosRenyi":
        graph = nx.erdos_renyi_graph(initialNodeCount, probability)

    elif generator == "configurationModel":
        graph = nx.configuration_model(initialNodeCount, degreeSequence)

    return graph

generator = "erdosRenyi"
initialNodeCount = int(sys.argv[1])
tolerance = float(sys.argv[3])
removeType = sys.argv[4]
simulations = 100
randomNodesToRemove = int(sys.argv[5])

preferentialAttachment = None
degreeSequence = None
probability = None
if generator == "barabasiAlbert":
    preferentialAttachment = int(sys.argv[2])
    filePath = f"Barabasi/EfficienciesData/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{preferentialAttachment}PA.txt"
    
elif generator == "erdosRenyi":
    probability = float(sys.argv[2])
    filePath = f"ErdosRenyi/EfficienciesData/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{probability*100}%chance.txt"

elif generator == "configurationModel":
    degreeSequence = float(sys.argv[2])
    filePath = f"ConfigurationModel/EfficienciesData/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{probability*100}%chance.txt"


firstFailure(simulations, tolerance, initialNodeCount, preferentialAttachment, removeType, generator, probability, degreeSequence, randomNodesToRemove)

#efficiency.averagesPlot(filePath)