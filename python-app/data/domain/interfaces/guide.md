## interfaceでは基本抽象化契約だけを置く場所

## interfaceとは
```
Cleanアーキテクチャでの
interfaceの意味は制限付きを設けたうえでApplicationとInfrastructureの間でやり取りするための契約を指す

Application → (契約) → Infrastructure

この流れを元に、Infraに渡せるようにするための制限付きの型をinterfaceとして定義
```

### 他のinterfaceの意味(３つの種類がある)


#### ①ユーザー → UI (Interface)
ユーザーが触る操作画面  
例：GUI、画面、UX、ダッシュボード


#### ② APIとしての interface（外部通信）
→ 他のサービスから呼ばれる部分が「インターフェース」。


## ファイルは基本、その抽象化別にファイル生成する認識