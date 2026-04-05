const BACKEND = "http://127.0.0.1:8080";

chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const url = tabs[0].url;
  document.getElementById("url-display").textContent = url;

  document.getElementById("yes-btn").addEventListener("click", () => {
    const yesBtn = document.getElementById("yes-btn");
    
    // Immediately show tick
    yesBtn.textContent = "✓";
    yesBtn.disabled = true;
    yesBtn.style.background = "#22c55e";
    yesBtn.style.color = "white";
    yesBtn.style.fontSize = "20px";

    fetch(`${BACKEND}/save-url`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    })
    .then(() => {
      // Close popup after a beat
      setTimeout(() => window.close(), 800);
    })
    .catch(err => {
      console.error("Failed to save URL:", err);
      yesBtn.textContent = "✕";
      yesBtn.style.background = "#ef4444";
    });
  });

  document.getElementById("no-btn").addEventListener("click", () => {
    window.close();
  });
});