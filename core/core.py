from rdflib import RDF, URIRef, Literal, FOAF, Graph
from rdflib.namespace import Namespace

from typing import List, Set

class Researcher:

    # class variables
    NS_CINII = Namespace("https://cir.nii.ac.jp/schema/1.0/")
    NS_DC = Namespace("http://purl.org/dc/elements/1.1/")  
    WORKTYPES = [
        NS_CINII.Article,
        NS_CINII.Book,
        NS_CINII.Dissertation,
        NS_CINII.Dataset,
        NS_CINII.Product,
    ]

    def __init__(self, resource: URIRef, name :str) -> None:
        self.resouse = resource
        self.name = name 

        self.graph = Graph()
        self.parsed = False

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        return self.resouse == other.resouse

    def __hash__(self) -> int:
        return hash(self.resouse)

    def getURI(self) -> str:
        return str(self.resouse)

    def parse(self) -> Graph:
        ret = self.graph.parse(str(self.resouse))
        self.parsed = True
        return ret

    def set_works(self) -> None:
        if not self.parsed:
            self.parse()
        self.works :Set[Work] = set()
        for worktype in self.WORKTYPES:
            for s, p, t in self.graph.triples((None, None, worktype)):
                work = Work(s, t) 
                self.works.add(work)

    def get_works(self) -> Set["Work"]:
        if not hasattr(self, "works"):
            self.set_works()
        return self.works


class Work:

    # class variables
    NS_CINII = Namespace("https://cir.nii.ac.jp/schema/1.0/")
    NS_DC = Namespace("http://purl.org/dc/elements/1.1/")

    def __init__(self, resource: URIRef, rdftype: URIRef) -> None:
        self.resouse = resource
        self.type = rdftype
        self.graph = Graph()
        self.parsed = False

    def parse(self) -> Graph:
        ret = self.graph.parse(str(self.resouse))
        self.parsed = True
        return ret

    def __str__(self) -> str:
        return str(self.resouse)

    def __eq__(self, other) -> bool:
        return self.resouse == other.resouse

    def __hash__(self) -> int:
        return hash(self.resouse)

    def set_title(self, title: str = None) -> None:
        if title is None:
            if not self.parsed:
                self.parse()
            titles = list(self.graph.triples((None, self.NS_DC.title, None)))
            self.title = str(titles[0][2])
        else:
            self.title = title
        return

    def get_title(self) -> str:
        if not hasattr(self, "title"):
            self.set_title()
        return self.title

    def get_type(self) -> URIRef:
        return self.type

    def getURI(self) -> str:
        return str(self.resouse)

    def set_authers(self) -> None:
        if not self.parsed:
            self.parse()
        self.authers: Set[Researcher] = set()
        for s, p, t in self.graph.triples((None, None, self.NS_CINII.Researcher)):
            auther = Researcher(s, "dummy")
            self.authers.add(auther)

    def get_authers(self) -> Set[Researcher]:
        if not hasattr(self, "authers"):
            self.set_authers()
        return self.authers
