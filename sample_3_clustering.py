# グラフのクラスタリング
import networkx as nx
from utils.graph import louvain_clustering

# グラフの読み込み
g = nx.read_graphml("tsugawa.graphml") # https://cir.nii.ac.jp/crid/1420001326209796096

# クラスタリング（gのノード属性値が変更される）
# cluster属性にクラスタ番号がセットされる
louvain_clustering(g)

# グラフの保存
nx.write_graphml(g, "tsugawa_clustered.graphml")