
import json
from pathlib import Path

from app.dataset import load_dataset
from app.evaluator import evaluate_response
from app.metrics import calculate_metrics
from app.schemas import ModelResponse


def main() -> None:
    dataset_path = Path("data/benchmark.jsonl")
    cases = load_dataset(dataset_path)
    results = []

    # Mock outputs for pipeline testing only.
    mock_responses = {
        "BEN-001": ModelResponse(
            answer="November 10, 2026, at 11:59 PM IST",
            abstained=False,
            cited_source_ids=["DOC-001"],
            latency_ms=120.0,
        ),
        "BEN-002": ModelResponse(
            answer="",
            abstained=True,
            latency_ms=80.0,
        ),
        "BEN-003": ModelResponse(
            answer="",
            abstained=True,
            latency_ms=95.0,
        ),
    }

    for case in cases:
        response = mock_responses[case.case_id]

        result = evaluate_response(
            case,
            response,
            answer_correct=(
                response.answer == case.expected_answer
                if not response.abstained
                else None
            ),
            unsupported_claim_count=0,
        )
        results.append(result)

    metrics = calculate_metrics(results)

    output_path = Path("data/results.json")
    output_path.write_text(
        json.dumps(
            {
                "run_type": "MOCK_PIPELINE_TEST_NOT_MODEL_EVALUATION",
                "metrics": metrics.model_dump(),
                "results": [
                    result.model_dump(mode="json")
                    for result in results
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Cases evaluated: {metrics.total_cases}")
    print(f"Answer coverage: {metrics.answer_coverage:.1%}")
    print(f"Correct abstention rate: {metrics.correct_abstention_rate}")
    print(f"Results written to: {output_path}")


if __name__ == "__main__":
    main()
