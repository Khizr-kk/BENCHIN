
import pytest

from app.metrics import calculate_metrics
from app.schemas import CaseType, EvaluationResult


def make_result(
    *,
    case_id: str,
    expected_abstention: bool,
    actual_abstention: bool,
    unsupported_claim_count: int = 0,
) -> EvaluationResult:
    return EvaluationResult(
        case_id=case_id,
        case_type=(
            CaseType.UNANSWERABLE
            if expected_abstention
            else CaseType.ANSWERABLE
        ),
        expected_abstention=expected_abstention,
        actual_abstention=actual_abstention,
        unsupported_claim_count=unsupported_claim_count,
    )


def test_mixed_results_calculate_metrics():
    results = [
        make_result(
            case_id="case-1",
            expected_abstention=False,
            actual_abstention=False,
            unsupported_claim_count=1,
        ),
        make_result(
            case_id="case-2",
            expected_abstention=True,
            actual_abstention=True,
        ),
        make_result(
            case_id="case-3",
            expected_abstention=True,
            actual_abstention=False,
            unsupported_claim_count=2,
        ),
    ]

    metrics = calculate_metrics(results)

    assert metrics.total_cases == 3
    assert metrics.answered_cases == 2
    assert metrics.abstained_cases == 1
    assert metrics.answer_coverage == pytest.approx(2 / 3)
    assert metrics.correct_abstention_rate == pytest.approx(1 / 2)
    assert metrics.unsupported_claims == 3


def test_empty_results_are_handled():
    metrics = calculate_metrics([])

    assert metrics.total_cases == 0
    assert metrics.answer_coverage == 0.0
    assert metrics.correct_abstention_rate is None


def test_abstaining_on_every_case_has_zero_coverage():
    results = [
        make_result(
            case_id="case-1",
            expected_abstention=False,
            actual_abstention=True,
        ),
        make_result(
            case_id="case-2",
            expected_abstention=True,
            actual_abstention=True,
        ),
    ]

    metrics = calculate_metrics(results)

    assert metrics.answer_coverage == 0.0
    assert metrics.correct_abstention_rate == 1.0
