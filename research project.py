from datasketch import MinHash, MinHashLSH
import process_data as pd
import networkx as nx

threshold = 6
instP = '012'
instQ = '070'

# Gp = nx.DiGraph()
# Gp.add_nodes_from(['a', 'b', 'c', 'd', 'f', 'x', 'y'])
# Gp.add_edges_from([
#     ('a', 'b', {'a': 100.0, 'c': 0}),
#     ('b', 'c', {'a': 200.0, 'c': 0}),
#     ('c', 'd', {'a': 300.0, 'c': 1}),
#     ('f', 'a', {'a': 400.0, 'c': 1}),
#     ('b', 'x', {'a': 400.0, 'c': 0}),
#     ('x', 'y', {'a': 400.0, 'c': 1}),
# ])
#
# Gq = nx.DiGraph()
# Gq.add_nodes_from(['a', 'c', 'd', 'e', 'f', 'x', 'y'])
# Gq.add_edges_from([
#     ('c', 'd', {'a': 300.0, 'c': 1}),
#     ('d', 'e', {'a': 400.0, 'c': 0}),
#     ('e', 'f', {'a': 500.0, 'c': 0}),
#     ('f', 'a', {'a': 200.0, 'c': 1}),
#     ('e', 'y', {'a': 400.0, 'c': 0}),
#     ('x', 'y', {'a': 400.0, 'c': 1}),
#
# ])

Gp, Gq = pd.createGraphs(instP, instQ)

def get_minhash(s, num_perm=128):
    m = MinHash(num_perm=num_perm)
    for item in s:
        m.update(item.encode('utf8'))
    return m

def citSetDiscovery(node, graph, depth):
    citNodesSet = set()
    visitedNodes = set()
    queue = {node}
    for _ in range(depth):
        next_queue = set()
        for current_node in queue:
            if current_node not in visitedNodes:
                visitedNodes.add(current_node)
            for neighbor in graph.neighbors(current_node):
                edge_data = graph.get_edge_data(current_node, neighbor)
                if edge_data['c'] == 1:
                    citNodesSet.add(neighbor)
                elif neighbor not in visitedNodes:
                    next_queue.add(neighbor)
        if not next_queue:
            break
        queue = next_queue
    return citNodesSet

def citSetDiscoveryLocal(node, graph, depth):
    citNodesSet = set()
    visitedNodes = set()
    queue = {node}
    for _ in range(depth):
        next_queue = set()
        for current_node in queue:
            if current_node not in visitedNodes:
                visitedNodes.add(current_node)
            neighbors = graph.neighbors(current_node)
            for neighbor in neighbors:
                edge_data = graph.get_edge_data(current_node, neighbor)
                if edge_data['c'] == 1:
                    citNodesSet.add(current_node)
                elif neighbor not in visitedNodes:
                    next_queue.add(neighbor)
        if not next_queue:
            break
        queue = next_queue
    return citNodesSet

def instPartOne(G):
    return createLSH(G)

def createLSH(G):
    allOutMinhashes = {}
    allInMinhashes = {}
    counter = 0
    for node in G.nodes():
        counter += 1
        if counter % 10 == 0:
            print("Processed", counter, "nodes.")
        citOutgoing = citSetDiscovery(node, G, threshold)
        if not citOutgoing:
            continue
        citIncoming = citSetDiscovery(node, G.reverse(), threshold)
        # print("CIT nodes detected for node " + node + ":", len(citOutgoing), "outgoing and", len(citIncoming), "incoming.")
        if not citIncoming:
            continue
        # print("CIT nodes:", citOutgoing, citIncoming)
        allOutMinhashes[node] = get_minhash(citOutgoing)
        allInMinhashes[node] = get_minhash(citIncoming)

    # print(allOutMinhashes)
    # print(allInMinhashes)

    lsh_O = MinHashLSH(threshold=0.01, num_perm=128)
    lsh_I = MinHashLSH(threshold=0.01, num_perm=128)

    for node, minhash in allOutMinhashes.items():
        lsh_O.insert(f"{node}", minhash)
    for node, minhash in allInMinhashes.items():
        lsh_I.insert(f"{node}", minhash)
    return lsh_O, lsh_I


def query(G, node, otherLSHOut, otherLSHIn):
    outgoing_cit = citSetDiscoveryLocal(node, G, threshold)
    incoming_cit = citSetDiscoveryLocal(node, G.reverse(), threshold)
    # print("Outgoing CIT nodes for node", node, ":", outgoing_cit)
    # print("Incoming CIT nodes for node", node, ":", incoming_cit)
    # print("1")
    outMinhash = get_minhash(outgoing_cit)
    inMinhash = get_minhash(incoming_cit)
    # print("2")

    candidates_out = otherLSHOut.query(inMinhash) 
    candidates_in = otherLSHIn.query(outMinhash)
    # print("3")
    print(candidates_in, candidates_out)
    return not (set(candidates_in) & set(candidates_out)) == set()
    


def instPartTwo(G, lshQOut, lshQIn):
    results = set()
    nodeLength = len(G.nodes)
    counter = 0
    print(str(nodeLength) + " total nodes")
    for node in G.nodes():
        bool = query(G, node, lshQOut, lshQIn)
        # print("4")
        counter += 1
        print(str(counter) + " nodes checked out of " + str(nodeLength) + " total nodes")
        if bool:
            results.add(node)
            # print(node, " is in a cycle.")
        else:
            # print(node, " is not in a cycle.")
            continue
    print("number of nodes in cycles: " + str(len(results)) + " out of " + str(nodeLength) + " total nodes.")
    print("Nodes in cycles:", results)


print("Starting inst P p1")
lshQOut, lshQIn = instPartOne(Gq)
print("Starting inst P p2")
instPartTwo(Gp, lshQOut, lshQIn)

print("Starting inst Q p1")
lshPOut, lshPIn = instPartOne(Gp)
print("Starting inst Q p2")
instPartTwo(Gq, lshPOut, lshPIn)

