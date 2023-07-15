from titanite import config


def init_config():
    settings = {"confd": "../sandbox/", "fname": "config.toml"}

    c = config.Config(**settings)
    c.load()

    q = c.get("questions").keys()
    x = c.get("choices").keys()

    expected_q = [
        "q1",
        "q2",
        "q3",
        "q4",
        "q5",
        "q6",
        "q7",
        "q8",
        "q9",
        "q10",
        "q11",
        "q12",
        "q13",
        "q14",
        "q15",
        "q16",
        "q17",
        "q18",
        "q19",
        "q20",
        "q21",
        "q22",
    ]
    expected_x = [
        "age",
        "gender",
        "regional",
        "subregional",
        "job_title",
        "research_group",
        "research_field",
        "research_years",
        "yes_no",
        "good_poor",
        "agree_disagree",
        "school",
    ]

    assert q == expected_q
    assert x == expected_x
