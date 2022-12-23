# グラフの合成
import networkx as nx

"""
CoCiNiiNetクラスのGメンバはnx.Graphを返すため、これも利用できる。
しかしながら、一度データをエクスポートすることが推奨される。
"""

# https://cir.nii.ac.jp/crid/1420003854341602816
g = nx.read_graphml("ito.graphml")

# https://cir.nii.ac.jp/crid/1420845751153905536
h = nx.read_graphml("morishima.graphml")

# hの属性値はgの属性値よりも優先される
c : nx.Graph = nx.compose(g, h)
nx.write_graphml(c, "fusion_comp_lab.graphml")