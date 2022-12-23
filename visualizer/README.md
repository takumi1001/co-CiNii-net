# visualizer
co-CiNii-netで生成したGraphMLファイルを[Gephi ToolKit](https://gephi.org/toolkit/)で可視化します。
SVGやPNGで出力できます。

## 可視化方法
 1. OpenOrdアルゴリズムでレイアウトします。
 2. 次数が1のノードを隠します。
 3. ノードサイズを次数によって変化させます。
 4. Noverlapアルゴリズムでレイアウトします。
 5. クラスタによって色を変えます（`cluster`属性がある場合）。

## Usage
### 環境構築
#### バイナリのダウンロード
1. Releaseより`visualizer.jar`をダウンロードし、適当なフォルダに配置します（準備中）。
2. `visualizer.jar`の位置するフォルダ下に`libs`フォルダを作成します。
3. [Gephi ToolKit](https://gephi.org/toolkit/)をダウンロードします。
4. Gephi Toolkitのjarファイルを`gephi-toolkit.jar`としてリネームし、`libs`下に保存してください。
```
./
┃ libs/
┃ ┗ gephi-toolkit.jar
┗ visualizer.jar
```
こうなっていれば大丈夫です。
#### Javaのインストール
Java実行環境を整えてください。作者の環境は以下の通りです。
```
> java -version
openjdk version "19.0.1" 2022-10-18
OpenJDK Runtime Environment (build 19.0.1+10-21)
OpenJDK 64-Bit Server VM (build 19.0.1+10-21, mixed mode, sharing)
```
### 実行
```
> java -jar ./visualizer.jar <command-line-options>

Usage:
        java -jar ./visualizer.jar input.graphml output.svg [font name]
Args:
        input.graphml   ... co-CiNii-net's GraphML file.
         output.svg     ... Output file name and ext. (.svg, .png, .pdf and more allowed.)
         [font name]    ... [Optional] Specify label font. Default is `IPA Gothic`.

　* Exporting PDF function has problems in printing multi-byte characters.
　* Specified font is ignored when it not found.
```
デフォルトのフォントが[IPA Gothic](https://moji.or.jp/ipafont/)となっていますので注意してください。
また、Gephi Toolkitのバグなのか、日本語のPDF出力がうまくいきません。SVGかPNGを利用してください。
#### 例
```
> java -jar visualizer.jar hoge.graphml out.png
---> "hoge.graphml"を"out.png"に可視化して出力します。

> java -jar visualizer.jar hoge.graphml out.svg 游明朝
---> "hoge.graphml"を"out.svg"に可視化して出力します。フォントは游明朝を指定します。
```

## Build
[IntelliJ IDEA](https://www.jetbrains.com/ja-jp/idea/)でいい感じにビルドできると思います。
