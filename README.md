# co-CiNii-net
Generate co-author networks from CiNii metadata based on RDF.

 - 情報メディア実験Bの担当教員である津川先生の共著 Ego Network（一部・加工後）
![image](https://user-images.githubusercontent.com/40143183/208823654-9a6357a9-5468-4911-80cb-d948adf2e048.png)

# About
CiNiiのRDFデータを利用し、任意の研究者を始点とする（Ego Networkである）共著ネットワークを生成します。

 - https://cir.nii.ac.jp/crid/1070012545625749888       (Webページ)
 - https://cir.nii.ac.jp/crid/1070012545625749888.rdf   (RDF)

このようなメタデータを利用します。

このプログラムは、筑波大学情報学群情報メディア創成学類が開講している「情報メディア実験B」の
テーマ「M28: ソーシャルネットワーク分析（担当教員：津川翔先生）」において田村が開発したものです。

# Usage
## 環境構築
```
poetry install      # install dependencies
poetry shell        # activate virtual env
```
(動作させるだけなら`--no-dev`をつけることもできます。)

## グラフの生成
2-hop、つまり「知り合いの知り合い」までのノードを含むグラフを生成します。
```python
from core.cociniinet import CoCiNiiNet

net = CoCiNiiNet(
        "https://cir.nii.ac.jp/crid/1420001326209796096",
        "Tsugawa Sho", 
        wait_seconds=0.5,
        is_nayose=True,
     )
net.generate()
net.write_graphml("result.graphml")
```

 - `wait_seconds`でCiNiiに対してGETリクエストを送る間隔を指定します。
 - `is_nayose`で名寄せ（表記ゆれの吸収）を有効にします。
   - 形態素解析でヘボン式ローマ字に変換し、小文字化、記号除去を行った後ソートした文字列を、研究者の識別情報にします。
   - `False`の場合はRDFの思想に則りURIを識別情報にします。

`wait_seconds`にもよりますが、生成にかなり時間がかかります。

## グラフの合成
異なる研究者の共著Ego Networkを合成できます。
（`is_nayose`の値が一致している必要がある。）

```python
import networkx as nx
g = nx.read_graphml("ito.graphml")        # https://cir.nii.ac.jp/crid/1420003854341602816
h = nx.read_graphml("morishima.graphml")  # https://cir.nii.ac.jp/crid/1420845751153905536
c : nx.Graph = nx.compose(g, h)           # hの属性値はgの属性値よりも優先される
nx.write_graphml(c, "fusion_comp_lab.graphml")
```

## クラスタリング
Louvainアルゴリズムでクラスタリングを行い、ノードの属性`cluster`にクラスタ番号をセットします。
この属性を用いて、Gephiなどでノードの色分けができます。
```python
import networkx as nx
from utils.graph import louvain_clustering
g = nx.read_graphml("tsugawa.graphml")       # https://cir.nii.ac.jp/crid/1420001326209796096
louvain_clustering(g)                        # クラスタリング（gのノード属性値が変更される）
nx.write_graphml(g, "tsugawa_clustered.graphml")
```

## 可視化
`visualizer.jar`を用いて可視化ができます。

詳しくは、[こちら](https://github.com/takumi1001/co-CiNii-net/tree/main/visualizer)。
