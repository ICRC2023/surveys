#let Q = "【Q15】Please let us know If your group has any good practice examples related to DE&I ?"
#let answers = json("../data/test_data/comment/q15.json")

#set document(
    title: Q
)

#set page(
    header: [
        #set text(8pt)
        #h(1fr) updated: 2023/07/23
        ],
    numbering: "1 / 1",
)

#set par(
    leading: 1em,
)

#set text(
    font: "Noto Serif CJK JP",
    size: 12pt,
)

#set heading(numbering: "1.1.1." )
#show heading: it => block(
    spacing: 1.2em,
    text(font: "Noto Sans CJK JP")[#it.body]
)

#show raw: it => text(fill: orange)[#it]


= 感情分析について

自由記述の回答について「感情分析」を行いました。
分析にはPythonの`textblob`パッケージを使っています。
指定した文章を`NLTK`（`National Language Toolkit`）を利用したパターン分析器（`PatternAnalyzer`）に通すと、その「極性」（ポジティブ／ネガティブ）が`[-1, 1]`、
「主観度」（客観／主観）が`[0, 1]`の間の`float`値で返ってきます。

パターン分析器の中身は、中身はきちんと理解できていませんが、英文ならそれなりに評価されるだろうと思って使っています。

極性の値は文章パターンがポジティブ要素かネガティブ要素かを評価したものであり、"文脈"のようなものは考慮されていません。今回の質問になっているDE&Iの取り組みに対してencourage / discourageするか、といったニュアンスを評価した値ではないので、ヒトが読んで感じた印象とはズレている場合もあります。
あくまで参考として使ってください。

#line(length: 100%)

極性によってコメントの背景色を変えています
（#text(fill: olive)[ポジティブ] / #text(fill: gray)[ニュートラル] / #text(fill: orange)[ネガティブ]）。
また、7月28日のdiversityセッションに参加するかしないかでソートしてあります
（Yes → No）。

#line(length: 100%)

#heading(level:1)[#Q]

回答数：#answers.len()

#for answer in answers [
    #let en = answer.q15
    #let ja = answer.q15_ja
    #let polarity = answer.q15_polarity
    #let subjectivity = answer.q15_subjectivity
    #let age = answer.q01
    #let gender = answer.q02
    #let work = answer.q03
    #let job = answer.q05
    #let group = answer.q06
    #let field = answer.q07
    #let session = answer.q11

    #line(length: 100%)
    #parbreak()

    #heading(level: 1, numbering: "【回答 1.1.】")[#gender / #age / #job]
    #let bg = teal
    #let fg = teal
    #if polarity > 0 {
        bg = olive
        fg = olive
    } else if polarity < 0 {
        bg = orange
        fg = orange
    } else {
        bg = silver
        fg = gray
    }

    #align(center)[
        #block(fill: bg, inset: 1.5em, width: 90%, radius: 1em)[
            #align(start)[#en \ （#ja）]
        ]
    ]
    - 感情分析：極性: #text(fill: fg)[#polarity] / 主観度 : #subjectivity
    - グループ：#group / #field
    - 地域（勤務地）：#work
    - Diversityセッション参加: #session
]