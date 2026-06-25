document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.getElementById("text");
    const charCount = document.getElementById("charCount");
    const wordCount = document.getElementById("wordCount");
    const form = document.getElementById("sentimentForm");
    const analyzeBtn = document.querySelector(".analyzeBtn");

    function updateCounter() {
        if (!textarea) return;

        const text = textarea.value;
        charCount.innerText = text.length + " Characters";

        const words = text.trim() === "" ? 0 : text.trim().split(/\s+/).length;
        wordCount.innerText = words + " Words";
    }

    if (textarea) {
        textarea.addEventListener("input", updateCounter);
        updateCounter();
    }

    if (form && analyzeBtn) {
        form.addEventListener("submit", function () {
            analyzeBtn.innerHTML =
                '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
            analyzeBtn.disabled = true;
        });
    }

    window.clearText = function () {
        if (!textarea) return;
        textarea.value = "";
        updateCounter();
        textarea.focus();
    };

    window.fillExample = function (text) {
        if (!textarea) return;
        textarea.value = text;
        updateCounter();
        textarea.focus();
    };

    window.copyResult = function () {
        const inputText = document.querySelector(".inputText");
        const badge = document.querySelector(".badge");
        const confidence = document.querySelector(".progressTitle span:last-child");

        if (!inputText || !badge || !confidence) {
            alert("No result available to copy.");
            return;
        }

        const resultText =
            "Text: " + inputText.innerText.trim() + "\n" +
            "Sentiment: " + badge.innerText.trim() + "\n" +
            "Confidence: " + confidence.innerText.trim();

        navigator.clipboard.writeText(resultText)
            .then(function () {
                alert("Result copied successfully!");
            })
            .catch(function () {
                alert("Copy failed. Please try again.");
            });
    };
});