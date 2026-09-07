// Smart Farmer Assistant — Frontend Utilities

document.addEventListener("DOMContentLoaded", function () {
    // Real-time soil health score preview calculator
    const phInput = document.getElementById("ph");
    const nInput = document.getElementById("nitrogen");
    const pInput = document.getElementById("phosphorus");
    const kInput = document.getElementById("potassium");

    if (phInput && nInput && pInput && kInput) {
        const updateSoilScorePreview = function () {
            const ph = parseFloat(phInput.value) || 6.5;
            const n = parseFloat(nInput.value) || 100;
            const p = parseFloat(pInput.value) || 40;
            const k = parseFloat(kInput.value) || 120;

            fetch("/api/soil-score", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ph: ph, nitrogen: n, phosphorus: p, potassium: k })
            })
            .then(res => res.json())
            .then(data => {
                const previewEl = document.getElementById("soilScorePreview");
                if (previewEl) {
                    previewEl.innerText = data.health_score + " / 100";
                }
            })
            .catch(err => console.error("Score fetch error:", err));
        };

        phInput.addEventListener("input", updateSoilScorePreview);
        nInput.addEventListener("input", updateSoilScorePreview);
        pInput.addEventListener("input", updateSoilScorePreview);
        kInput.addEventListener("input", updateSoilScorePreview);
    }
});
