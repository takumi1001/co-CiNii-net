import networkx as nx
from networkx.algorithms import community

from typing import List, Set

def louvain_clustering(G :nx.Graph, *, resolution :float = 1) -> None:
    """Clustering nodes and set cluster number to node attribute 'cluster' by Louvian method."""
    partition = community.louvain_communities(G, resolution=resolution)
    for i, cluster in enumerate(partition):
        for node in cluster:
            G.nodes[node]["cluster"] = i
 