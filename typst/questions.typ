#set text(
    font: "Noto Serif CJK JP",
)

#set par(
    leading: 1.5em,
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

= 基本属性

== Q1. 年齢（Age） : What is your age ?

+ 10s
+ 20s
+ 30s
+ 40s
+ 50s
+ 60s
+ 70s
+ 80
+ 90s+
+ Prefer not to answer

== Q2. 性別（Gender）: What gender do you identify as ?

+ Female
+ Male
+ Non-binary
+ Prefer to self-identify
+ Prefer not to answer

== Q3. 勤務地（Workplace）: Which geographical region are you currently working or attending school/university in ?

+ Asia / Japan
+ Asia / Eastern Asia
+ Asia / South-Eastern Asia
+ Asia / Southern Asia
+ Asia / Central Asia
+ Asia / Western Asia
+ Africa / Northern Africa
+ Africa / Western Africa
+ Africa / Middle Africa
+ Africa / Eastern Africa
+ Africa / Southern Africa
+ Europe / North Europe
+ Europe / West Europe
+ Europe / Central Europe
+ Europe / East Europe
+ Europe / South Europe
+ America / North America
+ America / Central America
+ America / South America
+ Oceania
+ Prefer not to answer

==  Q4. 出身地（Hometown）: Which geographical region do you most strongly associate with ?

+ Q3. と同じ

== Q5. 肩書き（Job Title）: What is your job title ?

+ Undergraduate
+ Master
+ Doctorate
+ Postdoc
+ Fixed-tem staff
+ Permanent staff
+ Prefer not to answer


== Q6. 研究分野（Research Group） : Which group do you belong to ?

(Labels are picked from ICRC2023 session name)

+ CRD: Cosmic-ray physics (Direct)
+ CRI: Cosmic-ray physics (Indirect)
+ GA: Gamma-ray astronomy
+ NU: Neutrino astronomy & physics
+ SH: Solar & heliospheric physics
+ DM: Dark-matter physics
+ MM&GW: Multimessenger & gravitational wave
+ O&E: Outreach & education
+ Prefer not to answer

== Q7. 理論・実験・その他（Research Field）: What is your research type ?

Are you a theorist, experimentalist ? If none of the options apply, please fill in "Others"

+ Theorist
+ Experimentarist
+ Prefer not to answer
+ Others（自由記述）

== Q8. 研究分野の在籍期間（Research Years）: How long have you been in this field ?

プルダウン

+ < 1 year
+ 1 - 3 years
+ 3 - 5 years
+ 5 - 10 years
+ > 10years
+ Prefer not to answer

== Q9. これまでの自分のキャリアに満足していますか？: Are you satisfied with your career to date ?

+ Yes
+ No
+ Prefer not to answer

== Q10. 家事・育児・介護の時間（Time for housework / childcare / caregiving） : How much of your time do you spend on housework, childcare, and caregiving ?

- 記述式／回答の検証
- 0 - 24 まで選べるようにする
- -1 = Prefer not to answer


== Q11. diversityセッションに参加しますか？ : Did you already sign up for the diversity session in ICRC2023 ?

+ Yes
+ No
+ Prefer not to answer

= 所属グループの実態に関する質問（Status of group you belong）

Questions about the actual status of the group to which you belong.
The term "group" will be used here to refer to laboratories at university, working groups within collaborations, etc.


== Q12. diversity / equity / inclusionに関する取り組み度　Group Status

What do you think about the level of commitment of your group ?
選択式（グリッド）
Gender balance / Diversity / Equity / Inclusion

+ Very good
+ Good
+ Poor
+ Very Poor
+ No interest
+ Prefer not to answer

✅（必須）女性研究者の割合　Gender Balance
What is the percentage of female researchers in your group?
記述式／回答の検証（-1 - 100）


割合に対してどう思いますか？　What do you think about the ration ?
Not enough / Enough
女性研究者が少ないと思う理由はなんですか？ Why do you think there are not enough female researchers ?
個人に関する質問（Individual awareness）
✅（必須）多様性の取り組みについてどう考えていますか？賛成ですか、反対ですか？
What do you think about current initiatives for diversity, equity & inclusion ? Do you agree or disagree ?
Very agree
Agree
Disagree
Very disagree
No interest
Prefer not to answer
✅あなたの考え（賛成／反対）について詳しく教えてください　Details of thoughts
Could you tell us more about your thoughts (agree / disagree) ?
自由記述
✅（必須）科学に興味を持ったのはいつですか？　Science Interests
When did you first become interested in science ?
Elementary shool
Junior High scool
High school
University
Others
（自由記述）多様性の取り組みに関係して、いま困っていることはありますか？
Do you have any current problems related to DE&I initiatives?
自由記述
（自由記述）多様性の取り組みを阻害している理由はなんだと思いますか？
What reasons do you think are hindering DE&I efforts?
自由記述
