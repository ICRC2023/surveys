#let Q = "【Q15】Please let us know If your group has any good practice examples related to DE&I ?"
#let answers = json("../test_data/q15.json")

#set document(
    title: Q
)

#set page(
    header: [
        #set text(8pt)
        #h(1fr) updated: 2023/07/20
        ],
    numbering: "1 / 1",
)

#set par(
    leading: 1em,
)

#set text(
    font: (
        "HackGen",
    ),
    size: 14pt,
    weight: "regular",
    lang: "ja"
)

= 感情分析について

自由記述の回答について「感情分析」をしました。
分析にはPythonのtextblobパッケージを使っています。
与えた文章に対して`NLTK（National Language Toolkit`）を利用したパターン分析器（`PatternAnalyzer`）によって、
文章の「極性」（ポジティブ／ネガティブ）が`[-1, 1]`、
「主観度」（客観／主観）が`[0, 1]`の間の`float`値で返ってきます。

パターン分析器は、文脈は考慮していないモデルのようです。
人間が読んで感じるものとはズレていることがあるかもしれません。

#line(length: 100%)

#heading(level:1)[#Q]

回答数：#answers.len()

#for answer in answers [
    #let en = answer.q15
    #let ja = answer.q15_ja
    #let polarity = answer.q15_polarity
    #let subjectivity = answer.q15_subjectivity
    #let age = answer.q1
    #let gender = answer.q2
    #let work = answer.q3
    #let job = answer.q5
    #let group = answer.q6
    #let field = answer.q7

    #parbreak()
    #heading(level: 1, numbering: "【回答 1.1.】")[
        #parbreak()
        #en
        #parbreak()
        ]
    #parbreak()
    #text(fill: luma(100), size: 12pt)[（自動翻訳）#ja]
    #parbreak()
    #text(fill: luma(50), size: 10pt)[感情分析：極性: #polarity / 主観度 : #subjectivity]
    #parbreak()
    #text(fill: luma(50), size: 8pt)[属性：#age, #gender, #work, #job, #group, #field]
    #parbreak()
    #line(length: 100%, stroke: luma(200))
    #parbreak()
    ]
