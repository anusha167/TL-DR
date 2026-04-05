const BACKEND = "http://127.0.0.1:8080";

// Show current URL
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const url = tabs[0].url;
  document.getElementById("url-display").textContent = url;

  // Yes button
  document.getElementById("yes-btn").addEventListener("click", () => {
    fetch(`${BACKEND}/save-url`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    })
    .then(() => {
      document.getElementById("main-view").style.display = "none";
      document.getElementById("success-view").style.display = "block";
    })
    .catch(err => console.error("Failed to save URL:", err));
  });

  // No button
  document.getElementById("no-btn").addEventListener("click", () => {
    window.close();
  });
});

// Email registration
document.getElementById("email-btn").addEventListener("click", () => {
  const email = document.getElementById("email-input").value;
  if (!email) return;

  fetch(`${BACKEND}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email })
  })
  .then(() => {
    document.getElementById("email-btn").textContent = "✓";
    document.getElementById("email-input").placeholder = "Saved!";
  })
  .catch(err => console.error("Failed to register email:", err));
});