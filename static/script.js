const uploadForm = document.getElementById("upload-form");
const audioInput = document.getElementById("audio-file");
const uploadBox = document.getElementById("upload-box");
const fileInfo = document.getElementById("file-info");
const fileName = document.getElementById("file-name");
const removeButton = document.getElementById("remove-file");
const audioPreview = document.getElementById("audio-preview");

const transcribeButton = document.getElementById("transcribe-button");
const loading = document.getElementById("loading");
const errorMessage = document.getElementById("error-message");

const resultSection = document.getElementById("result-section");
const transcript = document.getElementById("transcript");
const languageLabel = document.getElementById("language-label");
const processingTime = document.getElementById("processing-time");

const copyButton = document.getElementById("copy-button");
const downloadButton = document.getElementById("download-button");

const referenceTranscript = document.getElementById("reference-transcript");
const evaluateButton = document.getElementById("evaluate-button");
const evaluationLoading = document.getElementById("evaluation-loading");
const evaluationError = document.getElementById("evaluation-error");
const evaluationResults = document.getElementById("evaluation-results");

const werValue = document.getElementById("wer-value");
const cerValue = document.getElementById("cer-value");
const substitutionValue = document.getElementById("substitution-value");
const deletionValue = document.getElementById("deletion-value");
const insertionValue = document.getElementById("insertion-value");
const referenceWordsValue = document.getElementById("reference-words-value");

let selectedFile = null;
let audioUrl = null;

audioInput.addEventListener("change", () => {
    if (audioInput.files.length > 0) {
        selectFile(audioInput.files[0]);
    }
});

function selectFile(file) {
    const allowedExtensions = [
        "wav", "mp3", "ogg", "flac", "aac", "m4a"
    ];

    const extension = file.name.split(".").pop().toLowerCase();

    if (!allowedExtensions.includes(extension)) {
        showError("Unsupported audio format.");
        return;
    }

    if (file.size === 0) {
        showError("The selected file is empty.");
        return;
    }

    if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
    }

    selectedFile = file;
    audioUrl = URL.createObjectURL(file);

    fileName.textContent = file.name;
    fileInfo.classList.remove("hidden");

    audioPreview.src = audioUrl;
    audioPreview.classList.remove("hidden");

    transcribeButton.disabled = false;

    errorMessage.classList.add("hidden");
    resultSection.classList.add("hidden");

    resetEvaluation();
}

removeButton.addEventListener("click", () => {
    selectedFile = null;
    audioInput.value = "";

    if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
        audioUrl = null;
    }

    fileInfo.classList.add("hidden");
    audioPreview.classList.add("hidden");
    audioPreview.removeAttribute("src");

    transcribeButton.disabled = true;
    resultSection.classList.add("hidden");

    resetEvaluation();
});

uploadBox.addEventListener("dragover", (event) => {
    event.preventDefault();
    uploadBox.classList.add("drag-over");
});

uploadBox.addEventListener("dragleave", () => {
    uploadBox.classList.remove("drag-over");
});

uploadBox.addEventListener("drop", (event) => {
    event.preventDefault();
    uploadBox.classList.remove("drag-over");

    const file = event.dataTransfer.files[0];

    if (file) {
        selectFile(file);
    }
});

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove("hidden");
}

function showEvaluationError(message) {
    evaluationError.textContent = message;
    evaluationError.classList.remove("hidden");
}

function resetEvaluation() {
    if (evaluationResults) {
        evaluationResults.classList.add("hidden");
    }

    if (evaluationError) {
        evaluationError.classList.add("hidden");
        evaluationError.textContent = "";
    }

    if (referenceTranscript) {
        referenceTranscript.value = "";
    }

    if (evaluationLoading) {
        evaluationLoading.classList.add("hidden");
    }

    if (werValue) werValue.textContent = "—";
    if (cerValue) cerValue.textContent = "—";
    if (substitutionValue) substitutionValue.textContent = "—";
    if (deletionValue) deletionValue.textContent = "—";
    if (insertionValue) insertionValue.textContent = "—";
    if (referenceWordsValue) referenceWordsValue.textContent = "—";
}

uploadForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!selectedFile) {
        showError("Please select an audio file first.");
        return;
    }

    const formData = new FormData();
    formData.append("audio_file", selectedFile);

    transcribeButton.disabled = true;
    loading.classList.remove("hidden");
    errorMessage.classList.add("hidden");
    resultSection.classList.add("hidden");

    resetEvaluation();

    try {
        const response = await fetch("/transcribe", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || "Transcription failed."
            );
        }

        transcript.value = result.transcript || "";

        languageLabel.textContent =
            result.detected_language_code || result.model || "Prisma v3.0";

        processingTime.textContent =
            result.processing_time != null
                ? `Processing time: ${result.processing_time}s`
                : "Transcription complete";

        resultSection.classList.remove("hidden");

        resultSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (error) {
        showError(error.message || "Something went wrong.");
    } finally {
        loading.classList.add("hidden");
        transcribeButton.disabled = false;
    }
});

evaluateButton.addEventListener("click", async () => {
    const reference = referenceTranscript.value.trim();
    const hypothesis = transcript.value.trim();

    evaluationError.classList.add("hidden");
    evaluationResults.classList.add("hidden");

    if (!hypothesis) {
        showEvaluationError("The generated transcript is empty.");
        return;
    }

    if (!reference) {
        showEvaluationError("Please enter a reference transcript.");
        return;
    }

    evaluateButton.disabled = true;
    evaluationLoading.classList.remove("hidden");

    try {
        const response = await fetch("/evaluate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                reference: reference,
                hypothesis: hypothesis
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || "Evaluation failed."
            );
        }

        werValue.textContent =
            `${(result.wer * 100).toFixed(2)}%`;

        cerValue.textContent =
            `${(result.cer * 100).toFixed(2)}%`;

        substitutionValue.textContent = result.substitutions;
        deletionValue.textContent = result.deletions;
        insertionValue.textContent = result.insertions;
        referenceWordsValue.textContent = result.reference_words;

        evaluationResults.classList.remove("hidden");

        evaluationResults.scrollIntoView({
            behavior: "smooth",
            block: "nearest"
        });

    } catch (error) {
        showEvaluationError(
            error.message || "Unable to evaluate transcription."
        );
    } finally {
        evaluationLoading.classList.add("hidden");
        evaluateButton.disabled = false;
    }
});

copyButton.addEventListener("click", async () => {
    if (!transcript.value.trim()) {
        showError("There is no transcript to copy.");
        return;
    }

    try {
        await navigator.clipboard.writeText(transcript.value);

        copyButton.textContent = "Copied!";

        setTimeout(() => {
            copyButton.textContent = "Copy text";
        }, 1500);

    } catch {
        showError(
            "Unable to copy. Please select and copy the text manually."
        );
    }
});

downloadButton.addEventListener("click", () => {
    const text = transcript.value;

    if (!text.trim()) {
        showError("There is no transcript to download.");
        return;
    }

    const blob = new Blob(
        [text],
        { type: "text/plain;charset=utf-8" }
    );

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "benchin-transcript.txt";

    document.body.appendChild(link);
    link.click();
    link.remove();

    URL.revokeObjectURL(url);
});