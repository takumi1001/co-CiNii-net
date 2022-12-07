import time

import networkx as nx
from rdflib import URIRef

from core import Researcher, Work

from typing import List, Set


class CoCiNiiNetWork:

    def __init__(self, uri: str, name: str) -> None:
        self.first_node = Researcher(URIRef(uri), name)
        self.G = nx.Graph()

        self.add_node(self.first_node)

    def add_node(self, node: Researcher) -> None:
        self.G.add_node(node, label=node.name)

    def add_edge(self, node1: Researcher, node2: Researcher, work: Work) -> None:
        self.G.add_edge(node1, node2, label=work.title)

    def generate(self, max_reqests: int = 100) -> None:
        self.__generate(self.first_node, max_reqests=max_reqests)

    def __generate(self, node: Researcher, max_reqests: int = 100) -> None:
        reqests_count = 1
        new_nodes: List[Researcher] = []
        for authers in self.first_node.get_works():
            reqests_count += 1
            for auther in authers.get_authers():
                if auther == node.resouse:
                    continue
                if auther not in self.G.nodes:
                    self.add_node(auther)
                    new_nodes.append(auther)
                self.add_edge(node, auther)
                reqests_count += 1
                if reqests_count > max_reqests:
                    return
                else:
                    time.sleep(1)
        for new_node in new_nodes:
            self.__generate(new_node, max_reqests=max_reqests-reqests_count)

    def write_graphml(self, filename: str) -> None:
        nx.write_graphml(self.G, filename)


if __name__ == "__main__":
    net = CoCiNiiNetWork("G.add_node(FIRST_NODE, label=get_node_name(first_g))", "田村匠")
    net.generate(max_reqests=3)
    net.write_graphml("test.graphml")
