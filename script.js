(() => {
  "use strict";

  const menuButton = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav-links");

  if (menuButton && nav) {
    menuButton.addEventListener("click", () => {
      const open = menuButton.getAttribute("aria-expanded") !== "true";
      menuButton.setAttribute("aria-expanded", String(open));
      menuButton.setAttribute("aria-label", open ? "Închide meniul" : "Deschide meniul");
      nav.classList.toggle("is-open", open);
    });

    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        menuButton.setAttribute("aria-expanded", "false");
        menuButton.setAttribute("aria-label", "Deschide meniul");
        nav.classList.remove("is-open");
      });
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        menuButton.setAttribute("aria-expanded", "false");
        menuButton.setAttribute("aria-label", "Deschide meniul");
        nav.classList.remove("is-open");
        menuButton.focus();
      }
    });
  }

  const heroVideo = document.querySelector(".hero-video");
  if (heroVideo) {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    const syncHeroVideo = () => {
      if (reduceMotion.matches) {
        heroVideo.pause();
      } else {
        heroVideo.play().catch(() => {});
      }
    };
    syncHeroVideo();
    reduceMotion.addEventListener("change", syncHeroVideo);
  }


  const motionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");

  if (!motionPreference.matches) {
    const loopReservations = [];
    document.querySelectorAll(".hero h1 em, .page-hero h1 em").forEach((target) => {
      const phrases = (target.dataset.loopPhrases || target.textContent.trim())
        .split("|")
        .map((phrase) => phrase.trim())
        .filter(Boolean);
      if (!phrases.length) return;

      const reservePhraseSpace = () => {
        const headline = target.closest("h1");
        if (!headline) return;
        const targetStyle = window.getComputedStyle(target);
        const fontSize = parseFloat(targetStyle.fontSize) || 16;
        const measure = document.createElement("span");
        Object.assign(measure.style, {
          position: "fixed",
          left: "-10000px",
          top: "0",
          display: "block",
          visibility: "hidden",
          pointerEvents: "none",
          width: Math.max(1, headline.clientWidth - fontSize * 0.8) + "px",
          whiteSpace: "normal",
          overflowWrap: "anywhere",
          wordBreak: "normal",
          fontFamily: targetStyle.fontFamily,
          fontSize: targetStyle.fontSize,
          fontWeight: targetStyle.fontWeight,
          fontStyle: targetStyle.fontStyle,
          lineHeight: targetStyle.lineHeight,
          letterSpacing: targetStyle.letterSpacing
        });
        document.body.append(measure);
        let maxHeight = 0;
        phrases.forEach((phrase) => {
          measure.textContent = phrase;
          maxHeight = Math.max(maxHeight, measure.getBoundingClientRect().height);
        });
        measure.remove();
        target.style.setProperty("--phrase-height", Math.ceil(maxHeight + 4) + "px");
      };
      reservePhraseSpace();
      loopReservations.push(reservePhraseSpace);

      const visualPhrase = document.createElement("span");
      visualPhrase.className = "typewriter-text";
      visualPhrase.setAttribute("aria-hidden", "true");

      const readablePhrase = document.createElement("span");
      readablePhrase.className = "motion-readable";
      readablePhrase.textContent = phrases[0];
      target.replaceChildren(visualPhrase, readablePhrase);

      let phraseIndex = 0;
      const writePhrase = () => {
        const phrase = phrases[phraseIndex];
        visualPhrase.replaceChildren();
        visualPhrase.classList.remove("is-changing");

        Array.from(phrase).forEach((character, index) => {
          if (character === " ") {
            visualPhrase.append(document.createTextNode(" "));
            return;
          }

          const glyph = document.createElement("span");
          glyph.className = "typed-char";
          glyph.style.setProperty("--type-delay", (index * 29) + "ms");
          glyph.textContent = character;
          visualPhrase.append(glyph);
        });

        const glyphCount = visualPhrase.querySelectorAll(".typed-char").length;
        window.setTimeout(() => {
          visualPhrase.classList.add("is-changing");
          window.setTimeout(() => {
            phraseIndex = (phraseIndex + 1) % phrases.length;
            writePhrase();
          }, 150);
        }, Math.max(2850, glyphCount * 29 + 1550));
      };

      writePhrase();
    });

    let phraseResizeTimer;
    window.addEventListener("resize", () => {
      window.clearTimeout(phraseResizeTimer);
      phraseResizeTimer = window.setTimeout(() => loopReservations.forEach((reserve) => reserve()), 100);
    }, { passive: true });

    const revealTargets = document.querySelectorAll([
      ".hero-copy", ".hero-visual", ".page-hero-copy", ".page-aside",
      ".journey-step", ".idea-choice-intro", ".idea-option", ".idea-result",
      ".price-strip-heading", ".rate-item", ".section-heading",
      ".service-card", ".application-item", ".feature-image", ".copy-block",
      ".quality-panel", ".process-card", ".detail-image", ".detail-copy",
      ".value-card", ".project-card", ".contact-panel", ".contact-form",
      ".contact-item", ".cta-band", ".footer-grid > div"
    ].join(", "));

    if ("IntersectionObserver" in window && revealTargets.length) {
      document.documentElement.classList.add("motion-ready");
      const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      }, { threshold: 0.14, rootMargin: "0px 0px -32px 0px" });

      revealTargets.forEach((target) => {
        const siblingIndex = target.parentElement
          ? Array.prototype.indexOf.call(target.parentElement.children, target)
          : 0;
        target.classList.add("motion-reveal");
        target.style.setProperty(
          "--reveal-delay",
          Math.min(siblingIndex, 4) * 68 + "ms"
        );
        revealObserver.observe(target);
      });
    }
  }

  const serviceShowcase = document.querySelector("[data-service-showcase]");
  if (serviceShowcase) {
    const services = {
      fdm: {
        image: "images/service-fdm.jpg",
        alt: "Printare 3D FDM în lucru",
        kicker: "PRINTARE 3D · FDM",
        title: "Piese practice, strat cu strat.",
        price: "De la 10 lei / oră",
        href: "printare-fdm.html",
        linkText: "Descoperă serviciul",
      },
      sla: {
        image: "images/service-sla.jpg",
        alt: "Echipament pentru imprimare 3D SLA",
        kicker: "PRINTARE 3D · SLA",
        title: "Detaliu fin, suprafețe curate.",
        price: "De la 20 lei / oră",
        href: "printare-sla.html",
        linkText: "Descoperă serviciul",
      },
      scan: {
        image: "images/service-scanning.jpg",
        alt: "Scanarea digitală a unui obiect",
        kicker: "CAPTURĂ DIGITALĂ · SCANARE",
        title: "Obiectul devine model digital.",
        price: "De la 300 lei / oră",
        href: "scanare-3d.html",
        linkText: "Descoperă scanarea",
      }
    };
    const image = serviceShowcase.querySelector("[data-showcase-image]");
    const alternateImage = image.cloneNode(false);
    alternateImage.removeAttribute("data-showcase-image");
    alternateImage.className = "showcase-image-layer";
    alternateImage.alt = "";
    alternateImage.setAttribute("aria-hidden", "true");
    serviceShowcase.insertBefore(alternateImage, serviceShowcase.querySelector(".showcase-copy"));
    const kicker = serviceShowcase.querySelector("[data-showcase-kicker]");
    const title = serviceShowcase.querySelector("[data-showcase-title]");
    const price = serviceShowcase.querySelector("[data-showcase-price]");
    const link = serviceShowcase.querySelector("[data-showcase-link]");
    const showcaseCopy = serviceShowcase.querySelector(".showcase-copy");
    let imageVersion = 0;
    let copySwapTimer = 0;
    let activeImageLayer = image;

    serviceShowcase.querySelectorAll("[data-showcase-option]").forEach((button) => {
      button.addEventListener("click", () => {
        const service = services[button.dataset.showcaseOption];
        if (!service || button.getAttribute("aria-pressed") === "true") return;

        window.clearTimeout(copySwapTimer);
        serviceShowcase.querySelectorAll("[data-showcase-option]").forEach((option) => {
          option.setAttribute("aria-pressed", String(option === button));
        });
        showcaseCopy.classList.add("is-switching");
        copySwapTimer = window.setTimeout(() => showcaseCopy.classList.remove("is-switching"), 180);
        kicker.textContent = service.kicker;
        title.textContent = service.title;
        price.textContent = service.price;
        link.href = service.href;
        const arrow = document.createElement("span");
        arrow.setAttribute("aria-hidden", "true");
        arrow.textContent = "↗";
        link.replaceChildren(document.createTextNode(service.linkText + " "), arrow);
        const version = ++imageVersion;
        const previousImage = activeImageLayer;
        const nextImage = activeImageLayer === image ? alternateImage : image;
        let prepared = false;
        const revealImage = async () => {
          if (prepared || version !== imageVersion || !nextImage.complete || !nextImage.naturalWidth) return;
          prepared = true;
          if (nextImage.decode) await nextImage.decode().catch(() => {});
          if (version !== imageVersion) return;
          nextImage.alt = service.alt;
          nextImage.removeAttribute("aria-hidden");
          previousImage.alt = "";
          previousImage.setAttribute("aria-hidden", "true");
          nextImage.classList.add("is-active");
          previousImage.classList.remove("is-active");
          activeImageLayer = nextImage;
        };
        nextImage.onload = revealImage;
        nextImage.onerror = () => { if (version === imageVersion) nextImage.removeAttribute("data-load-version"); };
        nextImage.dataset.loadVersion = String(version);
        nextImage.src = service.image;
        if (nextImage.complete && nextImage.naturalWidth) revealImage();
      });
    });
  }

  const scrollShade = document.createElement("div");
  scrollShade.className = "scroll-shade";
  scrollShade.setAttribute("aria-hidden", "true");
  document.body.append(scrollShade);
  let scrollShadeFrame = 0;
  const updateScrollShade = () => {
    if (scrollShadeFrame) return;
    scrollShadeFrame = window.requestAnimationFrame(() => {
      scrollShadeFrame = 0;
      const remaining = Math.max(0, document.documentElement.scrollHeight - window.scrollY - window.innerHeight);
      const approach = Math.max(0, Math.min(1, (1050 - remaining) / 780));
      const fadeAtBottom = Math.max(0, Math.min(1, remaining / 180));
      const easedApproach = approach * approach * (3 - 2 * approach);
      scrollShade.style.opacity = String(easedApproach * fadeAtBottom * 0.56);
    });
  };
  window.addEventListener("scroll", updateScrollShade, { passive: true });
  window.addEventListener("resize", updateScrollShade, { passive: true });
  updateScrollShade();

  const ideaPicker = document.querySelector(".idea-picker");
  if (ideaPicker) {
    const routes = {
      file: {
        title: "Ai deja modelul. Noi îl pregătim.",
        copy: "Verificăm fișierul și alegem tehnologia potrivită după scopul și finisajul dorit.",
        href: "servicii.html",
        link: "Compară tehnologiile",
        count: "01 / 03"
      },
      object: {
        title: "Pornim de la obiectul existent.",
        copy: "Scanarea 3D îi captează forma pentru replicare, modificare sau pentru un nou flux digital.",
        href: "scanare-3d.html",
        link: "Descoperă scanarea",
        count: "02 / 03"
      },
      idea: {
        title: "Începem cu o schiță sau o conversație.",
        copy: "Modelăm piesa potrivită scopului tău, de la primele proporții până la fișierul pregătit pentru producție.",
        href: "modelare-3d.html",
        link: "Descoperă modelarea",
        count: "03 / 03"
      }
    };
    const resultTitle = ideaPicker.querySelector("[data-idea-title]");
    const resultCopy = ideaPicker.querySelector("[data-idea-copy]");
    const resultLink = ideaPicker.querySelector("[data-idea-link]");
    const resultCount = ideaPicker.querySelector("[data-idea-count]");
    let routeUpdateVersion = 0;

    ideaPicker.querySelectorAll("[data-idea-choice]").forEach((button) => {
      button.addEventListener("click", () => {
        const route = routes[button.dataset.ideaChoice];
        if (!route) return;

        ideaPicker.querySelectorAll("[data-idea-choice]").forEach((option) => {
          option.setAttribute("aria-pressed", String(option === button));
        });
        const routeVersion = ++routeUpdateVersion;
        ideaPicker.classList.add("is-updating");
        window.setTimeout(() => {
          if (routeVersion !== routeUpdateVersion) return;
          resultTitle.textContent = route.title;
          resultCopy.textContent = route.copy;
          resultLink.href = route.href;
          const arrow = document.createElement("span");
          arrow.setAttribute("aria-hidden", "true");
          arrow.textContent = "↗";
          resultLink.replaceChildren(document.createTextNode(route.link + " "), arrow);
          resultCount.textContent = route.count;
          ideaPicker.classList.remove("is-updating");
        }, 120);
      });
    });
  }

  const year = document.querySelector("[data-year]");
  if (year) year.textContent = new Date().getFullYear();

  const form = document.querySelector("#contact-form");
  if (form) {
    const captchaPrompt = form.querySelector("[data-human-question]");
    const captchaInput = form.querySelector("[name='human_check']");
    const honeypot = form.querySelector("[name='company_website']");
    const formNote = form.querySelector(".form-note");
    const formOpenedAt = Date.now();
    const challengeLeft = Math.floor(Math.random() * 5) + 2;
    const challengeRight = Math.floor(Math.random() * 5) + 1;
    const challengeAnswer = String(challengeLeft + challengeRight);
    if (captchaPrompt) captchaPrompt.textContent = challengeLeft + " + " + challengeRight;
    if (captchaInput) captchaInput.addEventListener("input", () => captchaInput.setCustomValidity(""));

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;

      if ((honeypot && honeypot.value.trim()) || Date.now() - formOpenedAt < 1300) return;
      if (!captchaInput || captchaInput.value.trim() !== challengeAnswer) {
        if (captchaInput) {
          captchaInput.setCustomValidity("Răspunde corect la calculul de verificare.");
          captchaInput.reportValidity();
          captchaInput.focus();
        }
        if (formNote) formNote.textContent = "Verificarea anti-spam nu este corectă încă.";
        return;
      }

      const fields = new FormData(form);
      const subject = encodeURIComponent("Solicitare ofertă — CR Print 3D");
      const body = encodeURIComponent(
        "Nume: " + fields.get("name") + "\n" +
        "Email: " + fields.get("email") + "\n" +
        "Telefon: " + (fields.get("phone") || "—") + "\n" +
        "Serviciu: " + (fields.get("service") || "—") + "\n\n" +
        "Detalii proiect:\n" + fields.get("message")
      );
      window.location.href = "mailto:hi@crprint.ro?subject=" + subject + "&body=" + body;
      if (formNote) formNote.textContent = "Am pregătit mesajul în aplicația ta de e-mail.";
    });
  }

  const siteIntro = document.querySelector("[data-site-intro]");
  if (siteIntro && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    let alreadySeen = false;
    try {
      alreadySeen = window.sessionStorage.getItem("crprint-intro-seen") === "1";
      if (!alreadySeen) window.sessionStorage.setItem("crprint-intro-seen", "1");
    } catch (_) {
      // The intro still plays once on this page when storage is unavailable.
    }
    if (!alreadySeen) {
      siteIntro.hidden = false;
      siteIntro.removeAttribute("aria-hidden");
      let exitTimer;
      const finishIntro = () => {
        if (siteIntro.classList.contains("is-exiting")) return;
        window.clearTimeout(exitTimer);
        siteIntro.classList.add("is-exiting");
        window.setTimeout(() => siteIntro.remove(), 320);
      };
      const skipButton = siteIntro.querySelector("[data-intro-skip]");
      if (skipButton) skipButton.addEventListener("click", finishIntro, { once: true });
      document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") finishIntro();
      }, { once: true });
      exitTimer = window.setTimeout(finishIntro, 1460);
    }
  }
})();
