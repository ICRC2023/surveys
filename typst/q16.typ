#let Q = "【Q16】Please let us know if there is anything your group needs to work on or if your group has any problems related to DE&I."
#let answers = json("../test_data/q16.json")

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

#heading(level:1)[#Q]

回答数：#answers.len()

#for answer in answers [
    #let en = answer.q16
    #let ja = answer.q16_ja
    #let polarity = answer.q16_polarity
    #let subjectivity = answer.q16_subjectivity
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
