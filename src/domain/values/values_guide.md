## ValueObject が持つルール（＝値の成立条件）

### ValueObject は「値そのものの正しさ」を保証する
- 空でいいか？
- 長さは？
- フォーマットは？
- 同値性（==）は？

👉 これが ValueObject の責務


## Entity が持つルール（＝状態と振る舞い）
- ID を持つ
- 状態遷移がある
- 複数の ValueObject を束ねる
- 自己完結した振る舞いを持つ

👉 ここが Entity の肉付け


## Entities と ValueObjects の違い
- Entity: ステータスやIDなどの「識別可能な属性」を持つオブジェクト
- ValueObject: 値そのものの正しさを保証するオブジェクト


## DomainService が持つルール（＝判断）
- 複数 Entity をまたぐ
- 文脈依存
- 状況により変わる