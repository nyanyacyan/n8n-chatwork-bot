# pytest 基本ルール（下書き）

このドキュメントは「pytest の型」を整理するためのメモです。
自分の言葉で追記して完成させることが目的です。

---

## 0. 基本方針
- 何を守るテストか（仕様）を最初に書く
- 何を確認するか（確認方法）を具体的に書く
- 1つのテストは1つの意図に絞る

### 記入例
例：ChatMsgContent
```
仕様：「空はNG」「文字数は1000文字以内」「2文字以内はNG」
確認方法：
・値に'hello'を入れて最終の渡される値が'hello'であることを確認 ▶ assert
・値の長さが'hello'のlengthが5であることを確認 ▶ assert
・空文字を入れてValueErrorになることを確認 ▶ pytest.raises
・Noneを入れてValueErrorになることを確認 ▶ pytest.raises
・1001文字の文字列を入れてValueErrorになることを確認 ▶ pytest.raises
```

### ユニットテストの基本Code
```python
import pytest

def test_chat_msg_content_valid():
    # Arrange
    content = "hello"
    
    # Act
    chat_msg_content = ChatMsgContent(content)
    
    # Assert
    assert chat_msg_content.value == content
    assert chat_msg_content.length() == len(content)


def test_chat_msg_content_invalid():
    # Arrange / Act / Assert
    with pytest.raises(ValueError):
        ChatMsgContent("")  # 空文字

    with pytest.raises(ValueError):
        ChatMsgContent(None)  # None

    with pytest.raises(ValueError):
        ChatMsgContent("a" * 1001)  # 1001文字
```

### テストの実行の仕方

#### 全テスト実行
```bash
pytest
```

#### 特定ファイルのテスト実行
```bash
pytest tests/application/domain/entities/test_chat_msg_content.py
```
#### 特定関数のテスト実行
```bash
pytest tests/application/domain/entities/test_chat_msg_content.py::test_chat_msg_content_valid
```

#### キーワードで絞る
```bash
pytest -k "valid"
```


### テスト結果
#### 正常系
- 緑色で passed と出る
![◯ passedと出力される](./assets/pytest_正常系テスト結果画像.png)

- 例外処理の場合でも緑色で passed と出る▶定義している例外が正しく発生しているか確認
![](./assets/pytest_正常系_例外テスト結果画像.png)

#### 異常系
- 赤色で failed と出る
![✕ failedと出力される](./assets/pytest_異常系テスト結果画像.png)


---

## 1. テストの基本形（AAA）
- Arrange（準備）
- Act（実行）
- Assert（検証）

```
# Arrange
# Act
# Assert
```

（ここに自分の言葉で補足）

---

## 2. 正常系 / 異常系の分け方
- 正常系: 期待通りに生成/返却されること
- 異常系: 不正な値で例外が出ること

### 2-1. 例外チェックの型
```python
with pytest.raises(ValueError):
    ...
```

（ここに自分の言葉で補足）

---

## 3. parametrize の型
- 同じ仕様を複数パターンで確認する

```python
@pytest.mark.parametrize(
    "invalid",
    ["", "   ", None, 123],
)
def test_xxx_invalid(invalid):
    with pytest.raises(ValueError):
        XXX(invalid)
```

（ここに自分の言葉で補足）

---

## 4. レイヤー別のテスト型

### 4-1. Value Object
- 目的: 値に対して制約を設け、守れているかを確認すること
- 正常系: valueとlengthにて値を確認▶実際の値を入れ込む
（value==‘hello’  value.length == 5）
- 異常系: 型/None/空/長さ超過 ▶5つがvalueerrorになることを確認 pytest.raises

（ここに自分の言葉で補足）

### 4-2. Entity
- 目的: 値の保持と振る舞い
- 正常系: フィールド保持と length 等
- 異常系: 基本は ValueObject に寄せる

（ここに自分の言葉で補足）

### 4-3. UseCase
- 目的: 流れが崩れていないか
- Fake を使って依存を切る
- 受け渡し値と呼び出し回数を確認

（ここに自分の言葉で補足）

### 4-4. Adapter / Client（Infra）
- 目的: 変換や呼び出しの形が崩れないか
- できれば外部通信はモック化

（ここに自分の言葉で補足）

---

## 5. テスト命名ルール
- test_対象_状況_期待結果 の順で読む
- 例: test_chat_msg_content_invalid

（ここに自分の言葉で補足）

---

## 6. コメントの書き方
- 先頭に「仕様：」を置く
- 何のテストか + 確認方法を書く

例:
```
# 仕様：
# ChatMsgContent の値オブジェクトが有効な文字列を保持できることと、
# 空文字・空白・None・長すぎる文字列・非文字列で ValueError になることを確認する。
# 確認方法: 正常系は value と length を assert、異常系は pytest.raises を使用。
```

（ここに自分の言葉で補足）

---

## 7. 追加で決めたいこと
- fixture の使いどころ
- Fake / Stub / Mock の使い分け
- どこまでユニット、どこから結合

（ここに自分の言葉で追記）
