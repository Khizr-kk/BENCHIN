
import pytest

from app.dataset import load_dataset
from app.evaluator import evaluate_response
from app.schemas import ModelResponse


@pytest.fixture
def answerable_case():
    return load_dataset("data/benchmark.jsonl")[0]


def test_records_answered_response(answerable_case):
    response = ModelResponse(
        answer="November 10, 2026, at 11:59 PM IST",
        abstained=False,
        cited_source_ids=["DOC-001"],
        latency_ms=125.0,
    )

    result = evaluate_response(
        answerable_case,
        response,
        answer_correct=True,
        unsupported_claim_count=0,
    )

    assert result.case_id == "BEN-001"
    assert result.actual_abstention is False
    assert result.answer_correct is True
    assert result.unsupported_claim_count == 0


def test_records_unsupported_claims(answerable_case):
    response = ModelResponse(
        answer="November 20, 2026",
        abstained=False,
        latency_ms=80.0,
    )

    result = evaluate_response(
        answerable_case,
        response,
        answer_correct=False,
        unsupported_claim_count=1,
    )

    assert result.answer_correct is False
    assert result.unsupported_claim_count == 1


def test_rejects_negative_unsupported_claim_count(answerable_case):
    response = ModelResponse(
        answer="",
        abstained=True,
        latency_ms=20.0,
    )

    with pytest.raises(ValueError, match="cannot be negative"):
        evaluate_response(
            answerable_case,
            response,
            unsupported_claim_count=-1,
        )
