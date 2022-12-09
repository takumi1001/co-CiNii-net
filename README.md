# co-CiNii-net
Generate co-author networks from CiNii metadata based on RDF.

# About
CiNiiのRDFデータを利用し、任意の研究者を始点とする共著ネットワークを生成します。

 - https://cir.nii.ac.jp/crid/1070012545625749888       (Webページ)
 - https://cir.nii.ac.jp/crid/1070012545625749888.rdf   (RDF)

このようなメタデータを利用します。

誠意開発中です。

# Usage
## 環境構築
```
poetry install      # install dependencies
poetry shell        # activate virtual env
```
(動作させるだけなら`--no-dev`をつけることもできます。)

## グラフの生成
```python
from core.cociniinet import CoCiNiiNet

net = CoCiNiiNet("https://cir.nii.ac.jp/crid/1070012545625749888", "田村匠", wait_seconds=1, is_nayose=True)
net.generate(max_reqests=500)
net.write_graphml("result.graphml")
```

 - `wait_seconds`でCiNiiに対してGETリクエストを送る間隔を指定します。
 - `is_nayose`で名寄せ（表記ゆれの吸収）を有効にします。
   - 形態素解析でヘボン式ローマ字に変換し、小文字化、記号除去を行った後ソートした文字列を、研究者の識別情報にします。
   - `False`の場合はRDFに規則に則りURIを識別情報にします。
 - `max_requests`でGETリクエストを送信する総数を指定します。 