import time

from tqdm import tqdm
import networkx as nx
from rdflib import URIRef
from core.base import Researcher, Work
from core.nayose import NayosedResearcher

from typing import List, Set

class MaxReqestsSentException(Exception):
    pass

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
        self.G.add_node(hash(node), label=node.name, resource=node.getURI())

    def add_edge(self, node1: Researcher, node2: Researcher, work: Work) -> None:
        self.G.add_edge(hash(node1), hash(node2), label=work.get_title(), resource=work.getURI())

    def generate(self, max_reqests: int = 100) -> None:
        self.visited_works : Set[Work] = set()
        self.__reqests_count = 0
        self.__pbar = tqdm(total=max_reqests)
        try:
            self.__generate(self.first_node, max_reqests=max_reqests)
        except MaxReqestsSentException:
            pass
        finally:
            self.__pbar.close()

    def __generate(self, node: Researcher, max_reqests: int = 100) -> bool:

        def count_request_and_wait() -> None:
            if self.__reqests_count >= max_reqests:
                raise MaxReqestsSentException
            self.__reqests_count += 1
            self.__pbar.update(1)
            time.sleep(self.wait_seconds)

        new_nodes: List[Researcher] = []

        count_request_and_wait()
        for work in node.get_works(): # GET request sent here
            if work in self.visited_works:
                continue
            else:
                self.visited_works.add(work)
            count_request_and_wait()
            for auther in work.get_authers(): # GET request sent here
                if auther == node:
                    continue
                if hash(auther) not in self.G.nodes:
                    self.add_node(auther)
                    new_nodes.append(auther)
                self.add_edge(node, auther, work)
        
        for new_node in new_nodes:
            self.__generate(new_node, max_reqests=max_reqests)

    def write_graphml(self, filename: str) -> None:
        nx.write_graphml(self.G, filename)
