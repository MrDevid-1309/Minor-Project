(() => {
  const container = document.getElementById("floating-code");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (!container || reducedMotion.matches) return;

  const symbols = ["0", "1", "{}", "</>", "AI", "ML", "()", "[]", "=>", "def", "class", "import", "#", "$", ";"];
  const colors = ["#67E8F9", "#93C5FD", "#C4B5FD", "#DDD6FE", "#A7F3D0", "#F8FAFC"];
  let resizeTimer;

  function renderSymbols() {
    const width = window.innerWidth;
    const count = width < 480 ? 12 : width < 900 ? 18 : 24;
    const fragment = document.createDocumentFragment();

    for (let index = 0; index < count; index += 1) {
      const element = document.createElement("span");
      const duration = 24 + Math.random() * 28;
      element.className = "floating-code-symbol";
      if (Math.random() < 0.22) element.classList.add("is-glowing");
      element.textContent = symbols[Math.floor(Math.random() * symbols.length)];
      element.dataset.symbolId = String(index);
      element.style.setProperty("--symbol-x", `${Math.random() * 100}%`);
      element.style.setProperty("--symbol-size", `${11 + Math.random() * 12}px`);
      element.style.setProperty("--symbol-duration", `${duration}s`);
      element.style.setProperty("--symbol-delay", `${-Math.random() * duration}s`);
      element.style.setProperty("--symbol-opacity", `${0.25 + Math.random() * 0.4}`);
      element.style.setProperty("--symbol-sway", `${-5 + Math.random() * 10}vw`);
      element.style.setProperty("--symbol-return", `${-5 + Math.random() * 10}vw`);
      element.style.setProperty("--symbol-drift", `${-18 + Math.random() * 36}vw`);
      element.style.setProperty("--symbol-color", colors[Math.floor(Math.random() * colors.length)]);
      fragment.append(element);
    }

    container.replaceChildren(fragment);
  }

  function handleResize() {
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(renderSymbols, 180);
  }

  renderSymbols();
  window.addEventListener("resize", handleResize, { passive: true });
  window.addEventListener("pagehide", () => {
    window.clearTimeout(resizeTimer);
    window.removeEventListener("resize", handleResize);
    container.replaceChildren();
  }, { once: true });
})();