import time

from tqdm import tqdm
import networkx as nx
from rdflib import URIRef
from core.base import Researcher, Work
from core.nayose import NayosedResearcher

from typing import List, Set

class CoCiNiiNet:

    def __init__(self, uri: str, name: str, wait_seconds :int = 1, is_nayose = True) -> None:
        if is_nayose:
            self.first_node = NayosedResearcher(URIRef(uri), name)
        else:
            self.first_node = Researcher(URIRef(uri), name)
        self.G = nx.Graph()
        self.add_node(self.first_node)
        self.wait_seconds = wait_seconds

    def add_node(self, node: Researcher) -> None:
        self.G.add_node(node.get_node_id(), label=node.name, resource=node.getURI())

    def add_edge(self, node1: Researcher, node2: Researcher, work: Work) -> None:
        self.G.add_edge(node1.get_node_id(), node2.get_node_id(), label=work.get_title(), resource=work.getURI())

    def generate(self) -> None:
        self.visited_works : Set[Work] = set()
        self.new_nodes : List[Researcher] = []

        self.__generate(self.first_node, is_update_new_nodes=True, desc="[EGO]")
        for i, new_node in enumerate(self.new_nodes):
            desc = f"[{i+1}/{len(self.new_nodes)}]" 
            self.__generate(new_node, is_update_new_nodes=False, desc=desc)

    def __generate(self, node: Researcher, is_update_new_nodes :bool, desc :str) -> None:
        time.sleep(self.wait_seconds)
        for work in tqdm(node.get_works(), desc=desc): # GET request sent here
            if work in self.visited_works:
                continue
            else:
                self.visited_works.add(work)

            time.sleep(self.wait_seconds)
            for auther in work.get_authers(): # GET request sent here
                if auther == node:
                    continue
                if hash(auther) not in self.G.nodes:
                    self.add_node(auther)
                    if is_update_new_nodes:
                        self.new_nodes.append(auther)
                self.add_edge(node, auther, work)

    def write_graphml(self, filename: str) -> None:
        nx.write_graphml(self.G, filename)
