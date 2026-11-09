
import re
import unicodedata
from dataclasses import dataclass


@dataclass
class TranscriptionMetrics:
    reference_words: int
    substitutions: int
    deletions: int
    insertions: int
    wer: float
    cer: float


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = text.casefold()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def edit_distance(reference: str, hypothesis: str) -> tuple[int, int, int]:
    ref = list(reference)
    hyp = list(hypothesis)

    rows = len(ref) + 1
    cols = len(hyp) + 1

    dp = [[0] * cols for _ in range(rows)]
    operations = [[None] * cols for _ in range(rows)]

    for i in range(rows):
        dp[i][0] = i
        if i:
            operations[i][0] = "deletion"

    for j in range(cols):
        dp[0][j] = j
        if j:
            operations[0][j] = "insertion"

    for i in range(1, rows):
        for j in range(1, cols):
            if ref[i - 1] == hyp[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
                operations[i][j] = "match"
            else:
                choices = [
                    (dp[i - 1][j - 1] + 1, "substitution"),
                    (dp[i - 1][j] + 1, "deletion"),
                    (dp[i][j - 1] + 1, "insertion"),
                ]
                dp[i][j], operations[i][j] = min(choices)

    substitutions = deletions = insertions = 0

    i, j = len(ref), len(hyp)

    while i > 0 or j > 0:
        operation = operations[i][j]

        if operation == "match":
            i -= 1
            j -= 1
        elif operation == "substitution":
            substitutions += 1
            i -= 1
            j -= 1
        elif operation == "deletion":
            deletions += 1
            i -= 1
        elif operation == "insertion":
            insertions += 1
            j -= 1

    return substitutions, deletions, insertions


def calculate_transcription_metrics(
    reference: str,
    hypothesis: str,
) -> TranscriptionMetrics:

    reference = normalize_text(reference)
    hypothesis = normalize_text(hypothesis)

    ref_words = reference.split()
    hyp_words = hypothesis.split()

    s, d, i = edit_distance(ref_words, hyp_words)

    wer = (s + d + i) / len(ref_words) if ref_words else (
        0.0 if not hyp_words else 1.0
    )

    char_s, char_d, char_i = edit_distance(reference, hypothesis)

    cer = (
        (char_s + char_d + char_i) / len(reference)
        if reference
        else (0.0 if not hypothesis else 1.0)
    )

    return TranscriptionMetrics(
        reference_words=len(ref_words),
        substitutions=s,
        deletions=d,
        insertions=i,
        wer=wer,
        cer=cer,
    )
