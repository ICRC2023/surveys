#let Q = "【Q18】Could you tell us more about your thoughts (agree / disagree) ?"
#let answers = json("../data/test_data/comment/q18.json")

#set document(
    title: Q
)
#set page(
    header: [
        #set text(8pt)
        #h(1fr) updated: 2023/07/20
        ],
    footer: "ICRC2023 Diversity Session",
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

#heading(level:1)[#Q]

回答数：#answers.len()

#for answer in answers [
    #let en = answer.q18
    #let ja = answer.q18_ja
    #let polarity = answer.q18_polarity
    #let subjectivity = answer.q18_subjectivity
    #let age = answer.q01
    #let gender = answer.q02
    #let work = answer.q03
    #let job = answer.q05
    #let group = answer.q06
    #let field = answer.q07

    #line(length: 100%)
    #parbreak()

    #heading(level: 1, numbering: "【回答 1.1.】")[#gender / #age / #job]
    #let bg = teal
    #if polarity > 0 {
        bg = aqua
    } else if polarity < 0 {
        bg = orange
    } else {
        bg = olive
    }

    #align(center)[
        #block(fill: bg, inset: 1.5em, width: 90%, radius: 1em)[
            #align(start)[#en \ （#ja）]
        ]
    ]
    - 感情分析：極性: #polarity / 主観度 : #subjectivity
    - 地域（勤務地）：#work
    - グループ：#group / #field
    ]