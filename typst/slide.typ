#let author = "Shota Takahashi"
#let today = "2023/07/20"

#let p005 = json("data/test_data/chi2_test/chi2_test_p005.json")

#set page(
    header: today,
    numbering: "1 / 1",
)

#set par(
    leading: 1.5em,
)

#set text(
    font: "Noto Serif CJK JP",
    size: 10pt,
)

#set heading(numbering: "1.1.1." )
#show heading: it => block(
    fill: blue,
    inset: 1.5em,
    spacing: 1.5em,
    width: 100%,
    text(font: "Noto Sans CJK JP", fill: white)[#it.body]
    )

#set line(
    length: 100%,
    stroke: 1pt + olive,
    )

#set image( width: 90%)

#outline(
    indent: auto,
    depth: 2,
    fill: line(
        length: 90%,
        stroke: 1pt + luma(200),
    )
)

#pagebreak()

= 事前アンケート集計

- 集計期間：2023年7月06日 - 7月21日
- 対象：ICRC2023の参加者（1406人？）
- 回答：282件

== 事前アンケート回答者の内訳

回答数：282件（回答率：20.1%）

- Female : 84 (29.8%)
- Male : 185 (65.6%)
- Non-binary : 5 (1.8%)
- Prefer to self-identify : 3 (1.1%)
- Prefer not to answer : 2 (0.7%)

== ICRC2023の参加者の内訳

#columns(2)[
現地参加：1102人

- Female：241 (21.9%)
- Male：852 (77.3%)
- NA 9 : (0.8%)

#colbreak()

オンライン：304人

- Female：84 (27.6%)
- Male：220 (72.4%)
- NA：0 (0.0%)
]

Diversityセッション参加：約120名

#line()

- 参加者の性別比率と比べると、アンケート回答者は男↓女↑になっている
- ダイバーシティの取り組みの関心度は、やはり男性＜女性の傾向があるのかもしれない

#pagebreak()

= アンケートの項目と回答

== 基本属性（8項目）

+ 【Q1】What is your age ?
+ 【Q2】What gender do you identify as ?
+ 【Q3】Which geographical region are you currently working or attending school/university in ?
+ 【Q4】Which geographical region do you most strongly associate with ?
+ 【Q5】What is your job title ?
+ 【Q6】Which group do you belong to ?
+ 【Q7】What is your research type ?
+ 【Q11】Did you already sign up for the diversity session in ICRC2023 ?

== グループの実態調査（5項目）

+ 【Q12】What do you think about the initiatives on DE&I of your group ?
    - [Gender balance]
    - [Diversity]
    - [Equity]
    - [Inclusion]
+ 【Q13】What is the percentage of female researcher in your group ?
+ 【Q14】What do you think about the percentage above ?
+ 【Q15】Please let us know If your group has any good practice examples related to DE&I ?
+ 【Q16】Please let us know if there is anything your group needs to work on or if your group has any problems related to DE&I.

== 個人の意識調査（8項目）

+ 【Q8】How long have you been in this field ?
+ 【Q9】Are you satisfied with your career to date ?
+ 【Q10】How many hours, on average, do you spend on housework, childcare, and caregiving per day ?
+ 【Q17】What are your thoughts on diversity, equity & inclusion initiatives ?
    - [Gender balance]
    - [Diversity]
    - [Equity]
    - [Inclusion]
+ 【Q18】Could you tell us more about your thoughts (agree / disagree) ?
+ 【Q19】When did you first become interested in science ?
+ 【Q20】Do you have any concerns / problems related to DE&I initiatives in science ?
+ 【Q21】What reasons do you think are hindering DE&I initiatives in science ?
+ 【Q22】Comments

== 備考


アンケートのとき、Q8, Q9, Q10は「基本属性」のセクションで聞いてしまったが、
分析するときは「個人の意識（状況）」として、相関をとる変数としたほうがよさそう。

#pagebreak()

= 分析クラスター

- 最初は、基本属性の項目でクラスタリングして、回答の傾向を調べる
- 相関が強いもの、かつ、面白そうなものを探して、新しいクラスターを追加する
- 他にも、基本属性の回答を組み合わせて、新しいクラスターを定義できるかも？（ただし、そこまでやる時間はなさそう）。


/ 年代（`q01`）: 10代から90代の範囲で回答をお願いした。
/ 性別（`q02`): 性自認の回答をお願いした。
/ 地域（q03 / q04）: 勤務地と出身地の回答をお願いした。選択肢はWikipediaにあった #link("https://ja.wikipedia.org/wiki/%E5%9B%BD%E9%80%A3%E3%81%AB%E3%82%88%E3%82%8B%E4%B8%96%E7%95%8C%E5%9C%B0%E7%90%86%E5%8C%BA%E5%88%86")[国連による世界地理区分]を参考にした。
/ 職種（`q5`）: 身分の回答をお願いした。
/ 所属グループ（`q6`）: 選択肢はICRC2023のセッションと同じにした。
/ 実験屋と理論屋（`q7`）: 選択肢の用意を間違えたかも。「その他」に現象論や両方と書く人がちらほら。まとめて「Others」にした。
/ Diversityセッション参加／不参加（`q11`）: セッションに登録済かどうかの回答をお願いした。

== その他

#pagebreak()

= 分析データの準備手順

+ アンケートの回答（Googleスプレッドシート）をCSV形式でダウンロードする
    - 保存先 : `data/raw_data/YYYYMMDD_icrc2023_diversity_presurveys.csv`
+ データを前処理する（`pandas`パッケージを利用する）
    - データフレームに変換する
    - 表記揺れを置換する
    - 地域の回答を「五大州」と「地域」に分割する
    - 順序ありのカテゴリカルデータ（離散変数）に変換する
    - 自由記述の感情分析（極性と主観度）を追加する（`textblob`パッケージを利用する）
    - 自由記述の自動翻訳（英語→日本語）を追加する（`textblob`パッケージを利用する）
    - 保存先 : `data/test_data/prepared_data.csv`
+ 基本分布を確認する（`pandas`パッケージを利用する）
    - 保存先 : `data/test_data/hbar/*.csv`
    - 保存先 : `data/test_data/hbar/*.png`
+ クロス集計する（`pandas`パッケージを利用する）
    - クロス集計可能な回答（＝カテゴリカルデータ）を総当たりで集計する
    - 保存先 : `data/test_data/crosstab/*.csv`
    - 保存先 : `data/test_data/crosstab/*.png`
+ カイ二乗検定する（`scipy`パッケージを利用する）
    - 保存先 : `data/test_data/chi2_test/chi2_test.csv`
    - 保存先 : `data/test_data/chi2_test/chi2_test_p005.csv`
+ `p < 0.05`の項目を確認する
    - 保存先 : `data/test_data/p005/質問番号/chi2_test_p005_質問番号.csv`
+ 自由記述をJSON形式で保存する
    - 保存先 : `data/test_data/comments/質問番号.json`

#pagebreak()

= 確認したいこと

== Q12（グループの取り組み具合）の各項目との相関

=== `q12` and `q1`
    - `q12_genderbalance` and `q1`
    - `q12_diversity` and `q1`
    - `q12_equity` and `q1`
    - `q12_inclusion` and `q1`

    + q12 and q2
    + q12 and q3 / q3_regional / q3_subretional
    + q12 and q4 / q4_regional / q4_subretional
    + q12 and q5
    + q12 and q6
    + q12 and q7
    + q12 and q11
+ Q17（個人の取り組みに対する意識）の各項目との相関
    + q17 and q1
        - `q17_genderbalance` and `q1`
        - `q17_diversity` and `q1`
        - `q17_equity` and `q1`
        - `q17_inclusion` and `q1`
    + q17 and q2
    + q17 and q3 / q3_regional / q3_subretional
    + q17 and q4 / q4_regional / q4_subretional
    + q12 and q5
    + q12 and q6
    + q12 and q7
    + q12 and q11
+ Q13（女性研究者比率）とQ14（比率に対する考え）
    + q13 and q14 : 20% = Poor / 30% = Goodな分布ができそう
+ Q19（科学に興味をもった時期）と各項目の相関
    + q17 and q1
    + q17 and q2
    + q17 and q3 / q3_regional / q3_subretional ← 地域性が見られるとよい
    + q17 and q4 / q4_regional / q4_subretional
    + q12 and q5
    + q12 and q6
    + q12 and q7
    + q12 and q11


= 自由記述の分析

- 質問ごとに回答した人だけのデータを作成する
- 回答ごとに感情分析（極性と主観度）を評価する
- 極性と主観度の特徴量を計算する（平均値 or 中央値？）
- 質問ごとに、基本属性との相関を計算し、平均値との箱ひげ図を作成する

#pagebreak()



#pagebreak()

= 基本分布を作ってみた

== 性別と年代

#figure(
    image("data/quick_summary/tmp_q02.png"),
    caption: [性別]
)

#figure(
    image("data/quick_summary/tmp_q01.png"),
    caption: [年代]
)

- 20代〜40代に `non-binary`などの回答がある

#pagebreak()

== 地域

#figure(
    image("data/quick_summary/tmp_q03.png"),
    caption: [勤務地]
)

#figure(
    image("data/quick_summary/tmp_q04.png"),
    caption: [出身地]
)

#pagebreak()

== 地域（五大州）

#figure(
    image("data/quick_summary/tmp_q03_regional.png"),
    caption: [勤務地]
)

#figure(
    image("data/quick_summary/tmp_q04_regional.png"),
    caption: [出身地]
)

#pagebreak()

== 地域（詳細）

#figure(
    image("data/quick_summary/tmp_q03_subregional.png"),
    caption: [勤務地]
)

#figure(
    image("data/quick_summary/tmp_q04_subregional.png"),
    caption: [出身地]
)


- 中央アジアと西アジア（中東）は（回答者の）男女比が逆転している
- 日本の回答者の90%が男性

#pagebreak()

== 肩書き

#figure(
    image("data/quick_summary/tmp_q05.png"),
    caption: [肩書き]
)

#pagebreak()

== 所属グループ

#figure(
    image("data/quick_summary/tmp_q06.png"),
    caption: [所属グループ]
)

- O&E関係者は女性が多い
    - 僕の肌感覚も、広報担当者は女性が多いなぁという印象

#pagebreak()

== 理論 or 実験

#figure(
    image("data/quick_summary/tmp_q07.png"),
    caption: [理論 or 実験]
)

- これは回答の選択肢が不十分だったかも
- ``Prefer not to answer``の他に``Others``という回答もある
    - ``both``とかいたり、``phenomenologist``とかいたり

#pagebreak()

== Diversityセッション登録

#figure(
    image("data/quick_summary/tmp_q11.png"),
    caption: [Diversityセッション登録の有無]
)

#pagebreak()

== キャリア

#figure(
    image("data/quick_summary/tmp_q08.png"),
    caption: [キャリアの長さ]
)

#figure(
    image("data/quick_summary/tmp_q09.png"),
    caption: [キャリアに満足？]
)

- 3年から10年にかけて、男性比率がアップしている
- 3年未満でいちどリセットされる？

#pagebreak()

== 家事・育児・介護

#figure(
    image("data/quick_summary/tmp_q10_binned.png"),
    caption: [1日で家事・育児・介護にかかる平均時間数]
)

- 男性＝短時間、女性＝長時間という傾向がみられるかと思ったら、そうでもなかった

#pagebreak()

== 所属グループのDEI取り組み

#figure(
    image("data/quick_summary/tmp_q12_genderbalance.png"),
    caption: [Gender Balance]
)

#figure(
    image("data/quick_summary/tmp_q12_diversity.png"),
    caption: [Diversity]
)

#figure(
    image("data/quick_summary/tmp_q12_equity.png"),
    caption: [Equity]
)

#figure(
    image("data/quick_summary/tmp_q12_inclusion.png"),
    caption: [Inclusion]
)

- ただし、`Gender Balance`、`Diversity`、`Equity`、`Inclusion`のすべての項目に対して、男性は「`Very Good` or `Good`」、女性は「`Very Poor` or `Poor`」と感じている。


#pagebreak()

== 個人のDEI意識

#figure(
    image("data/quick_summary/tmp_q17_genderbalance.png"),
    caption: [Gender Balance]
)

#figure(
    image("data/quick_summary/tmp_q17_diversity.png"),
    caption: [Diversity]
)

#figure(
    image("data/quick_summary/tmp_q17_equity.png"),
    caption: [Equity]
)

#figure(
    image("data/quick_summary/tmp_q17_inclusion.png"),
    caption: [Inclusion]
)


- `Gender balance` と `Diversity` に関して「Disagree」の回答が少し目立つ気がした。
- `Gender balance`の取り組みに対して反対の割合は、女性も多い。

#pagebreak()

== グループ内の女性研究者の割合

#figure(
    image("data/quick_summary/tmp_q13_binned.png"),
    caption: [所属グループの女性研究者の割合]
)

#figure(
    image("data/quick_summary/tmp_q14.png"),
    caption: [上記の割合についてどう思うか]
)


#pagebreak()

== 科学にはじめて興味を持った時期

#figure(
    image("data/quick_summary/tmp_q19.png"),
    caption: [科学への興味]
)


小学校で興味を持った研究者が多い。
中学校より、高校で興味を持った研究者の方が多い。
男性の方が早い段階（＝小学校）で興味を持つ。
ただし、それほど男女差はないのかも？
地域で見た方がいいのかもしれない？

#pagebreak()

= クロス集計してみた

- カテゴリカルデータ（離散変数）を2つ選び、そのクロス集計表（frequensy table）を作成する
- 作成した集計表に対し、相関がないという帰無仮説を仮定し、$chi^(2)$検定をかけて、有意差（p値）を評価する
- $chi^(2)$検定にはPythonの`scipy`パッケージを使う
    - デフォルトで`correction=True`。自由度が1のとき、イェーツの連続補正が適用される

```python
from scipy.stats import chi2_contingency
cross_tab = pd.crosstab(data[x], data[y])
chi2, p, dof, expected = chi2_contingency(cross_tab)
```

== $chi^2$検定

$
chi^2 = sum ("observed" - "expected")^(2) / "expected"
$

- カテゴリカルデータ（離散変数）を対象とした検定手法
- 対象とする離散変数の独立性を評価する
    - 離散変数に"相関がない"帰無仮説を仮定して、期待度数を計算する
    - 測定量と期待度数の差を計算する
- p値が0.05以下だと「独立ではない」（＝相関がある）

== $chi^(2)$検定の結果

- p値 < 0.05以下の項目を抽出し、次ページ以降に相関図を載せた
- 該当数 ＝ #p005.len()

#pagebreak()

#for row in p005 [
    == #row.questions

    #let png = "data/test_data/crosstab/" + row.questions + ".png"

    - ファイル名: #png

    #figure(
        image(png),
        caption: [#row.questions]
    )

    === 検定の結果

    #align(center)[
        #table(
            columns: 3,
            inset: 1em,
            align: start,
            /* --- header --- */
            [**p-value**],
            [**DoF**],
            [**Statistic**],
            /*--- body --- */
            [#row.p_value],
            [#row.dof],
            [#row.statistic],
        )
    ]

    #pagebreak()
]


#pagebreak()

= 感情分析

== Q15

#figure(
    image("../data/quick_summary/tmp_q15_polarity.png"),
    caption: [Q15 : 極性（polarity）]
)

#figure(
    image("../data/quick_summary/tmp_q15_subjectivity.png"),
    caption: [Q15 : 主観度（subjectivity）]
)

#pagebreak()

== Q16

#figure(
    image("../data/quick_summary/tmp_q16_polarity.png"),
    caption: [Q16 : 極性（polarity）]
)

#figure(
    image("../data/quick_summary/tmp_q16_subjectivity.png"),
    caption: [Q16 : 主観度（subjectivity）]
)

#pagebreak()

== Q18

#figure(
    image("../data/quick_summary/tmp_q18_polarity.png"),
    caption: [Q18 : 極性（polarity）]
)

#figure(
    image("../data/quick_summary/tmp_q18_subjectivity.png"),
    caption: [Q18 : 主観度（subjectivity）]
)

#pagebreak()

== Q20

#figure(
    image("../data/quick_summary/tmp_q20_polarity.png"),
    caption: [Q20 : 極性（polarity）]
)

#figure(
    image("../data/quick_summary/tmp_q20_subjectivity.png"),
    caption: [Q20 : 主観度（subjectivity）]
)

#pagebreak()

== Q21

#figure(
    image("../data/quick_summary/tmp_q21_polarity.png"),
    caption: [Q21 : 極性（polarity）]
)

#figure(
    image("../data/quick_summary/tmp_q21_subjectivity.png"),
    caption: [Q21 : 主観度（subjectivity）]
)

#pagebreak()

== Q22

#figure(
    image("../data/quick_summary/tmp_q22_polarity.png"),
    caption: [Q22 : 極性（polarity）]
)

#figure(
    image("../data/quick_summary/tmp_q22_subjectivity.png"),
    caption: [Q22 : 主観度（subjectivity）]
)

#pagebreak()
