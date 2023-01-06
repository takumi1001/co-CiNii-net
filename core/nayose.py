
# Researcherの名寄せ対応版

"""
名寄せアルゴリズム
1.形態素解析でヘボン式ローマ字にする
2.小文字に変換し、記号を除去
3.文字列をソート
"""


import re

import pykakasi
from rdflib import URIRef

from core.base import Researcher, Work

class NayosedResearcher(Researcher):

    def __init__(self, resource: URIRef, name: str) -> None:
        super().__init__(resource, name)
        self.__nayose_string :str = None 
        self.__kks = pykakasi.kakasi()
        self.__pat = re.compile(r"[^a-z]")

    def __eq__(self, other) -> bool:
        if not isinstance(other, NayosedResearcher):
            return False
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        if not self.__nayose_string:
            self.__set_nayose_string()
        return hash(self.__nayose_string)

    def get_node_id(self) -> str:
        if not self.__nayose_string:
            self.__set_nayose_string()
        return self.__nayose_string

    def __set_nayose_string(self) -> None:
        result = self.__kks.convert(self.name)
        romans = ""
        for item in result:
            romans += item["hepburn"]
        only_lower_alphabets = self.__pat.sub("", romans.lower())
        self.__nayose_string = "".join(sorted(only_lower_alphabets))
        if self.__nayose_string == "":
            # 中国人の方などは変換に失敗することがあるので、その場合は元の名前を使う
            # idが空だとGephiでエラーになる
            print("Failed to convert to nayose string: " + self.name)
            print("Use original name as nayose string instead.")
            self.__nayose_string = self.name

    def create_work(self, source: URIRef, rdftype: URIRef) -> "NayosedWork":
        return NayosedWork(source, rdftype)
        
class NayosedWork(Work):
    def create_researcher(self, source: URIRef, name :str) -> NayosedResearcher:
        return NayosedResearcher(source, name)