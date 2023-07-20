#set page(
    header: [
        #set text(8pt)
        #h(1fr) updated: 2023/07/20
        ],
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

#let answers = json("../test_data/q15.json")


= 【Q15】Please let us know If your group has any good practice examples related to DE&I ?


#for answer in answers [
    #line(length: 100%)
    #parbreak()
    #answer.q15
    #parbreak()
    #text(fill: luma(100), size: 12pt)[#answer.q15_ja]
    #parbreak()
    #text(fill: luma(50), size: 10pt)[感情分析：極性: #answer.q15_polarity / 主観度 : #answer.q15_subjectivity]
    #parbreak()
    #text(fill: luma(50), size: 8pt)[属性：#answer.q1, #answer.q2, #answer.q3, #answer.q5, #answer.q6, #answer.q7]
    #parbreak()
    ]
