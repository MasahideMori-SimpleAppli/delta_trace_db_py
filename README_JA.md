# delta-trace-db

日本語版の解説です。
このパッケージは、DeltaTraceDBのPython版です。 

## 使い方

[Dart版](https://github.com/MasahideMori-SimpleAppli/delta_trace_db)を参照してください。  
引数がデフォルトでスネークケースになることや、標準関数と名前空間が競合する場合は変数名の後にアンダースコアが付加されるなど、いくつか違いはありますが、使い方は同じです。  

サーバーサイドコードの簡単な例を以下に示します。  
[サーバーサイドの例](https://github.com/MasahideMori-SimpleAppli/delta_trace_db_py_server_example)  

## 速度

このパッケージはインメモリデータベースなので、基本的に高速です。  
現在、高速化する仕組みはありませんが、プログラム内のforループとほぼ同じ動作をするため、10万件程度であれば通常は問題ありません。  
testフォルダ内のtest_speed.pyを使用して、実際の環境でテストすることをお勧めします。  
ただし、データ量に応じてRAM容量を消費するため、非常に大規模なデータベースが必要な場合は、一般的なデータベースの使用を検討してください。  
参考までに、Ryzen 3600 CPUを搭載した少し古いPCで実行した速度テストの結果（tests/test_speed.py）を以下に示します。  
テスト条件は十分に時間がかかるように選択していますが、実用上問題になることは少ないと思います。  
なお、速度はデータ量にも依存するため、大きなデータが多い場合は遅くなります。  

```text
tests/test_speed.py speed test for 100000 records
start add
end add: 340 ms
start getAll (with object convert)
end getAll: 655 ms
returnsLength: 100000
start save (with json string convert)
end save: 467 ms
start load (with json string convert)
end load: 555 ms
start search (with object convert)
end search: 865 ms
returnsLength: 100000
start search paging, half limit pre search (with object convert)
end search paging: 425 ms
returnsLength: 50000
start update at half index and last index object
end update: 97 ms
start updateOne of half index object
end updateOne: 31 ms
start conformToTemplate
end conformToTemplate: 81 ms
start delete half object (with object convert)
end delete: 550 ms
returnsLength: 50000
start deleteOne for last object (with object convert)
end deleteOne: 22 ms
returnsLength: 1
start add with serialKey
end add with serialKey: 100 ms
addedCount:100000
```

## 今後の予定

データベースの高速化は可能ですが、優先度は低いので、使い勝手の向上や周辺ツールの作成を優先することになると思います。  

## 注意

このパッケージは基本的にシングルスレッド操作を前提としています。  
Dart版とは異なり、DeltaTraceDatabase クラス内部の大半のメソッドは RLock を取得するためマルチスレッドでの呼び出しが可能ですが、
その他のクラスやユーティリティ関数はスレッドセーフではないため、並行して使用する場合は注意が必要です。  
また、メモリを共有しない並列処理（プロセス間など）を行う場合は、Dart版同様にメッセージパッシング等の追加処理が必要となります。  

## サポート

There is essentially no support at this time, but bugs will likely be fixed.  
If you find any issues, please open an issue on GitHub.

## バージョン管理について

The C part will be changed at the time of version upgrade.  
However, versions less than 1.0.0 may change the file structure regardless of the following rules.

- Changes such as adding variables, structure change that cause problems when reading previous
  files.
    - C.X.X
- Adding methods, etc.
    - X.C.X
- Minor changes and bug fixes.
    - X.X.C

## ライセンス

This software is released under the Apache-2.0 License, see LICENSE file.

Copyright 2025 Masahide Mori

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## 商標など

- “Dart” and “Flutter” are trademarks of Google LLC.  
  *This package is not developed or endorsed by Google LLC.*

- “Python” is a trademark of the Python Software Foundation.  
  *This package is not affiliated with the Python Software Foundation.*

- GitHub and the GitHub logo are trademarks of GitHub, Inc.  
  *This package is not affiliated with GitHub, Inc.*
