"""Test config.Config class"""
from titanite import config

CONFIG_DIVERSITY = "../sandbox/config.toml"
CONFIG_REPORT = "../sandbox/config_report.toml"


def test_config_keys():
    c = config.Config(load_from="../sandbox/config.toml")
    c.load()
    t = sorted(c.config.keys())

    expected = sorted(["volumes", "questions", "choices", "options", "overview"])
    assert t == expected


def test_config_volumes():
    c = config.Config(load_from="../sandbox/config.toml")
    c.load()
    t = c.config.get("volumes", "Not defined")

    expected = {
        "main": "../data/main_data",
        "test": "../data/test_data",
    }
    assert t == expected


def test_config_questions():
    c = config.Config(load_from="../sandbox/config.toml")
    c.load()
    t = c.config.get("questions", "Not defined")

    expected = {
        "q01": "【Q1】What is your age ?",
        "q02": "【Q2】What gender do you identify as ?",
        "q03": "【Q3】Which geographical region are you currently working or attending school/university in ?",
        "q04": "【Q4】Which geographical region do you most strongly associate with ?",
        "q05": "【Q5】What is your job title ?",
        "q06": "【Q6】Which group do you belong to ? ",
        "q07": "【Q7】What is your research type ?",
        "q08": "【Q8】How long have you been in this field ?",
        "q09": "【Q9】Are you satisfied with your career to date ?",
        "q10": "【Q10】How many hours, on average, do you spend on housework, childcare, and caregiving per day ?",
        "q11": "【Q11】Did you already sign up for the diversity session in ICRC2023?",
        "q12": "【Q12】What do you think about the initiatives on DE&I of your group?",
        "q13": "【Q13】What is the percentage of female researcher in your group?",
        "q14": "【Q14】What do you think about the percentage above ?",
        "q15": "【Q15】Please let us know If your group has any good practice examples related to DE&I ?",
        "q16": "【Q16】Please let us know if there is anything your group needs to work on or if your group has any problems related to DE&I.",
        "q17": "【Q17】What are your thoughts on diversity, equity & inclusion initiatives ?",
        "q18": "【Q18】Could you tell us more about your thoughts (agree / disagree) ?",
        "q19": "【Q19】When did you first become interested in science ?",
        "q20": "【Q20】Do you have any concerns / problems related to DE&I initiatives in science ?",
        "q21": "【Q21】What reasons do you think are hindering DE&I initiatives in science ?",
        "q22": "【Q22】Comments",
    }

    assert t == expected


def test_config_choices():
    c = config.Config(load_from="../sandbox/config.toml")
    c.load()
    t = c.config.get("choices", "Not defined")

    expected = {
        "age": [
            "10s",
            "20s",
            "30s",
            "40s",
            "50s",
            "60s",
            "70s",
            "80s",
            "90s+",
            "Prefer not to answer",
        ],
        "gender": [
            "Male",
            "Female",
            "Non-binary",
            "Prefer to self-identify",
            "Prefer not to answer",
        ],
        "geoscheme": [
            "Europe / North Europe",
            "Europe / West Europe",
            "Europe / Central Europe",
            "Europe / East Europe",
            "Europe / South Europe",
            "Asia / Japan",
            "Asia / Eastern Asia",
            "Asia / South-Eastern Asia",
            "Asia / Southern Asia",
            "Asia / Central Asia",
            "Asia / Western Asia",
            "America / North America",
            "America / Central America",
            "America / South America",
            "Oceania / Oceania",
            "Africa / Northern Africa",
            "Africa / Western Africa",
            "Africa / Middle Africa",
            "Africa / Eastern Africa",
            "Africa / Southern Africa",
            "Prefer not to answer / Prefer not to answer",
        ],
        "regional": [
            "Europe",
            "Asia",
            "America",
            "Oceania",
            "Africa",
            "Prefer not to answer",
        ],
        "subregional": [
            "North Europe",
            "West Europe",
            "Central Europe",
            "East Europe",
            "South Europe",
            "Japan",
            "Eastern Asia",
            "South-Eastern Asia",
            "Southern Asia",
            "Central Asia",
            "Western Asia",
            "North America",
            "Central America",
            "South America",
            "Oceania",
            "Northern Africa",
            "Western Africa",
            "Middle Africa",
            "Eastern Africa",
            "Southern Africa",
            "Prefer not to answer",
        ],
        "job_title": [
            "Undergraduate",
            "Master",
            "Doctrate",
            "Postdoc",
            "Fixed-term staff",
            "Permanent staff",
            "Prefer not to answer",
        ],
        "research_group": [
            "CRD: Cosmic-ray physics (Direct)",
            "CRI: Cosmic-ray physics (Indirect)",
            "GA: Gamma-ray astronomy",
            "NU: Neutrino astronomy & physics",
            "SH: Solar & heliospheric physics",
            "DM: Dark-matter physics",
            "MM&GW: Multimessenger & gravitational wave",
            "O&E: Outreach & education",
            "Prefer not to answer",
        ],
        "research_field": [
            "Theorist",
            "Experimentalist",
            "Others",
            "Prefer not to answer",
        ],
        "research_years": [
            "< 1 year",
            "1 - 3 years",
            "3 - 5 years",
            "5 - 10 yeas",
            "> 10 years",
            "Prefer not to answer",
        ],
        "yes_no": ["Yes", "No", "Prefer not to answer"],
        "good_poor": [
            "Very Good",
            "Good",
            "Poor",
            "Very Poor",
            "No interest",
            "Prefer not to answer",
        ],
        "agree_disagree": ["Agree", "Disagree", "No interest", "Prefer not to answer"],
        "school": [
            "Pre school",
            "Elementary school",
            "Junior High school",
            "High school",
            "University",
            "Prefer not to answer",
        ],
        "cluster": ["Cluster1", "Cluster2", "Cluster3", "Cluster4", "Others"],
    }
    assert t == expected


def test_config_options():
    c = config.Config(load_from="../sandbox/config.toml")
    c.load()
    t = c.config.get("options", "Not defined")

    expected = [
        {
            "name": "q01",
            "title": "Age Group",
            "description": "【Q1】What is your age?",
            "type": "categorical",
            "category": "age",
        },
        {
            "name": "q02",
            "title": "Gender Identity",
            "description": "【Q2】What gender do you identify as?",
            "type": "categorical",
            "category": "gender",
        },
        {
            "name": "q03",
            "title": "Workplace",
            "description": "【Q3】Which geographical region are you currently working or attending school/university in?",
            "type": "categorical",
            "category": "geoscheme",
        },
        {
            "name": "q03_regional",
            "title": "Workplace (Region)",
            "description": "【Q3】Which geographical region are you currently working or attending school/university in?",
            "type": "categorical",
            "category": "regional",
        },
        {
            "name": "q03_subregional",
            "title": "Workplace (Sub Region)",
            "description": "【Q3】Which geographical region are you currently working or attending school/university in?",
            "type": "categorical",
            "category": "subregional",
        },
        {
            "name": "q04",
            "title": "Birthplace/Hometown",
            "description": "【Q4】Which geographical region do you most strongly associate with?",
            "type": "categorical",
            "category": "geoscheme",
        },
        {
            "name": "q04_regional",
            "title": "Birthplace/Hometown (Region)",
            "description": "【Q4】Which geographical region do you most strongly associate with?",
            "type": "categorical",
            "category": "regional",
        },
        {
            "name": "q04_subregional",
            "title": "Birthplace/Hometown (Sub Region)",
            "description": "【Q4】Which geographical region do you most strongly associate with?",
            "type": "categorical",
            "category": "subregional",
        },
        {
            "name": "q05",
            "title": "Job Title",
            "description": "【Q5】What is your job title?",
            "type": "categorical",
            "category": "job_title",
        },
        {
            "name": "q06",
            "title": "Research Group",
            "description": "【Q6】Which group do you belong to?",
            "type": "categorical",
            "category": "research_group",
        },
        {
            "name": "q07",
            "title": "Research Field",
            "description": "【Q7】What is your research type?",
            "type": "categorical",
            "category": "research_field",
        },
        {
            "name": "q08",
            "title": "Research Years",
            "description": "【Q8】How long have you been in this field?",
            "type": "categorical",
            "category": "research_years",
        },
        {
            "name": "q09",
            "title": "Career Satisfaction",
            "description": "【Q9】Are you satisfied with your career to date?",
            "type": "categorical",
            "category": "yes_no",
        },
        {
            "name": "q10",
            "title": "Hours on housework, childcare, caregiving per day",
            "description": "【Q10】How many hours, on average, do you spend on housework, childcare, and caregiving per day?",
            "type": "numerical",
        },
        {
            "name": "q11",
            "title": "Diversity Session Signup",
            "description": "【Q11】Did you already sign up for the diversity session in ICRC2023?",
            "type": "categorical",
            "category": "yes_no",
        },
        {
            "name": "q12_genderbalance",
            "title": "Group Initiatives on Gender Balance",
            "description": "【Q12】What do you think about the initiatives on DE&I of your group?",
            "type": "categorical",
            "category": "good_poor",
        },
        {
            "name": "q12_diversity",
            "title": "Group Initiatives on Diversity",
            "description": "【Q12】What do you think about the initiatives on DE&I of your group?",
            "type": "categorical",
            "category": "good_poor",
        },
        {
            "name": "q12_equity",
            "title": "Group Initiatives on Equity",
            "description": "【Q12】What do you think about the initiatives on DE&I of your group?",
            "type": "categorical",
            "category": "good_poor",
        },
        {
            "name": "q12_inclusion",
            "title": "Group Initiatives on Inclusion",
            "description": "【Q12】What do you think about the initiatives on DE&I of your group?",
            "type": "categorical",
            "category": "good_poor",
        },
        {
            "name": "q13",
            "title": "Percentage of Female Researchers in Group",
            "description": "【Q13】What is the percentage of female researcher in your group?",
            "type": "numerical",
        },
        {
            "name": "q14",
            "title": "Percentage",
            "description": "【Q14】What do you think about the percentage above?",
            "type": "categorical",
            "category": "good_poor",
        },
        {
            "name": "q15",
            "title": "Good Practices",
            "description": "【Q15】Please let us know If your group has any good practice examples related to DE&I?",
            "type": "comment",
        },
        {
            "name": "q16",
            "title": "Problems",
            "description": "【Q16】Please let us know if there is anything your group needs to work on or if your group has any problems related to DE&I.",
            "type": "comment",
        },
        {
            "name": "q17_genderbalance",
            "title": "Personal Attitude on Gender Balance Initiatives",
            "description": "【Q17】What are your thoughts on diversity, equity & inclusion initiatives?",
            "type": "categorical",
            "category": "agree_disagree",
        },
        {
            "name": "q17_diversity",
            "title": "Personal Attitude on Diversity Initiatives",
            "description": "【Q17】What are your thoughts on diversity, equity & inclusion initiatives?",
            "type": "categorical",
            "category": "agree_disagree",
        },
        {
            "name": "q17_equity",
            "title": "Personal Attitude on Equity Initiatives",
            "description": "【Q17】What are your thoughts on diversity, equity & inclusion initiatives?",
            "type": "categorical",
            "category": "agree_disagree",
        },
        {
            "name": "q17_inclusion",
            "title": "Personal Attitude on Inclusion Initiatives",
            "description": "【Q17】What are your thoughts on diversity, equity & inclusion initiatives?",
            "type": "categorical",
            "category": "agree_disagree",
        },
        {
            "name": "q18",
            "title": "Reasons",
            "description": "【Q18】Could you tell us more about your thoughts?",
            "type": "comment",
        },
        {
            "name": "q19",
            "title": "Science Interest",
            "description": "【Q19】When did you first become interested in science?",
            "type": "categorical",
            "category": "school",
        },
        {
            "name": "q20",
            "title": "Concerns/Problems Related to DE&I Initiatives in Science",
            "description": "【Q20】Do you have any concerns / problems related to DE&I initiatives in science?",
            "type": "comment",
        },
        {
            "name": "q21",
            "title": "Hindering",
            "description": "【Q21】What reasons do you think are hindering DE&I initiatives in science?",
            "type": "comment",
        },
        {
            "name": "q22",
            "title": "Comments",
            "description": "【Q22】Comments",
            "type": "comment",
        },
    ]
    assert t == expected


def test_config_overview():
    c = config.Config(load_from="../sandbox/config.toml")
    c.load()
    t = c.config.get("overview", "Not defined")

    expected = [
        {"name": "in-person", "total": 1102, "male": 852, "female": 241, "others": 9},
        {"name": "online", "total": 304, "male": 220, "female": 84, "others": 0},
        {"name": "pre-survey", "total": 295, "male": 195, "female": 90, "others": 10},
    ]

    assert t == expected


def test_config_names():
    c = config.Config(load_from=CONFIG_DIVERSITY)
    c.load()
    t = c.get_names()

    expected = [
        "q01",
        "q02",
        "q03",
        "q03_regional",
        "q03_subregional",
        "q04",
        "q04_regional",
        "q04_subregional",
        "q05",
        "q06",
        "q07",
        "q08",
        "q09",
        "q10",
        "q11",
        "q12_diversity",
        "q12_equity",
        "q12_genderbalance",
        "q12_inclusion",
        "q13",
        "q14",
        "q15",
        "q16",
        "q17_diversity",
        "q17_equity",
        "q17_genderbalance",
        "q17_inclusion",
        "q18",
        "q19",
        "q20",
        "q21",
        "q22",
    ]

    assert t == expected


def test_config_titles():
    c = config.Config(load_from=CONFIG_DIVERSITY)
    c.load()
    t = c.get_titles()

    expected = {
        "q01": "Age Group",
        "q02": "Gender Identity",
        "q03": "Workplace",
        "q03_regional": "Workplace (Region)",
        "q03_subregional": "Workplace (Sub Region)",
        "q04": "Birthplace/Hometown",
        "q04_regional": "Birthplace/Hometown (Region)",
        "q04_subregional": "Birthplace/Hometown (Sub Region)",
        "q05": "Job Title",
        "q06": "Research Group",
        "q07": "Research Field",
        "q08": "Research Years",
        "q09": "Career Satisfaction",
        "q10": "Hours on housework, childcare, caregiving per day",
        "q11": "Diversity Session Signup",
        "q12_genderbalance": "Group Initiatives on Gender Balance",
        "q12_diversity": "Group Initiatives on Diversity",
        "q12_equity": "Group Initiatives on Equity",
        "q12_inclusion": "Group Initiatives on Inclusion",
        "q13": "Percentage of Female Researchers in Group",
        "q14": "Percentage",
        "q15": "Good Practices",
        "q16": "Problems",
        "q17_genderbalance": "Personal Attitude on Gender Balance Initiatives",
        "q17_diversity": "Personal Attitude on Diversity Initiatives",
        "q17_equity": "Personal Attitude on Equity Initiatives",
        "q17_inclusion": "Personal Attitude on Inclusion Initiatives",
        "q18": "Reasons",
        "q19": "Science Interest",
        "q20": "Concerns/Problems Related to DE&I Initiatives in Science",
        "q21": "Hindering",
        "q22": "Comments",
    }

    assert t == expected


def test_config_descriptions():
    c = config.Config(load_from=CONFIG_DIVERSITY)
    c.load()
    t = c.get_descriptions()

    expected = {
        "q01": "【Q1】What is your age?",
        "q02": "【Q2】What gender do you identify as?",
        "q03": "【Q3】Which geographical region are you currently working or attending school/university in?",
        "q03_regional": "【Q3】Which geographical region are you currently working or attending school/university in?",
        "q03_subregional": "【Q3】Which geographical region are you currently working or attending school/university in?",
        "q04": "【Q4】Which geographical region do you most strongly associate with?",
        "q04_regional": "【Q4】Which geographical region do you most strongly associate with?",
        "q04_subregional": "【Q4】Which geographical region do you most strongly associate with?",
        "q05": "【Q5】What is your job title?",
        "q06": "【Q6】Which group do you belong to?",
        "q07": "【Q7】What is your research type?",
        "q08": "【Q8】How long have you been in this field?",
        "q09": "【Q9】Are you satisfied with your career to date?",
        "q10": "【Q10】How many hours, on average, do you spend on housework, childcare, and caregiving per day?",
        "q11": "【Q11】Did you already sign up for the diversity session in ICRC2023?",
        "q12_genderbalance": "【Q12】What do you think about the initiatives on DE&I of your group?",
        "q12_diversity": "【Q12】What do you think about the initiatives on DE&I of your group?",
        "q12_equity": "【Q12】What do you think about the initiatives on DE&I of your group?",
        "q12_inclusion": "【Q12】What do you think about the initiatives on DE&I of your group?",
        "q13": "【Q13】What is the percentage of female researcher in your group?",
        "q14": "【Q14】What do you think about the percentage above?",
        "q15": "【Q15】Please let us know If your group has any good practice examples related to DE&I?",
        "q16": "【Q16】Please let us know if there is anything your group needs to work on or if your group has any problems related to DE&I.",
        "q17_genderbalance": "【Q17】What are your thoughts on diversity, equity & inclusion initiatives?",
        "q17_diversity": "【Q17】What are your thoughts on diversity, equity & inclusion initiatives?",
        "q17_equity": "【Q17】What are your thoughts on diversity, equity & inclusion initiatives?",
        "q17_inclusion": "【Q17】What are your thoughts on diversity, equity & inclusion initiatives?",
        "q18": "【Q18】Could you tell us more about your thoughts?",
        "q19": "【Q19】When did you first become interested in science?",
        "q20": "【Q20】Do you have any concerns / problems related to DE&I initiatives in science?",
        "q21": "【Q21】What reasons do you think are hindering DE&I initiatives in science?",
        "q22": "【Q22】Comments",
    }

    assert t == expected
