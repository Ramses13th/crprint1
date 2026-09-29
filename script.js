/**
 * CR Print 3D — Main Script
 * Handles: navbar, scroll animations, particles, counters, mobile menu, form, cookie consent
 */

(function () {
  'use strict';

  /* ───────── DOM Cache ───────── */
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

  const topBar       = $('#top-bar');
  const navbar       = $('#navbar');
  const menuToggle   = $('#menu-toggle');
  const navLinks     = $('#nav-links');
  const heroParticles = $('#hero-particles');
  const contactForm  = $('#contact-form');

  /* ───────── Top-bar hide on scroll ───────── */
  let lastScroll = 0;
  const TOPBAR_THRESHOLD = 80;

  function handleTopBar() {
    const y = window.scrollY;
    if (y > TOPBAR_THRESHOLD) {
      topBar?.classList.add('hidden');
    } else {
      topBar?.classList.remove('hidden');
    }
  }

  /* ───────── Navbar scroll effect ───────── */
  function handleNavbar() {
    if (window.scrollY > 60) {
      navbar?.classList.add('scrolled');
    } else {
      navbar?.classList.remove('scrolled');
    }
  }

  /* ───────── Mobile Menu ───────── */
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
      const isOpen = navLinks.classList.toggle('mobile-open');
      menuToggle.classList.toggle('active');
      menuToggle.setAttribute('aria-expanded', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    // Close mobile menu when clicking a link
    $$('a', navLinks).forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('mobile-open');
        menuToggle.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }

  /* ───────── Scroll Reveal Animation ───────── */
  function initScrollReveal() {
    const reveals = $$('.reveal');
    if (!reveals.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -60px 0px'
    });

    reveals.forEach(el => observer.observe(el));
  }

  /* ───────── Animated Counters ───────── */
  function animateCounter(el, target, suffix = '') {
    const duration = 2000;
    const start = 0;
    const startTime = performance.now();

    function update(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = Math.round(start + (target - start) * eased);
      el.textContent = value + suffix;

      if (progress < 1) {
        requestAnimationFrame(update);
      }
    }

    requestAnimationFrame(update);
  }

  function initCounters() {
    const counters = [
      { id: 'counter-projects', target: 500, suffix: '+' },
      { id: 'counter-clients', target: 200, suffix: '+' },
      { id: 'counter-tech', target: 5, suffix: '' }
    ];

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const data = counters.find(c => c.id === entry.target.id);
          if (data) animateCounter(entry.target, data.target, data.suffix);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    counters.forEach(({ id }) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });
  }

  /* ───────── Interactive 3D Lattice & Particle Canvas ───────── */
  function initHeroCanvas() {
    const canvas = document.getElementById('hero-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let width = 0;
    let height = 0;
    let animationId = null;
    let isVisible = true;

    // Mouse coordinates relative to canvas
    const mouse = { x: -1000, y: -1000, radius: 160 };

    window.addEventListener('mousemove', (e) => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
    }, { passive: true });

    window.addEventListener('mouseleave', () => {
      mouse.x = -1000;
      mouse.y = -1000;
    });

    function resize() {
      const hero = document.getElementById('hero');
      width = canvas.width = hero ? hero.offsetWidth : window.innerWidth;
      height = canvas.height = hero ? hero.offsetHeight : window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize, { passive: true });

    // Particle nodes
    const colors = [
      { r: 255, g: 107, b: 0 },   // #ff6b00 orange
      { r: 255, g: 179, b: 71 },  // #ffb347 amber
      { r: 255, g: 77,  b: 0 },   // #ff4d00 warm
      { r: 255, g: 140, b: 51 }   // #ff8c33 light orange
    ];

    const particleCount = window.innerWidth < 768 ? 30 : 60;
    const particles = [];

    for (let i = 0; i < particleCount; i++) {
      const color = colors[Math.floor(Math.random() * colors.length)];
      particles.push({
        x: Math.random() * (width || window.innerWidth),
        y: Math.random() * (height || window.innerHeight),
        vx: (Math.random() - 0.5) * 0.75,
        vy: (Math.random() - 0.5) * 0.75,
        radius: Math.random() * 2.2 + 1.2,
        baseRadius: Math.random() * 2.2 + 1.2,
        color: color,
        alpha: Math.random() * 0.45 + 0.35,
        pulseSpeed: Math.random() * 0.02 + 0.01,
        pulseAngle: Math.random() * Math.PI * 2
      });
    }

    function draw() {
      if (!isVisible) return;

      ctx.clearRect(0, 0, width, height);

      // Connect particles with glowing orange filaments
      const maxDist = window.innerWidth < 768 ? 95 : 135;
      const maxDistSq = maxDist * maxDist;

      for (let i = 0; i < particles.length; i++) {
        const p1 = particles[i];

        // Update position
        p1.x += p1.vx;
        p1.y += p1.vy;

        // Bounce off walls
        if (p1.x < 0) { p1.x = 0; p1.vx *= -1; }
        else if (p1.x > width) { p1.x = width; p1.vx *= -1; }
        if (p1.y < 0) { p1.y = 0; p1.vy *= -1; }
        else if (p1.y > height) { p1.y = height; p1.vy *= -1; }

        // Pulse radius
        p1.pulseAngle += p1.pulseSpeed;
        p1.radius = p1.baseRadius + Math.sin(p1.pulseAngle) * 0.5;

        // Mouse repulsion
        const dxMouse = mouse.x - p1.x;
        const dyMouse = mouse.y - p1.y;
        const distMouse = Math.sqrt(dxMouse * dxMouse + dyMouse * dyMouse);
        if (distMouse < mouse.radius && distMouse > 0) {
          const force = (mouse.radius - distMouse) / mouse.radius;
          p1.x -= (dxMouse / distMouse) * force * 2.5;
          p1.y -= (dyMouse / distMouse) * force * 2.5;
        }

        // Connect with nearby particles
        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dx = p1.x - p2.x;
          const dy = p1.y - p2.y;
          const distSq = dx * dx + dy * dy;

          if (distSq < maxDistSq) {
            const dist = Math.sqrt(distSq);
            const lineAlpha = (1 - dist / maxDist) * 0.35;
            ctx.strokeStyle = `rgba(${p1.color.r}, ${p1.color.g}, ${p1.color.b}, ${lineAlpha})`;
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
          }
        }

        // Draw particle node with subtle glow
        ctx.fillStyle = `rgba(${p1.color.r}, ${p1.color.g}, ${p1.color.b}, ${p1.alpha})`;
        ctx.shadowBlur = 8;
        ctx.shadowColor = `rgba(${p1.color.r}, ${p1.color.g}, ${p1.color.b}, 0.7)`;
        ctx.beginPath();
        ctx.arc(p1.x, p1.y, p1.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0; // reset
      }

      animationId = requestAnimationFrame(draw);
    }

    // Observer to pause when hero not in viewport
    const heroSection = document.getElementById('hero');
    if (heroSection && 'IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          isVisible = entry.isIntersecting;
          if (isVisible && !animationId) {
            draw();
          } else if (!isVisible && animationId) {
            cancelAnimationFrame(animationId);
            animationId = null;
          }
        });
      }, { threshold: 0.1 });
      observer.observe(heroSection);
    } else {
      draw();
    }
  }

  /* ───────── Hero Video & Toggle Control ───────── */
  function initHeroVideo() {
    const video = document.getElementById('hero-bg-video');
    const toggleBtn = document.getElementById('video-toggle-btn');
    if (!video || !toggleBtn) return;

    const pauseIcon = toggleBtn.querySelector('.icon-pause');
    const playIcon  = toggleBtn.querySelector('.icon-play');
    const textSpan  = toggleBtn.querySelector('.vt-text');

    function updateBtnState(isPlaying) {
      if (isPlaying) {
        video.classList.remove('paused');
        toggleBtn.classList.remove('is-paused');
        if (pauseIcon) pauseIcon.style.display = 'block';
        if (playIcon) playIcon.style.display = 'none';
        if (textSpan) textSpan.textContent = 'Video Activ';
      } else {
        video.classList.add('paused');
        toggleBtn.classList.add('is-paused');
        if (pauseIcon) pauseIcon.style.display = 'none';
        if (playIcon) playIcon.style.display = 'block';
        if (textSpan) textSpan.textContent = 'Video Oprit';
      }
    }

    toggleBtn.addEventListener('click', () => {
      if (video.paused) {
        video.play().then(() => updateBtnState(true)).catch(() => {});
      } else {
        video.pause();
        updateBtnState(false);
      }
    });

    // Pause video when out of viewport to preserve resources
    const heroSection = document.getElementById('hero');
    if (heroSection && 'IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) {
            if (!video.paused) video.pause();
          } else {
            if (!toggleBtn.classList.contains('is-paused')) {
              video.play().catch(() => {});
            }
          }
        });
      }, { threshold: 0.1 });
      observer.observe(heroSection);
    }
  }

  /* ───────── Smooth Scroll for anchor links ───────── */
  function initSmoothScroll() {
    $$('a[href^="#"]').forEach(link => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        if (href === '#') return;

        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          const offset = 80;
          const top = target.getBoundingClientRect().top + window.scrollY - offset;
          window.scrollTo({ top, behavior: 'smooth' });
        }
      });
    });
  }

  /* ───────── Active Nav Link based on scroll ───────── */
  function initActiveNav() {
    const sections = $$('section[id]');
    const links = $$('.nav-links > a, .nav-links .dropdown-toggle');

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          links.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href');
            if (href === `#${id}`) {
              link.classList.add('active');
            }
          });
        }
      });
    }, {
      threshold: 0.2,
      rootMargin: '-80px 0px -50% 0px'
    });

    sections.forEach(section => observer.observe(section));
  }

  /* ───────── Contact Form Handler ───────── */
  function initContactForm() {
    if (!contactForm) return;

    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const btn = contactForm.querySelector('.btn-primary');
      const originalText = btn.innerHTML;

      // Get form fields
      const name = contactForm.querySelector('#name');
      const email = contactForm.querySelector('#email');
      const phone = contactForm.querySelector('#phone');
      const service = contactForm.querySelector('#service');
      const message = contactForm.querySelector('#message');

      // Clear previous error states
      [name, email, message].forEach(field => {
        field.style.borderColor = '';
      });

      // Remove any previous status messages
      const oldStatus = contactForm.querySelector('.form-status');
      if (oldStatus) oldStatus.remove();

      // Validate required fields
      let hasError = false;
      if (!name.value.trim()) {
        name.style.borderColor = '#ef4444';
        hasError = true;
      }
      if (!email.value.trim() || !isValidEmail(email.value)) {
        email.style.borderColor = '#ef4444';
        hasError = true;
      }
      if (!message.value.trim()) {
        message.style.borderColor = '#ef4444';
        hasError = true;
      }

      if (hasError) {
        const errorMsg = document.createElement('div');
        errorMsg.className = 'form-status error';
        errorMsg.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z"/>
          </svg>
          Te rugăm să completezi toate câmpurile obligatorii.
        `;
        contactForm.querySelector('.form-submit').appendChild(errorMsg);
        setTimeout(() => {
          [name, email, message].forEach(field => { field.style.borderColor = ''; });
          errorMsg.remove();
        }, 3000);
        return;
      }

      // Show loading state
      btn.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="animation: spin 1s linear infinite">
          <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182"/>
        </svg>
        Se trimite...
      `;
      btn.disabled = true;

      // Simulate email sending (replace with EmailJS or backend when ready)
      setTimeout(() => {
        btn.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
          </svg>
          Mesaj trimis cu succes!
        `;
        btn.style.background = '#10b981';

        // Add success message
        const successMsg = document.createElement('div');
        successMsg.className = 'form-status success';
        successMsg.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
          </svg>
          Mulțumim! Mesajul tău a fost trimis. Te vom contacta în cel mai scurt timp.
        `;
        contactForm.querySelector('.form-submit').appendChild(successMsg);

        setTimeout(() => {
          btn.innerHTML = originalText;
          btn.style.background = '';
          btn.disabled = false;
          contactForm.reset();
          successMsg.remove();
        }, 4000);
      }, 1500);
    });
  }

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  /* ───────── Ticker Pause on Hover ───────── */
  function initTicker() {
    const ticker = $('#ticker-track');
    if (!ticker) return;

    ticker.addEventListener('mouseenter', () => {
      ticker.style.animationPlayState = 'paused';
    });
    ticker.addEventListener('mouseleave', () => {
      ticker.style.animationPlayState = 'running';
    });
  }

  /* ───────── Navbar Link Styling for Dropdown ───────── */
  function initDropdownMobile() {
    // On mobile, clicking dropdown toggles its menu
    const dropdowns = $$('.nav-dropdown');
    dropdowns.forEach(dd => {
      const toggle = dd.querySelector('.dropdown-toggle');
      toggle?.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
          e.preventDefault();
          dd.classList.toggle('open');
        }
      });
    });
  }

  /* ───────── Typing effect for hero (subtle) ───────── */
  function initTypingCursor() {
    const title = $('.hero-title .gradient-text');
    if (!title) return;

    // Add blinking cursor briefly
    title.style.borderRight = '2px solid var(--clr-accent)';
    title.style.paddingRight = '4px';
    title.style.animation = 'none';

    setTimeout(() => {
      title.style.borderRight = '';
      title.style.paddingRight = '';
    }, 3000);
  }

  /* ───────── CSS Animation helper (added to <style>) ───────── */
  function addDynamicStyles() {
    const style = document.createElement('style');
    style.textContent = `
      @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
      
      /* Parallax-like subtle background movement */
      .hero-bg img {
        will-change: transform;
      }
    `;
    document.head.appendChild(style);
  }

  /* ───────── Subtle parallax on hero image ───────── */
  function initParallax() {
    const heroImg = $('.hero-bg img');
    if (!heroImg) return;

    let ticking = false;

    function updateParallax() {
      const scroll = window.scrollY;
      if (scroll < window.innerHeight) {
        heroImg.style.transform = `translateY(${scroll * 0.3}px) scale(1.1)`;
      }
      ticking = false;
    }

    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(updateParallax);
        ticking = true;
      }
    }, { passive: true });

    // Set initial scale
    heroImg.style.transform = 'scale(1.1)';
  }

  /* ───────── Magnetic effect on CTA buttons ───────── */
  function initMagneticButtons() {
    $$('.btn-primary').forEach(btn => {
      btn.addEventListener('mousemove', (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        btn.style.transform = `translateY(-2px) translate(${x * 0.1}px, ${y * 0.1}px)`;
      });

      btn.addEventListener('mouseleave', () => {
        btn.style.transform = '';
      });
    });
  }

  /* ───────── Cookie Consent Banner ───────── */
  function initCookieConsent() {
    const banner = $('#cookie-banner');
    const acceptBtn = $('#cookie-accept');
    const declineBtn = $('#cookie-decline');

    if (!banner) return;

    // Check if user already made a choice
    const consent = localStorage.getItem('crprint-cookie-consent');
    if (consent) return; // Already accepted/declined

    // Show banner after 1.5s delay
    setTimeout(() => {
      banner.classList.add('visible');
    }, 1500);

    acceptBtn?.addEventListener('click', () => {
      localStorage.setItem('crprint-cookie-consent', 'accepted');
      banner.classList.remove('visible');
    });

    declineBtn?.addEventListener('click', () => {
      localStorage.setItem('crprint-cookie-consent', 'declined');
      banner.classList.remove('visible');
    });
  }

  /* ───────── Custom Interactive Neon Cursor ───────── */
  function initCustomCursor() {
    const dot = document.getElementById('cursor-dot');
    const ring = document.getElementById('cursor-ring');
    const glow = document.getElementById('cursor-glow');

    if (!dot || !ring || window.matchMedia('(pointer: coarse)').matches) {
      return;
    }

    let mouseX = -100, mouseY = -100;
    let ringX = -100, ringY = -100;
    let glowX = -100, glowY = -100;
    let isVisible = false;

    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      if (!isVisible) {
        isVisible = true;
        dot.style.opacity = '1';
        ring.style.opacity = '1';
        if (glow) glow.style.opacity = '0.85';
      }
      dot.style.transform = `translate(${mouseX}px, ${mouseY}px) translate(-50%, -50%)`;
    }, { passive: true });

    document.addEventListener('mouseleave', () => {
      isVisible = false;
      dot.style.opacity = '0';
      ring.style.opacity = '0';
      if (glow) glow.style.opacity = '0';
    });

    document.addEventListener('mousedown', () => {
      ring.classList.add('cursor-click');
    });

    document.addEventListener('mouseup', () => {
      ring.classList.remove('cursor-click');
    });

    // Smooth trailing physics for ring and glow
    function renderCursor() {
      if (isVisible) {
        ringX += (mouseX - ringX) * 0.22;
        ringY += (mouseY - ringY) * 0.22;
        ring.style.transform = `translate(${ringX}px, ${ringY}px) translate(-50%, -50%)`;

        if (glow) {
          glowX += (mouseX - glowX) * 0.12;
          glowY += (mouseY - glowY) * 0.12;
          glow.style.transform = `translate(${glowX}px, ${glowY}px) translate(-50%, -50%)`;
        }
      }
      requestAnimationFrame(renderCursor);
    }
    requestAnimationFrame(renderCursor);

    // Hover detection on interactive elements
    const hoverSelectors = 'a, button, input, select, textarea, .service-card, .offer-card, .step-card, .contact-card, .btn-primary, .btn-secondary, .social-links a, .menu-toggle';
    
    document.addEventListener('mouseover', (e) => {
      if (e.target.closest(hoverSelectors)) {
        ring.classList.add('cursor-hover');
        dot.classList.add('cursor-hover');
      }
    });

    document.addEventListener('mouseout', (e) => {
      if (e.target.closest(hoverSelectors)) {
        ring.classList.remove('cursor-hover');
        dot.classList.remove('cursor-hover');
      }
    });
  }

  /* ───────── Site-wide Background Ambient Canvas ───────── */
  function initSiteAmbientCanvas() {
    const canvas = document.getElementById('ambient-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let width = 0;
    let height = 0;

    function resize() {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize, { passive: true });

    // Embers and floating neon cyber particles
    const particleCount = window.innerWidth < 768 ? 22 : 45;
    const embers = [];

    const emberColors = [
      { r: 255, g: 107, b: 0 },   // #ff6b00
      { r: 255, g: 179, b: 71 },  // #ffb347
      { r: 255, g: 140, b: 51 },  // #ff8c33
      { r: 255, g: 77,  b: 0 }    // #ff4d00
    ];

    for (let i = 0; i < particleCount; i++) {
      embers.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.35,
        vy: -(Math.random() * 0.5 + 0.15), // gentle upward float
        radius: Math.random() * 1.8 + 0.8,
        baseAlpha: Math.random() * 0.35 + 0.15,
        color: emberColors[Math.floor(Math.random() * emberColors.length)],
        angle: Math.random() * Math.PI * 2,
        wobbleSpeed: Math.random() * 0.02 + 0.008
      });
    }

    let lastScrollY = window.scrollY;
    let scrollDelta = 0;

    window.addEventListener('scroll', () => {
      scrollDelta = (window.scrollY - lastScrollY) * 0.04;
      lastScrollY = window.scrollY;
    }, { passive: true });

    function drawAmbient() {
      ctx.clearRect(0, 0, width, height);

      // Dampen scrollDelta
      scrollDelta *= 0.92;

      for (let i = 0; i < embers.length; i++) {
        const p = embers[i];
        p.angle += p.wobbleSpeed;
        p.x += p.vx + Math.sin(p.angle) * 0.3;
        p.y += p.vy - scrollDelta;

        // Wrap around viewport edges
        if (p.y < -10) p.y = height + 10;
        else if (p.y > height + 10) p.y = -10;
        if (p.x < -10) p.x = width + 10;
        else if (p.x > width + 10) p.x = -10;

        // Pulsing alpha
        const currentAlpha = p.baseAlpha + Math.sin(p.angle * 2) * 0.1;

        ctx.fillStyle = `rgba(${p.color.r}, ${p.color.g}, ${p.color.b}, ${Math.max(0, currentAlpha)})`;
        ctx.shadowBlur = 10;
        ctx.shadowColor = `rgba(${p.color.r}, ${p.color.g}, ${p.color.b}, 0.8)`;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      requestAnimationFrame(drawAmbient);
    }

    requestAnimationFrame(drawAmbient);
  }

  /* ───────── Init Everything ───────── */
  function init() {
    addDynamicStyles();
    initCustomCursor();
    initSiteAmbientCanvas();
    initHeroCanvas();
    initHeroVideo();
    initScrollReveal();
    initCounters();
    initSmoothScroll();
    initActiveNav();
    initContactForm();
    initTicker();
    initDropdownMobile();
    initTypingCursor();
    initParallax();
    initMagneticButtons();
    initCookieConsent();

    // Scroll handlers (throttled via rAF)
    let scrollTick = false;
    window.addEventListener('scroll', () => {
      if (!scrollTick) {
        requestAnimationFrame(() => {
          handleTopBar();
          handleNavbar();
          scrollTick = false;
        });
        scrollTick = true;
      }
    }, { passive: true });

    // Initial state
    handleTopBar();
    handleNavbar();
  }

  // Start when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
