# 社内決済システムで理解する Port / Adapter

このメモは、社内決済（申請 -> 承認 -> 決済）を例に  
`Port` と `Adapter` の役割を整理したものです。

---

## 1. まず結論（あなたの理解の確認）

あなたの理解はほぼ正しいです。  
補足すると次の通りです。

- `Port`:
  - 「外部アクセス時に何を受け取り、何を返すか」の**契約**を定義する
  - 実装（HTTP/JSON/SDK）は持たない
  - Domain型で入出力を揃えることが多い

- `Adapter`:
  - `Port` の実装
  - Domain型 <-> 外部API形式（JSON等）の変換
  - 実際の `Client` 呼び出しを行う

---

## 2. 社内決済に置き換える

### 2.1 登場人物

- `UseCase`: 申請処理の手順を進める
- `Domain(Entity/Value)`: 申請が正しいかを判定する
- `Port`: 決済ゲートウェイに「実行依頼する契約」
- `Adapter`: 実際に銀行API/決済APIへ接続する
- `Client`: HTTP/SDK通信を実行する

---

## 3. フロー図

```mermaid
flowchart LR
    UI[申請画面] --> P[Presentation]
    P --> U[SubmitPaymentUseCase]
    U --> D[PaymentRequest(Entity)]
    U --> Port[PaymentGatewayPort]
    Port --> A[BankPaymentAdapter]
    A --> C[BankApiClient]
    C --> API[銀行/決済API]
```

ポイント:
- UseCaseは `PaymentGatewayPort` しか知らない
- 銀行APIのURLやJSON項目名は Adapter/Client 側に閉じ込める

---

## 4. 役割の切り分け（何をどこに書くか）

### Domain に書く
- 申請可能か（必須入力が埋まっているか）
- 状態遷移が正しいか（`draft -> submitted` はOK、`approved -> submitted` はNG）

### UseCase に書く
- どの順番で処理するか
- いつ Port を呼ぶか

### Port に書く
- 例: `execute(request: PaymentRequest) -> PaymentResult`

### Adapter に書く
- `PaymentRequest` を API用JSONへ変換
- `Client` 呼び出し
- APIレスポンスを `PaymentResult` へ変換

---

## 5. 最小コードイメージ

```python
# Port（契約）
class PaymentGatewayPort(Protocol):
    def execute(self, req: PaymentRequest) -> PaymentResult:
        ...

# UseCase（手順）
class SubmitPaymentUseCase:
    def __init__(self, gateway: PaymentGatewayPort):
        self.gateway = gateway

    def execute(self, req: PaymentRequest) -> PaymentResult:
        req.assert_submittable()  # Domain判定
        return self.gateway.execute(req)

# Adapter（実装）
class BankPaymentAdapter(PaymentGatewayPort):
    def __init__(self, client: BankApiClient):
        self.client = client

    def execute(self, req: PaymentRequest) -> PaymentResult:
        payload = {
            "amount": req.amount.value,
            "currency": req.currency.value,
        }
        raw = self.client.post_payment(payload)
        return PaymentResult.from_api(raw)
```

---

## 6. よくある混同

- 「Port = 画面インターフェース」ではない  
  ここでの interface は**プログラム上の契約**です

- 「Port がAPIを直接叩く」ではない  
  APIを叩くのは Adapter/Client です

- 「Adapter が業務判断する」ではない  
  業務判断は Domain/UseCase です

---

## 7. 5秒で判定する質問

- この処理は「業務ルール」か？  
  -> Domain
- この処理は「手順の制御」か？  
  -> UseCase
- この処理は「外部サービス接続」か？  
  -> Adapter/Client
- これは「接続契約の定義」か？  
  -> Port
