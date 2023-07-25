#from titanite import config
from titanite import config


def init_config():
    settings = {"load_from": "../sandbox/config.toml"}
    c = config.Config(**settings)
    cfg = c.load_config()

    q = cfg.get("questions").keys()
    x = cfg.get("choices").keys()

    expected_q = [
        "q01",
        "q02",
        "q03",
        "q04",
        "q05",
        "q06",
        "q07",
        "q08",
        "q09",
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
        "cluster",
    ]

    assert q == expected_q
    assert x == expected_x
