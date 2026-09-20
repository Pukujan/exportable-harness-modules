;/* === kilo-claude-hot-start === */
(() => {
  if (typeof document === "undefined") return;
  if (window.__kiloClaudeCssHotReload) return;
  window.__kiloClaudeCssHotReload = true;
  const STYLE_ID = "kilo-claude-md-hot";
  let last = "";
  const tick = async () => {
    try {
      const href = Array.from(document.querySelectorAll('link[rel="stylesheet"]'))
        .map((node) => node.href)
        .find((value) => /webview\.css|agent-manager\.css/.test(value));
      if (!href) return;
      const url = href.replace(/[^/]+\.css(\?.*)?$/, "kilo-user-markdown.css") + "?t=" + Date.now();
      const res = await fetch(url, { cache: "no-store" });
      if (!res.ok) return;
      const text = await res.text();
      if (text === last) return;
      last = text;
      let style = document.getElementById(STYLE_ID);
      if (!style) {
        style = document.createElement("style");
        style.id = STYLE_ID;
        document.documentElement.appendChild(style);
      }
      style.textContent = text;
    } catch (_err) {}
  };
  tick();
  setInterval(tick, 1000);
})();
;/* === kilo-claude-hot-end === */
