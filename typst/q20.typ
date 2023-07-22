#let Q = "【Q20】Do you have any concerns / problems related to DE&I initiatives in science ?"
#let answers = json("../data/test_data/comment/q20.json")

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
    #let en = answer.q20
    #let ja = answer.q20_ja
    #let polarity = answer.q20_polarity
    #let subjectivity = answer.q20_subjectivity
    #let age = answer.q01
    #let gender = answer.q02
    #let work = answer.q03
    #let job = answer.q05
    #let group = answer.q06
    #let field = answer.q07

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
