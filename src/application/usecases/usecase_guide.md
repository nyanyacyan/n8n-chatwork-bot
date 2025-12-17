## UseCase の正体
```
UseCase とは
利用者がやりたいこと（ユースケース）のFlowを
コードでそのまま書いたもの
```

### 👉 1つの UseCase = 1つの execute() まとめる
・「チャットに来たメッセージに返信を生成する」
・「最新メッセージを取得する」
・「メッセージを送信する」



AdapterでセットされているものをUseCaseで呼び出すイメージ
→実際に実体化させて動かすのはUseCaseのexecute()メソッド

```python

```


Prompt生成に関しては、UseCaseではなく「Domain」に置くのが正

👉 LLMが変わっても Prompt の思想は変わらない

infrastructureに置くものはあくまでも、動きがあるもの、外部へのアクセスが有るものをまとめるところ


ビジネスルールとは値自体に制約をもたせることのことを指す
- この room_id は空じゃダメ
- この形式じゃないとダメ
- この長さじゃないとダメ

## DTOでやっていること

生のデータを受け取ってそれを明示するもの
#### 基本は引数に入れて使う

- 型を揃える（str / int / list など）
- フィールドを明示する
- 「この UseCase は何を受け取るか」を表す

```
@dataclass
class GetNewMsgRequest:
    room_id: str
    msg: str



from src.application.dtos.get_new_msg import GetNewMsgRequest

def execute(self, req: GetNewMsgRequest):
    ...
```


## DTOでやってはいけないこと
- ビジネスルールの実装
- 値の意味のチェック
- 制約の実装（長さ、形式、状態）


## DTOを使うのは **この条件のときだけ**
```
「この UseCase は外部（UI / API / Webhook）から直接呼ばれるか？」
つまり入口のみDTOを使う
```

