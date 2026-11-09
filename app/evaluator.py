
from app.schemas import BenchmarkCase, EvaluationResult, ModelResponse


def evaluate_response(
    case: BenchmarkCase,
    response: ModelResponse,
    *,
    unsupported_claim_count: int = 0,
    answer_correct: bool | None = None,
) -> EvaluationResult:
    """Score a response's abstention behavior and supplied verification results.

    Claim verification and answer correctness must be determined separately.
    This function does not infer factual correctness from text similarity.
    """
    if unsupported_claim_count < 0:
        raise ValueError("unsupported_claim_count cannot be negative")

    return EvaluationResult(
        case_id=case.case_id,
        case_type=case.case_type,
        expected_abstention=case.expected_abstention,
        actual_abstention=response.abstained,
        answer_correct=answer_correct,
        unsupported_claim_count=unsupported_claim_count,
    )
