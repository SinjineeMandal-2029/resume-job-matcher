const API_URL = "https://resume-job-matcher-kde4.onrender.com/analyze";

const form = document.getElementById("form");
const btn = document.getElementById("btn");
const statusEl = document.getElementById("status");
const results = document.getElementById("results");

function showStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.className = isError ? "status error" : "status";
}

function fillChips(containerId, items, cssClass) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";
  if (items.length === 0) {
    container.textContent = "None";
    return;
  }
  items.forEach((item) => {
    const chip = document.createElement("span");
    chip.className = "chip " + cssClass;
    chip.textContent = item;
    container.appendChild(chip);
  });
}

function render(data) {
  if (data.coverage === null) {
    showStatus("No known skills were found in this job description.", true);
    results.classList.add("hidden");
    return;
  }
  document.getElementById("barFill").style.width = data.coverage + "%";
  document.getElementById("coverageText").textContent =
    data.coverage + "% of the skills this job asks for are on your resume";
  fillChips("matched", data.matched, "ok");
  fillChips("missing", data.missing, "bad");
  document.getElementById("tfidfText").textContent =
    "Text similarity (TF-IDF): " + data.tfidf_score + "%";
  results.classList.remove("hidden");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  btn.disabled = true;
  results.classList.add("hidden");
  showStatus("Analyzing... the first request can take a few seconds.");

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      body: new FormData(form),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Something went wrong.");
    showStatus("");
    render(data);
  } catch (err) {
    if (err instanceof TypeError) {
      showStatus("Cannot reach the server. Is the backend running?", true);
    } else {
      showStatus(err.message, true);
    }
  } finally {
    btn.disabled = false;
  }
});