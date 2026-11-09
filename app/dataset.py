
import json
from pathlib import Path

from app.schemas import BenchmarkCase


def load_dataset(path: str | Path) -> list[BenchmarkCase]:
    """Load and validate a JSONL benchmark dataset."""
    dataset_path = Path(path)
    cases: list[BenchmarkCase] = []
    seen_ids: set[str] = set()

    with dataset_path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                raw_case = json.loads(line)
                case = BenchmarkCase.model_validate(raw_case)
            except (json.JSONDecodeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid benchmark record at "
                    f"{dataset_path}:{line_number}: {exc}"
                ) from exc

            if case.case_id in seen_ids:
                raise ValueError(
                    f"Duplicate case_id {case.case_id!r} "
                    f"at {dataset_path}:{line_number}"
                )

            seen_ids.add(case.case_id)
            cases.append(case)

    if not cases:
        raise ValueError(f"No benchmark cases found in {dataset_path}")

    return cases
