## ✔ Clean Architecture的にClient 定義してはいけないもの
- ✔ **Client に抽象化は不要**
- ✔ Client は API ドキュメントの写経
- ✔ model を Infra に置くのは正しい
- ✔ Domain / UseCase が model を知らない構成は理想形
- ✔ 今のディレクトリ構成は Clean Architecture 的に問題なし

<br>

### Client の正体（ここが一番大事）
つまり Client は **「使われることを前提にした、無感情な道具」 です。**
- Domain の型は一切出てこない
- OpenAI / ChatGPT の 公式ドキュメントどおりの実装
- 引数も戻り値も 外部API都合
- 「このAPIはどう呼ぶか」しか知らない
- ビジネスルール・条件分岐は一切持たない


<br>

## Flow
```
UseCase
  ↓（抽象）
Port（TextGeneratorPort）
  ↓（翻訳）
Adapter  ここで値と結びつけする
  ↓（生データ）
Client
  ↓
外部API
```

- Client は UseCase から直接呼ばれない
- 必ず Adapter 経由で呼ばれる
- Client 自身は「なぜ呼ばれたか」を知らない

<br>

## ❌ Client が知ってはいけないもの
- MsgContent（Domain）
- Port
- UseCase
- Entity
- ValueObject

## ❓ なぜ？
- Clientは外部サービスとのやり取りを担当する層であり、内部のビジネスロジックやデータ構造に依存しないようにするため
- これにより、Clientの実装を変更しても、他の層に影響を与えず、システムの柔軟性と保守性を向上させることができるため



## Entity と ValueObject の役割まとめ（やさしく版）

---

### ValueObject は「値そのもの」


### Entity は「値をまとめて、意味と状態を持たせる箱」

---

## 慣例的な正解構成（王道）
```
domain/
├─ entities/
│  └─ user.py
│
├─ values/
│  ├─ user_id.py
│  ├─ email_address.py
│  └─ password.py
```

### 実際のCode
```python
class User:
    def __init__(
        self,
        user_id: UserId,
        email: EmailAddress,
        password: Password,
    ):
        self.user_id = user_id
        self.email = email
        self.password = password

    def change_email(self, new_email: EmailAddress):
        self.email = new_email
```
---
### 🧱 ValueObject（値の正しさ）

EmailAddress
- フォーマット検証
- 空チェック
- 等価性

Password
- 長さ
- ハッシュ化ルール
- 生パスワード禁止

👉 **「値として成立するか」を保証**

```python
@dataclass(frozen=True)
class UserId:
    value: str

    def __post_init__(self):
        if not self.is_not_empty():
            raise ValueError("UserId is empty")

        if not self.is_short_enough():
            raise ValueError("UserId is too long")

        if not self.has_only_letters_and_numbers():
            raise ValueError("UserId has invalid characters")

    def is_not_empty(self) -> bool:
        return bool(self.value)

    def is_short_enough(self) -> bool:
        return len(self.value) <= 20

    def has_only_letters_and_numbers(self) -> bool:
        return self.value.isalnum()


# 別ファイル掲載
@dataclass(frozen=True)
class EmailAddress:
    value: str

    def __post_init__(self):
        if not self.is_not_empty():
            raise ValueError("Email is empty")

        if not self.has_at_mark():
            raise ValueError("Email must have @")

        if not self.looks_like_email():
            raise ValueError("Email format is wrong")

    def is_not_empty(self) -> bool:
        return bool(self.value)

    def has_at_mark(self) -> bool:
        return "@" in self.value

    def looks_like_email(self) -> bool:
        return self.value.count("@") == 1


# 別ファイル掲載
@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        if not self.is_not_empty():
            raise ValueError("Password is empty")

        if not self.is_long_enough():
            raise ValueError("Password is too short")

        if not self.has_letters():
            raise ValueError("Password needs letters")

        if not self.has_numbers():
            raise ValueError("Password needs numbers")

    def is_not_empty(self) -> bool:
        return bool(self.value)

    def is_long_enough(self) -> bool:
        return len(self.value) >= 8

    def has_letters(self) -> bool:
        return any(c.isalpha() for c in self.value)

    def has_numbers(self) -> bool:
        return any(c.isdigit() for c in self.value)
```


---

### 🧍 Entity（存在と状態）

User
- UserId を持つ
- EmailAddress を持つ
- Password を持つ
- 状態遷移（有効 / 無効 / 仮登録など）

👉 **「誰か」「いつ」「どんな状態か」を管理**

```python
# src/domain/entities/user.py
from src.domain.values.user_id import UserId
from src.domain.values.email_address import EmailAddress
from src.domain.values.password import Password

class User:
    def __init__(
        self,
        user_id: UserId,
        email: EmailAddress,
        password: Password,
    ):
        self.user_id = user_id
        self.email = email
        self.password = password

    def change_email(self, new_email: EmailAddress):
        # EmailAddress 側でチェック済みなので、そのまま入れ替えるだけ
        self.email = new_email

    def change_password(self, new_password: Password):
        # Password 側でチェック済み
        self.password = new_password
```