#set page(
    header: "2023/07/20",
    numbering: "1 / 1",
)

#set text(
    font: (
        "HackGen",
    ),
    size: 14pt,
    weight: "regular",
    lang: "ja"
)

#let answers = json("comment_q20.json")

= 【Q20】Do you have any concerns / problems related to DE&I initiatives in science ?

#for answer in answers [
    #line(length: 100%)

    #answer.q20
    \
    #text(fill: luma(100), size: 12pt)[#answer.q20_ja]
    \
    #text(fill: luma(50), size: 10pt)[感情分析：極性: #answer.q20_polarity / 主体性 : #answer.q20_subjectivity]
    \
    #text(fill: luma(50), size: 8pt)[属性：#answer.q1, #answer.q2, #answer.q3, #answer.q5, #answer.q6, #answer.q7]
    ]
