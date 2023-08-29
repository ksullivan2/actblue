import json
import os

import pytest
from main import scrub



@pytest.mark.parametrize("case_path", [f.path for f in os.scandir('./tdd_cases') if f.is_dir()])
def test_tdd_case(case_path: str):
    input = json.dumps(open(f"{case_path}/input.json", "r").readlines())
    output = json.dumps(open(f"{case_path}/output.json", "r").readlines())
    sensitive_fields = open(f"{case_path}/sensitive_fields.txt", "r").readlines()
    assert scrub(input, sensitive_fields) == output