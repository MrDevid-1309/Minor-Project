(() => {
  const button = document.getElementById("start-assessment");
  if (!button) return;

  let animationRunning = false;

  button.addEventListener("click", (event) => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const destination = button.href;
    const hero = button.closest(".hero");
    if (!hero || !destination) return;

    event.preventDefault();
    if (animationRunning) return;

    const buttonRect = button.getBoundingClientRect();
    const heroRect = hero.getBoundingClientRect();
    const startX = buttonRect.left + buttonRect.width / 2;
    const startY = buttonRect.top + buttonRect.height / 2;
    const carWidth = 76;
    const rightEdge = Math.min(heroRect.right, window.innerWidth);
    const travelDistance = Math.max(0, rightEdge - startX - carWidth / 2 - 12);

    animationRunning = true;
    button.classList.add("is-launching");
    button.setAttribute("aria-disabled", "true");

    const car = document.createElement("div");
    car.className = "assessment-car is-moving";
    car.setAttribute("aria-hidden", "true");
    car.style.transform = "translate(-50%, -50%) translateX(0px)";

    for (let particle = 0; particle < 2; particle += 1) {
      const dust = document.createElement("span");
      dust.className = "car-dust";
      dust.setAttribute("aria-hidden", "true");
      car.append(dust);
    }

    const image = document.createElement("img");
    image.src = button.dataset.carImage;
    image.alt = "";
    car.append(image);
    car.style.left = `${startX}px`;
    car.style.top = `${startY}px`;
    document.body.append(car);

    let finished = false;
    let fallbackTimeout;
    const finishAnimation = () => {
      if (finished) return;
      finished = true;
      window.clearTimeout(fallbackTimeout);
      car.remove();
      button.classList.remove("is-launching");
      button.removeAttribute("aria-disabled");
      animationRunning = false;
      window.location.assign(destination);
    };

    car.addEventListener("transitionend", (transitionEvent) => {
      if (transitionEvent.propertyName === "transform") finishAnimation();
    }, { once: true });
    fallbackTimeout = window.setTimeout(finishAnimation, 2300);

    car.getBoundingClientRect();
    requestAnimationFrame(() => {
      car.style.transform = `translate(-50%, -50%) translateX(${travelDistance}px)`;
    });
  });
})();
