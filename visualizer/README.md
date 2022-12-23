# visualizer
co-CiNii-netで生成したグラフを[Gephi ToolKit](https://gephi.org/toolkit/)で可視化します。

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
```

## Build
[IntelliJ IDEA](https://www.jetbrains.com/ja-jp/idea/)でいい感じにビルドできると思います。
