import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import choose, efficiency, evolution
import sys

def calculateLoads(graph):
    nodesLoad = nx.betweenness_centrality(graph)             
    return nodesLoad

def firstFailure(simulations, tolerance, initialNodeCount, preferentialAttachment, removeType, generator, probability, powerLawParameter, numberOfNodesToRemove=None):
    for simulation in range(simulations):
        #print("Simulação:", simulation)

        graph = chooseGraphGenerator(generator, initialNodeCount, preferentialAttachment, probability, powerLawParameter)
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

        elif removeType == "10%LargestHubs":
            nodes = choose.highestDegreesNodes(graph, int(0.1*initialNodeCount))

        elif removeType == "20%LargestHubs":
            nodes = choose.highestDegreesNodes(graph, int(0.2*initialNodeCount))

        elif removeType == "30%LargestHubs":
            nodes = choose.highestDegreesNodes(graph, int(0.3*initialNodeCount))

        else:
            print("Create new folder for this case!")
            return 0

        #degreeDistribution(graph, "initial degree histogram", "Initial")

        initialLoad = calculateLoads(graph)
        
        graph.remove_nodes_from(nodes)

        newLoad = calculateLoads(graph)

        overloadCheck(graph, initialLoad, newLoad, tolerance, initialNodeCount, preferentialAttachment, removeType, probability, powerLawParameter)

    #printResults(graph)

    return graph

def removeNodeFromInitialLoadList(initialLoad, newLoad):
    newInitialLoad = initialLoad.copy()

    for node in initialLoad:
        if node not in newLoad:
            newInitialLoad.pop(node, None)

    return newInitialLoad

def overloadCheck(graph, startingLoad, newLoad, tolerance, initialNodeCount, preferentialAttachment, removeType, probability, powerLawParameter):
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
        
        if graph.number_of_nodes() != 0:
            nodesInLargestComponent = len(max(nx.connected_components(graph), key=len))
        else:
            nodesInLargestComponent = 0
        
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
        efficiency.writeToFile(efficienciesList, initialNodeCount, tolerance, preferentialAttachment, removeType, probability, powerLawParameter)
        evolution.writeNodesToFile(nodeCountList, nodesInLargestComponentList, initialNodeCount, tolerance, preferentialAttachment, removeType, probability, powerLawParameter)

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

def chooseGraphGenerator(generator, initialNodeCount, preferentialAttachment, probability, powerLawParameter):
    if generator == "barabasiAlbert":
        graph = nx.barabasi_albert_graph(initialNodeCount, preferentialAttachment)
    
    elif generator == "erdosRenyi":
        graph = nx.erdos_renyi_graph(initialNodeCount, probability)

    elif generator == "configurationModel":
        degreeSequence = powerLawIntegerSequence(powerLawParameter, initialNodeCount)
        graphMulti = nx.configuration_model(degreeSequence)

        graph = nx.Graph(graphMulti)
        graph.remove_edges_from(nx.selfloop_edges(graph))

    return graph

def powerLawIntegerSequence2(powerLawParameter, maxSum):
    sum = 0
    degree = 1
    sequence = []

    while sum < maxSum:
        current = max(1, int(round(degree ** powerLawParameter)))
        sum += current
        sequence.append(current)

        if sum > 0.995 * maxSum or (sum >= 0.98 * maxSum and maxSum < 200):
            sequence.append(int(maxSum - sum))
            break

        degree += 1

    return sequence

def powerLawIntegerSequence(powerLawParameter, nodeCount):
    sequence = [int(degreeCount) for degreeCount in nx.utils.powerlaw_sequence(nodeCount, powerLawParameter)]

    if sum(sequence) % 2 != 0:
        sequence[-1] += 1

    return sequence

generator = "configurationModel"
initialNodeCount = int(sys.argv[1])
tolerance = float(sys.argv[3])
removeType = sys.argv[4]
simulations = 100
randomNodesToRemove = int(sys.argv[5])

# initialNodeCount = 1000
# tolerance = 0.4
# removeType = "3LargestHubs"
# simulations = 1
# randomNodesToRemove = 100

preferentialAttachment = None
powerLawParameter = None
probability = None
if generator == "barabasiAlbert":
    preferentialAttachment = int(sys.argv[2])
    filePath = f"Barabasi/EfficienciesData/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{preferentialAttachment}PA.txt"
    
elif generator == "erdosRenyi":
    probability = float(sys.argv[2])
    filePath = f"ErdosRenyi/EfficienciesData/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{probability*100}%chance.txt"

elif generator == "configurationModel":
    powerLawParameter = float(sys.argv[2])
    filePath = f"ConfigurationModel/EfficienciesData/{removeType}/{initialNodeCount}Nodes_{int(tolerance*100)}%tolerance_{powerLawParameter}gamma.txt"


firstFailure(simulations, tolerance, initialNodeCount, preferentialAttachment, removeType, generator, probability, powerLawParameter, randomNodesToRemove)

#efficiency.averagesPlot(filePath)