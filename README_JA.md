# delta-trace-db

日本語版の解説です。

## 概要

**DeltaTraceDB は、クラス構造をそのまま保存・検索できる軽量・高速のインメモリ NoSQL データベースです。**  
NoSQLですが、ネストされた子クラスの値についても全文検索が行えます。

さらに、DeltaTraceDB のクエリはクラスであり、  
クエリ自体をシリアライズして保存することで任意の時点のDBを復元できる他、  
**who / when / what / why / from** 等の操作情報を保持可能です。  
これにより、セキュリティ監査や利用状況分析に利用できる「リッチな操作ログ」を作ることができます。

## 特徴
- **クラスをそのまま保存・検索**（モデルクラス＝DB構造）
- 約 10 万件レベルでも高速な検索性能
- クエリ自体がクラスなので操作ログとして保存可能
- フロントエンド用にはDart 版があります。  
  → https://pub.dev/packages/delta_trace_db
- DB の内容を編集できる GUI ツールもあります。  
  → https://github.com/MasahideMori-SimpleAppli/delta_trace_studio

## 基本操作

詳細な使用方法やクエリの記述などは、オンラインドキュメントをご覧ください。

📘 [オンラインドキュメント](https://masahidemori-simpleappli.github.io/delta_trace_db_docs/)

## クイックスタート

サーバーサイドコードの簡単な例を以下に示します。  
[サーバーサイドの例](https://github.com/MasahideMori-SimpleAppli/delta_trace_db_py_server_example)

また、簡単なサンプルは次の通りです。

```python
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Any
from file_state_manager import CloneableFile
from delta_trace_db import DeltaTraceDatabase, QueryBuilder


@dataclass
class User(CloneableFile):
    id: int
    name: str
    age: int
    created_at: datetime
    updated_at: datetime
    nested_obj: dict

    @classmethod
    def from_dict(cls, src: Dict[str, Any]) -> "User":
        return User(
            id=src["id"],
            name=src["name"],
            age=src["age"],
            created_at=datetime.fromisoformat(src["createdAt"]).astimezone(timezone.utc),
            updated_at=datetime.fromisoformat(src["updatedAt"]).astimezone(timezone.utc),
            nested_obj=dict(src["nestedObj"]),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "createdAt": self.created_at.astimezone(timezone.utc).isoformat(),
            "updatedAt": self.updated_at.astimezone(timezone.utc).isoformat(),
            "nestedObj": dict(self.nested_obj),
        }

    def clone(self) -> "User":
        return User.from_dict(self.to_dict())


def main():
    db = DeltaTraceDatabase()
    now = datetime.now(timezone.utc)

    users = [
        User(
            id=-1,
            name="Taro",
            age=30,
            created_at=now,
            updated_at=now,
            nested_obj={"a": "a"},
        ),
        User(
            id=-1,
            name="Jiro",
            age=25,
            created_at=now,
            updated_at=now,
            nested_obj={"a": "b"},
        ),
    ]

    # If you want the return value to be reflected immediately on the front end,
    # set return_data = True to get data that properly reflects the serial key.
    query = (
        QueryBuilder.add(
            target="users",
            add_data=users,
            serial_key="id",
            return_data=True,
        )
        .build()
    )

    # In the Python version, no type specification is required (duck typing)
    r = db.execute_query(query)

    # If you want to check the return value, you can easily do so by using toDict, which serializes it.
    print(r.to_dict())

    # You can easily convert from the Result object back to the original class.
    # The value of r.result is deserialized using the function specified by convert.
    results = r.convert(User.from_dict)


if __name__ == "__main__":
    main()
```

## DB の構造

DeltaTraceDB では、各コレクションが「クラスのリスト」に相当します。  
クラス設計そのままでデータが扱えるため、フロントエンド・バックエンド間の整合性がとりやすく、  
「必要なクラスオブジェクトを取得する」という自然な操作に集中できます。

```
📦 Database (DeltaTraceDB)
├── 🗂️ CollectionA (key: "collection_a")
│   ├── 📄 Item (ClassA)
│   │   ├── id: int
│   │   ├── name: String
│   │   └── timestamp: String
│   └── ...
├── 🗂️ CollectionB (key: "collection_b")
│   ├── 📄 Item (ClassB)
│   │   ├── uid: String
│   │   └── data: Map<String, dynamic>
└── ...
```

## パフォーマンス

本パッケージはインメモリ DB のため基本的に高速です。  
プログラムの for ループに近い性能で動作するため、10 万件規模では実用上ほぼ問題ありません。  

テストコードは以下にあります。
```
tests/test_speed.py
```

また、以下は Ryzen 3600 の PC で実施した実際の結果です。
```text
tests/test_speed.py speed test for 100000 records
start add
end add: 339 ms
start getAll (with object convert)
end getAll: 659 ms
returnsLength: 100000
start save (with json string convert)
end save: 467 ms
start load (with json string convert)
end load: 558 ms
start search (with object convert)
end search: 866 ms
returnsLength: 100000
start search paging, half limit pre search (with object convert)
end search paging: 425 ms
returnsLength: 50000
start searchOne, the last index object search (with object convert)
end searchOne: 38 ms
returnsLength: 1
start update at half index and last index object
end update: 90 ms
start updateOne of half index object
end updateOne: 16 ms
start conformToTemplate
end conformToTemplate: 82 ms
start delete half object (with object convert)
end delete: 621 ms
returnsLength: 50000
start deleteOne for last object (with object convert)
end deleteOne: 22 ms
returnsLength: 1
start add with serialKey
end add with serialKey: 98 ms
addedCount:100000
```

## 今後の予定について

高速化は可能なものの優先度は低めで、  
使い勝手の向上や周辺ツールの開発 が主な改良対象になる予定です。

## 注意事項

本パッケージは **シングルスレッド前提** で設計されています。  
メモリを共有しない並列処理では、メッセージパッシングなどの追加処理が必要なことに注意してください。

## サポート

このパッケージは、オープンソースプロジェクトとして私が個人的に開発・保守しています。
バグ報告や機能リクエストについては、GitHub Issues をご利用ください。

**有料サポート、コンサルティング、カスタム開発**
（例：優先サポート、設計アドバイス、実装支援）が必要な場合は、
下記までご連絡ください。

**合同会社シンプルアプリ**  
https://simpleappli.com/index.html

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
