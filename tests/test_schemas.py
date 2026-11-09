
import pytest
from pydantic import ValidationError

from app.schemas import (
    BenchmarkCase,
    CaseType,
    EvaluationResult,
    Evidence,
    ModelResponse,
)


@pytest.fixture
def evidence():
    return [
        Evidence(
            source_id="source-1",
            source_name="Project Documentation",
            text="BENCHIN was created in 2026.",
        )
    ]


def test_valid_answerable_case_is_accepted(evidence):
    case = BenchmarkCase(
        case_id="case-001",
        question="When was BENCHIN created?",
        case_type=CaseType.ANSWERABLE,
        evidence=evidence,
        expected_answer="2026",
        expected_abstention=False,
    )

    assert case.case_id == "case-001"
    assert case.expected_abstention is False


def test_answerable_case_requires_expected_answer(evidence):
    with pytest.raises(ValidationError):
        BenchmarkCase(
            case_id="case-002",
            question="When was BENCHIN created?",
            case_type=CaseType.ANSWERABLE,
            evidence=evidence,
            expected_abstention=False,
        )


def test_unanswerable_case_requires_abstention(evidence):
    with pytest.raises(ValidationError):
        BenchmarkCase(
            case_id="case-003",
            question="Who funded BENCHIN?",
            case_type=CaseType.UNANSWERABLE,
            evidence=evidence,
            expected_abstention=False,
        )


def test_conflicting_case_requires_abstention(evidence):
    with pytest.raises(ValidationError):
        BenchmarkCase(
            case_id="case-004",
            question="When was BENCHIN created?",
            case_type=CaseType.CONFLICTING,
            evidence=evidence,
            expected_abstention=False,
        )


def test_model_response_rejects_negative_latency():
    with pytest.raises(ValidationError):
        ModelResponse(
            answer="2026",
            abstained=False,
            latency_ms=-1,
        )


def test_evaluation_result_rejects_negative_unsupported_count():
    with pytest.raises(ValidationError):
        EvaluationResult(
            case_id="case-001",
            case_type=CaseType.ANSWERABLE,
            expected_abstention=False,
            actual_abstention=False,
            unsupported_claim_count=-1,
        )
