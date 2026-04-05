const BACKEND = "http://localhost:5000";
let currentMode = "both";
let currentAudio = null;

// Load articles
async function loadDigest() {
  try {
    const res = await fetch(`${BACKEND}/digest`);
    const articles = await res.json();

    const container = document.getElementById("cards-container");
    const countEl = document.getElementById("article-count");
    const emptyState = document.getElementById("empty-state");

    container.innerHTML = "";

    if (articles.length === 0) {
      emptyState.style.display = "block";
      countEl.textContent = "No articles yet";
      return;
    }

    countEl.textContent = `${articles.length} article${articles.length > 1 ? "s" : ""} ready`;

    articles.forEach(article => {
      const card = createCard(article);
      container.appendChild(card);
    });

  } catch (err) {
    console.error("Failed to load digest:", err);
    document.getElementById("article-count").textContent = "Could not connect to backend";
  }
}

function createCard(article) {
  const card = document.createElement("div");
  card.className = "card";

  const domain = (() => {
    try { return new URL(article.url).hostname.replace("www.", ""); }
    catch { return article.url; }
  })();

  const wordCount = article.summary ? article.summary.split(" ").length : 0;
  const listenTime = Math.ceil(wordCount / 150); // avg reading speed

  card.innerHTML = `
    <div class="card-source">${domain}</div>
    <div class="card-title">${article.title || "Untitled Article"}</div>
    ${currentMode !== "audio" ? `<div class="card-summary">${article.summary || "Summary not available."}</div>` : ""}
    <div class="card-actions">
      ${article.audio_path && currentMode !== "text" ? `
        <button class="play-btn" onclick="playAudio('${article.audio_path}', '${(article.title || "Article").replace(/'/g, "\\'")}')">
          ▶ Listen
        </button>
      ` : ""}
      <a class="card-link" href="${article.url}" target="_blank">View Original ↗</a>
      ${currentMode !== "audio" ? `<span class="listen-time">${listenTime} min read</span>` : ""}
    </div>
  `;

  return card;
}

function playAudio(filename, title) {
  const player = document.getElementById("audio-player");
  const bar = document.getElementById("audio-bar");
  const titleEl = document.getElementById("audio-title");
  const playBtn = document.getElementById("play-btn");

  const audioUrl = `${BACKEND}/audio/${filename}`;
  player.src = audioUrl;
  player.play();

  bar.style.display = "flex";
  titleEl.textContent = title;
  playBtn.textContent = "⏸";

  player.ontimeupdate = () => {
    const progress = (player.currentTime / player.duration) * 100;
    document.getElementById("progress-bar").value = progress || 0;
    document.getElementById("current-time").textContent = formatTime(player.currentTime);
    document.getElementById("total-time").textContent = formatTime(player.duration);
  };

  player.onended = () => { playBtn.textContent = "▶"; };
}

function formatTime(seconds) {
  if (!seconds || isNaN(seconds)) return "0:00";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60).toString().padStart(2, "0");
  return `${m}:${s}`;
}

// Play/pause toggle
document.getElementById("play-btn").addEventListener("click", () => {
  const player = document.getElementById("audio-player");
  const btn = document.getElementById("play-btn");
  if (player.paused) { player.play(); btn.textContent = "⏸"; }
  else { player.pause(); btn.textContent = "▶"; }
});

// Rewind/forward
document.getElementById("rewind-btn").addEventListener("click", () => {
  document.getElementById("audio-player").currentTime -= 15;
});
document.getElementById("forward-btn").addEventListener("click", () => {
  document.getElementById("audio-player").currentTime += 15;
});

// Progress bar scrubbing
document.getElementById("progress-bar").addEventListener("input", (e) => {
  const player = document.getElementById("audio-player");
  player.currentTime = (e.target.value / 100) * player.duration;
});

// Toggle modes
document.querySelectorAll(".toggle").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".toggle").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    currentMode = btn.dataset.mode;
    loadDigest();
  });
});

// Sidebar email
document.getElementById("sidebar-email-btn").addEventListener("click", () => {
  const email = document.getElementById("sidebar-email").value;
  if (!email) return;

  fetch(`${BACKEND}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email })
  }).then(() => {
    document.getElementById("sidebar-email-btn").textContent = "✓ Saved";
    document.getElementById("sidebar-email").placeholder = "Registered!";
  });
});

// Auto-refresh every 10 seconds
loadDigest();
setInterval(loadDigest, 10000);