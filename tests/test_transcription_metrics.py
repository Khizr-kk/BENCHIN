from app.transcription_metrics import calculate_transcription_metrics


def test_identical_transcription():
    result = calculate_transcription_metrics("hello world", "hello world")

    assert result.wer == 0.0
    assert result.cer == 0.0


def test_word_substitution():
    result = calculate_transcription_metrics("hello world", "hello there")

    assert result.substitutions == 1
    assert result.deletions == 0
    assert result.insertions == 0
    assert result.wer == 0.5


def test_word_deletion():
    result = calculate_transcription_metrics("a b c", "a c")

    assert result.deletions == 1
    assert result.wer == 1 / 3


def test_word_insertion():
    result = calculate_transcription_metrics("a c", "a b c")

    assert result.insertions == 1
    assert result.wer == 0.5


def test_empty_reference():
    result = calculate_transcription_metrics("", "hello")

    assert result.wer == 1.0
    assert result.cer == 1.0


def test_whitespace_normalization():
    result = calculate_transcription_metrics(
        "hello   world",
        "hello world",
    )

    assert result.wer == 0.0
    assert result.cer == 0.0
