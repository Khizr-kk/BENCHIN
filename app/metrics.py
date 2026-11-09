
from collections.abc import Sequence

from pydantic import BaseModel, Field

from app.schemas import EvaluationResult


class AggregateMetrics(BaseModel):
    total_cases: int = Field(ge=0)
    answered_cases: int = Field(ge=0)
    abstained_cases: int = Field(ge=0)
    answer_coverage: float = Field(ge=0, le=1)
    correct_abstention_rate: float | None = Field(
        default=None, ge=0, le=1
    )
    unsupported_claims: int = Field(ge=0)


def calculate_metrics(
    results: Sequence[EvaluationResult],
) -> AggregateMetrics:
    total = len(results)
    answered = sum(not result.actual_abstention for result in results)
    abstained = total - answered

    expected_abstentions = [
        result for result in results if result.expected_abstention
    ]
    correct_abstentions = sum(
        result.expected_abstention and result.actual_abstention
        for result in results
    )

    correct_abstention_rate = (
        correct_abstentions / len(expected_abstentions)
        if expected_abstentions
        else None
    )

    return AggregateMetrics(
        total_cases=total,
        answered_cases=answered,
        abstained_cases=abstained,
        answer_coverage=answered / total if total else 0.0,
        correct_abstention_rate=correct_abstention_rate,
        unsupported_claims=sum(
            result.unsupported_claim_count for result in results
        ),
    )
