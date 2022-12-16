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
        self.resource = resource
        self.name = name 

        self.graph = Graph()
        self.parsed = False

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        if not isinstance(other, Researcher):
            return False
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        return hash(self.resource)

    def get_node_id(self) -> str:
        return str(self.resource)

    def getURI(self) -> str:
        return str(self.resource)

    def parse(self) -> Graph:
        ret = self.graph.parse(str(self.resource))
        self.parsed = True
        return ret

    def set_works(self) -> None:
        if not self.parsed:
            self.parse()
        self.works :Set[Work] = set()
        for worktype in self.WORKTYPES:
            for s, p, t in self.graph.triples((None, None, worktype)):
                work = self.create_work(s, t)
                self.works.add(work)

    def create_work(self, source: URIRef, rdftype: URIRef) -> "Work":
        return Work(source, rdftype)

    def get_works(self) -> Set["Work"]:
        if not hasattr(self, "works"):
            self.set_works()
        return self.works


class Work:

    # class variables
    NS_CINII = Namespace("https://cir.nii.ac.jp/schema/1.0/")
    NS_DC = Namespace("http://purl.org/dc/elements/1.1/")

    def __init__(self, resource: URIRef, rdftype: URIRef) -> None:
        self.resource = resource
        self.type = rdftype
        self.graph = Graph()
        self.parsed = False

    def parse(self) -> Graph:
        ret = self.graph.parse(str(self.resource))
        self.parsed = True
        return ret

    def __str__(self) -> str:
        return str(self.resource)

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        return hash(self.resource)

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
        return str(self.resource)

    def set_authers(self) -> None:
        if not self.parsed:
            self.parse()
        self.authers: Set[Researcher] = set()
        for s, p, t in self.graph.triples((None, None, self.NS_CINII.Researcher)):
            auther = self. create_researcher(s, self.__get_auther_name(s))
            self.authers.add(auther)

    def create_researcher(self, source: URIRef, name :str) -> Researcher:
        return Researcher(source, name)

    def __get_auther_name(self, auther: URIRef) -> str:
        if not self.parsed:
            self.parse()
        return str(self.graph.value(auther, FOAF.name))

    def get_authers(self) -> Set[Researcher]:
        if not hasattr(self, "authers"):
            self.set_authers()
        return self.authers
