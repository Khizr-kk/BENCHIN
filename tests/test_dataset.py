
import json

import pytest

from app.dataset import load_dataset


def write_jsonl(path, records):
    path.write_text(
        "".join(json.dumps(record) + "\n" for record in records),
        encoding="utf-8",
    )


def valid_case(case_id="BEN-TEST-001"):
    return {
        "case_id": case_id,
        "question": "What is the deadline?",
        "case_type": "answerable",
        "evidence": [
            {
                "source_id": "DOC-1",
                "source_name": "Test document",
                "text": "The deadline is November 10, 2026.",
            }
        ],
        "expected_answer": "November 10, 2026",
        "expected_abstention": False,
    }


def test_loads_valid_dataset(tmp_path):
    path = tmp_path / "benchmark.jsonl"
    write_jsonl(path, [valid_case()])

    cases = load_dataset(path)

    assert len(cases) == 1
    assert cases[0].case_id == "BEN-TEST-001"


def test_rejects_duplicate_case_ids(tmp_path):
    path = tmp_path / "benchmark.jsonl"
    write_jsonl(path, [valid_case(), valid_case()])

    with pytest.raises(ValueError, match="Duplicate case_id"):
        load_dataset(path)


def test_rejects_invalid_json(tmp_path):
    path = tmp_path / "benchmark.jsonl"
    path.write_text("{invalid json}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid benchmark record"):
        load_dataset(path)


def test_rejects_empty_dataset(tmp_path):
    path = tmp_path / "benchmark.jsonl"
    path.write_text("\n  \n", encoding="utf-8")

    with pytest.raises(ValueError, match="No benchmark cases"):
        load_dataset(path)
