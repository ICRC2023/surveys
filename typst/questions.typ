#set text(
    font: "Noto Serif CJK JP",
)

#set par(
    leading: 1.5em,
)

#show raw: it => text(
    fill: orange,
    [#it]
    )

//#set heading(numbering: "1.1.1." )
#show heading: it => block(
    fill: blue,
    inset: 1.5em,
    spacing: 1.5em,
    width: 100%,
    text(font: "Noto Sans CJK JP", fill: white)[#it.body]
    )

#outline()

= 質問項目

- Q01. 年齢（Age）
- Q02. 性別（Gender）
- Q03. 勤務地（Workplace）
- Q04. 出身地（Hometown）
- Q05. 肩書き（Job Title）
- Q06. 研究分野（Research Group）
- Q07. 理論・実験・その他（Research Field）
- Q08. 研究分野の在籍期間（Research Years）
- Q09. これまでの自分のキャリアに満足していますか？
- Q10. 家事・育児・介護の時間（Time for housework / childcare / caregiving）【整数値】
- Q01. diversityセッションに参加しますか？

== 所属グループの実態に関する質問（Status of group you belong）

Questions about the actual status of the group to which you belong.
The term "group" will be used here to refer to laboratories at university, working groups within collaborations, etc.

- Q12. DE&Iに関するグループの取り組み具合（`good_poor`）
    - ``q12_gender_balance``
    - ``q12_diversity``
    - ``q12_equity``
    - ``q12_inclusion``
- Q13. 女性研究者の割合（Gender Fraction）【整数値】
- Q14. 上記の割合に対してどう思いますか？
- Q15. 所属するグループのDE&Iの取り組みに関するグッドプラクティスがあれば教えてください【記述式】
- Q16. 所属するグループがDE&Iに関連して取り組む必要があると感じるがあれば教えてください【記述式】

== 個人に関する質問（Individual awareness）

- Q17. DI&Iに関する個人の考え（`agree_disagree`）取り組み度　Group Status
    - ``q17_gender_balance``
    - ``q17_diversity``
    - ``q17_equity``
    - ``q17_inclusion``
- Q18. 上記の考えについて詳しく教えてください【記述式】
- Q19. 科学にはじめて興味を持ったのはいつですか？（Science Interests）
- Q20. 科学分野におけるDE&Iの取り組みに関係して、いま困っていることがあれば教えてください【記述式】
- Q21. 科学分野におけるDE&Iの取り組みを阻害している理由はなんだと思いますか？【記述式】
- Q22. その他のコメント【記述式】


= $chi^(2)$検定のp値マップ

== ぜんぶ

#figure(
    image("../data/main_data/chi2.png"),
    caption: [ぜんぶ]
)

#pagebreak()

== p < 0.05

#figure(
    image("../data/main_data/chi2_p005.png"),
    caption: [p < 0.05]
)

#pagebreak()

== p < 0.01

#figure(
    image("../data/main_data/chi2_p001.png"),
    caption: [p < 0.01]
)

#pagebreak()

== p < 0.005

#figure(
    image("../data/main_data/chi2_p0005.png"),
    caption: [p < 0.005]
)

#pagebreak()

== p < 0.001

#figure(
    image("../data/main_data/chi2_p0001.png"),
    caption: [p < 0.001]
)