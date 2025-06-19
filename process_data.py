import csv
import networkx as nx
from pyvis.network import Network


def sortBanks():
    reader = csv.reader(open('HI-Small_Trans.csv', 'r'))
    data = [row for row in reader]

    fromdict = {}
    todict = {}
    for row in data:
        sourceBank = row[1]
        targetBank = row[3]
        if not sourceBank in fromdict:
            fromdict[sourceBank] = 1
        else:
            fromdict[sourceBank] += 1
        if not sourceBank in todict:
            todict[sourceBank] = 1
        else:
            todict[sourceBank] += 1
        if not targetBank in fromdict:
            fromdict[targetBank] = 1
        else:
            fromdict[targetBank] += 1
        if not targetBank in todict:
            todict[targetBank] = 1
        else:
            todict[targetBank] += 1
    print("from")
    sorted_items_from = sorted(fromdict.items(), key=lambda item: item[1], reverse=True)[:10]
    for key, value in sorted_items_from:
        print(f"{key}: {value}")
    print("to")
    sorted_items_to = sorted(todict.items(), key=lambda item: item[1], reverse=True)[:10]
    for key, value in sorted_items_to:
        print(f"{key}: {value}")


def createGraphs(instP, instQ):
    reader = csv.reader(open('HI-Small_Trans.csv', 'r'))
    header = next(reader)
    data = [row for row in reader]

    Gp = nx.DiGraph()
    Gq = nx.DiGraph()
    for row in data:
        sourceBank = row[1]
        targetBank = row[3]
        sourceAccount = row[2]
        targetAccount = row[4]
        # if sourceBank != instP and sourceBank != instQ:
        #     continue
        # if targetBank != instP and targetBank != instQ:
        #     continue
        if sourceBank == instP or targetBank == instP:
            if sourceBank == targetBank:
                Gp.add_edge(sourceAccount, targetAccount, a=float(row[5]), c=0)
                print("p to p")
            else:
                Gp.add_edge(sourceAccount, targetAccount, a=float(row[5]), c=1)
                print("p to q")
        if sourceBank == instQ or targetBank == instQ:
            if sourceBank == targetBank:
                Gq.add_edge(sourceAccount, targetAccount, a=float(row[5]), c=0)
                print("q to q")
            else:
                Gq.add_edge(sourceAccount, targetAccount, a=float(row[5]), c=1)
                print("q to p")
    print(len(Gp.nodes), len(Gq.nodes))
    return Gp, Gq


def visualise_graph(graph, filename='graph.html'):
    net = Network(
        directed=True,
        select_menu=True,
        filter_menu=True,
    )
    net.show_buttons()
    net.from_nx(graph)
    net.show(filename, notebook=False)


# gp, gq = createGraphs("0116", "0211")
# print(len(gp.nodes()))
# print(len(gq.nodes()))
# visualise_graph(gp, "test_gp.html")
# visualise_graph(gq, "test_gq.html")
# sortBanks()
