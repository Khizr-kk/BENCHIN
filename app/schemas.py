
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class CaseType(StrEnum):
    ANSWERABLE = "answerable"
    UNANSWERABLE = "unanswerable"
    CONFLICTING = "conflicting"


class Evidence(BaseModel):
    source_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    source_name: str = Field(min_length=1)


class BenchmarkCase(BaseModel):
    case_id: str = Field(min_length=1)
    question: str = Field(min_length=1)
    case_type: CaseType
    evidence: list[Evidence] = Field(min_length=1)
    expected_answer: str | None = None
    expected_abstention: bool

    @model_validator(mode="after")
    def validate_expected_behavior(self):
        if self.case_type == CaseType.ANSWERABLE:
            if self.expected_abstention:
                raise ValueError(
                    "Answerable cases must not expect abstention."
                )
            if not self.expected_answer:
                raise ValueError(
                    "Answerable cases require an expected answer."
                )

        if self.case_type == CaseType.UNANSWERABLE:
            if not self.expected_abstention:
                raise ValueError(
                    "Unanswerable cases must expect abstention."
                )

        if self.case_type == CaseType.CONFLICTING:
            if not self.expected_abstention:
                raise ValueError(
                    "Conflicting cases must expect abstention "
                    "in this benchmark version."
                )

        return self


class ModelResponse(BaseModel):
    answer: str
    abstained: bool
    cited_source_ids: list[str] = Field(default_factory=list)
    latency_ms: float = Field(ge=0)


class EvaluationResult(BaseModel):
    case_id: str
    case_type: CaseType
    expected_abstention: bool
    actual_abstention: bool
    answer_correct: bool | None = None
    unsupported_claim_count: int = Field(ge=0)
