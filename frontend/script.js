const inputText = document.getElementById("inputText");
const analyzeBtn = document.getElementById("analyzeBtn");

const rawViewBtn = document.getElementById("rawViewBtn");
const structuredViewBtn = document.getElementById("structuredViewBtn");

const rawView = document.getElementById("rawView");
const structuredView = document.getElementById("structuredView");

const rawText = document.getElementById("rawText");
const segmentsEl = document.getElementById("segments");
const themesEl = document.getElementById("themes");

rawViewBtn.addEventListener("click", () => toggleView("raw"));
structuredViewBtn.addEventListener("click", () => toggleView("structured"));
analyzeBtn.addEventListener("click", analyze);

function toggleView(view) {
  if (view === "raw") {
    rawView.classList.remove("hidden");
    structuredView.classList.add("hidden");
    rawViewBtn.classList.add("active");
    structuredViewBtn.classList.remove("active");
  } else {
    structuredView.classList.remove("hidden");
    rawView.classList.add("hidden");
    structuredViewBtn.classList.add("active");
    rawViewBtn.classList.remove("active");
  }
}

const loader = document.getElementById("loader");

async function analyze() {
  console.log("Calling backend...");

  loader.style.display = "inline-block";
  analyzeBtn.disabled = true;

  try {
    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: inputText.value })
    });

    const data = await response.json();
    console.log("Response received", data);

    renderStructured(data.clusters);

  } catch (error) {
    console.error("Error:", error);
  } finally {
    loader.style.display = "none";
    analyzeBtn.disabled = false;
  }
}


function renderRaw(text) {
  rawText.textContent = text;
}

function renderStructured(clusters) {
  segmentsEl.innerHTML = "";
  themesEl.innerHTML = "";

  clusters.forEach(cluster => {

    cluster.segments.forEach(seg => {
      const li = document.createElement("li");
      li.textContent = seg.text;
      segmentsEl.appendChild(li);
    });

    const themeDiv = document.createElement("div");
    themeDiv.className = "theme";

    const list = cluster.segments
      .map(seg => `<li>${seg.text}</li>`)
      .join("");

    themeDiv.innerHTML = `
      <div class="theme-title">${cluster.label}</div>
      <ul>${list}</ul>
    `;

    themesEl.appendChild(themeDiv);
  });
}
