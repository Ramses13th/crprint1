(() => {
  'use strict';
  const q = selector => document.querySelector(selector);
  const qa = selector => [...document.querySelectorAll(selector)];
  const root = document.documentElement;
  const status = q('#guide-status');
  const storage = {
    get(key, fallback) { try { return localStorage.getItem(key) ?? fallback; } catch { return fallback; } },
    set(key, value) { try { localStorage.setItem(key, value); } catch {} }
  };

  // Chapter progress stays local. Accept only valid keys and a valid JSON array.
  const chapterLinks = qa('.sidebar nav a');
  const chapterKeys = chapterLinks.map(link => link.getAttribute('href').replace('.html', ''));
  let complete = [];
  try {
    const saved = JSON.parse(storage.get('crprint-guide-progress', '[]'));
    if (Array.isArray(saved)) complete = [...new Set(saved)].filter(key => chapterKeys.includes(key));
  } catch {}
  const completeButton = q('[data-complete]');
  function progress() {
    q('[data-progress]').textContent = `${complete.length}/${chapterKeys.length} capitole parcurse`;
    q('progress').value = complete.length;
    const read = complete.includes(completeButton.dataset.complete);
    completeButton.textContent = read ? 'Capitol parcurs ✓ · Anulează marcarea' : 'Marchează capitolul ca parcurs ✓';
    completeButton.setAttribute('aria-pressed', String(read));
    chapterLinks.forEach((link, index) => {
      const done = complete.includes(chapterKeys[index]);
      link.querySelector('.nav-check').textContent = done ? '✓' : '';
      link.setAttribute('aria-label', `Capitolul ${index + 1}: ${link.querySelector('strong').textContent}${done ? ', parcurs' : ''}`);
    });
  }
  progress();
  completeButton.addEventListener('click', () => {
    const key = completeButton.dataset.complete;
    complete = complete.includes(key) ? complete.filter(value => value !== key) : [...complete, key];
    storage.set('crprint-guide-progress', JSON.stringify(complete));
    progress();
    status.textContent = completeButton.getAttribute('aria-pressed') === 'true' ? 'Capitol marcat ca parcurs.' : 'Marcarea capitolului a fost anulată.';
  });

  const themeButton = q('.theme-button');
  function themeLabel() {
    const dark = root.dataset.theme === 'dark';
    themeButton.setAttribute('aria-label', dark ? 'Activează tema luminoasă' : 'Activează tema întunecată');
    themeButton.setAttribute('aria-pressed', String(dark));
    themeButton.textContent = dark ? '☼' : '◐';
  }
  themeLabel();
  themeButton.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    storage.set('crprint-guide-theme', root.dataset.theme);
    themeLabel();
  });

  // On narrow screens the chapter list becomes an opaque, keyboard-accessible drawer.
  const sidebar = q('.sidebar');
  const toggle = q('.nav-toggle');
  const close = q('.nav-close');
  const backdrop = q('.nav-backdrop');
  const narrow = matchMedia('(max-width: 800px)');
  function menu(open, restoreFocus = true) {
    const active = open && narrow.matches;
    root.classList.toggle('nav-open', active);
    toggle.setAttribute('aria-expanded', String(active));
    backdrop.hidden = !active;
    q('main').inert = active;
    q('.guide-header').inert = active;
    if (active) {
      sidebar.setAttribute('role', 'dialog');
      sidebar.setAttribute('aria-modal', 'true');
      close.focus();
    } else {
      sidebar.removeAttribute('role');
      sidebar.removeAttribute('aria-modal');
      if (restoreFocus && narrow.matches) toggle.focus();
    }
  }
  toggle.addEventListener('click', () => menu(!root.classList.contains('nav-open')));
  close.addEventListener('click', () => menu(false));
  backdrop.addEventListener('click', () => menu(false));
  narrow.addEventListener('change', () => menu(false, false));
  sidebar.addEventListener('click', event => {
    if (event.target.closest('a') && root.classList.contains('nav-open')) menu(false, false);
  });
  document.addEventListener('keydown', event => {
    if (!root.classList.contains('nav-open')) return;
    if (event.key === 'Escape') { event.preventDefault(); menu(false); }
    if (event.key === 'Tab') {
      const focusable = [...sidebar.querySelectorAll('button,a,input')].filter(element => element.getClientRects().length);
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
  });
  root.classList.add('guide-ready');

  // Search deep-links to the matching section. No third-party search or tracking.
  const search = q('#guide-search');
  const results = q('.search-results');
  let index = [], loadError = false;
  const normalize = value => value.toLocaleLowerCase('ro').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  function searchResult() {
    const query = normalize(search.value.trim());
    results.replaceChildren();
    results.hidden = query.length < 2;
    if (results.hidden) return;
    if (loadError) { results.textContent = 'Căutarea nu este disponibilă. Folosește lista capitolelor.'; return; }
    if (!index.length) { results.textContent = 'Se încarcă indexul…'; return; }
    const terms = query.split(/\s+/);
    const found = index.filter(page => terms.every(term => normalize(page.title + ' ' + page.chapter + ' ' + page.text).includes(term)))
      .sort((a, b) => Number(normalize(b.title).includes(query)) - Number(normalize(a.title).includes(query))).slice(0, 8);
    if (!found.length) { results.textContent = 'Nu am găsit o secțiune. Încearcă „SMTP”, „stoc” sau „factură”.'; return; }
    for (const page of found) {
      const link = document.createElement('a'); link.href = page.url;
      const chapter = document.createElement('small'); chapter.textContent = page.chapter;
      const title = document.createElement('strong'); title.textContent = page.title;
      link.append(chapter, title); results.append(link);
    }
  }
  fetch('search-index.json').then(response => { if (!response.ok) throw new Error('index'); return response.json(); })
    .then(data => { index = Array.isArray(data) ? data : []; searchResult(); }).catch(() => { loadError = true; searchResult(); });
  search.addEventListener('input', searchResult);
  // A modifier shortcut avoids hijacking a single character for assistive technology.
  document.addEventListener('keydown', event => {
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
      event.preventDefault(); if (narrow.matches) menu(true); search.focus();
    }
  });

  const sections = qa('.section-panel');
  const fold = q('[data-fold]');
  function foldLabel() { fold.textContent = sections.some(panel => panel.open) ? 'Restrânge secțiunile' : 'Deschide secțiunile'; }
  fold.addEventListener('click', () => {
    const open = !sections.some(panel => panel.open);
    sections.forEach(panel => panel.open = open);
    foldLabel();
  });
  sections.forEach(panel => panel.addEventListener('toggle', foldLabel));
  function revealHash() {
    let id; try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    if (!id) return;
    const target = document.getElementById(id);
    if (!target) return;
    const panel = target.matches('details') ? target : target.querySelector('.section-panel');
    if (panel) panel.open = true;
    const parent = target.closest('details'); if (parent) parent.open = true;
  }
  window.addEventListener('hashchange', revealHash);
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (!link) return;
    const target = document.getElementById(link.getAttribute('href').slice(1));
    const panel = target?.querySelector('.section-panel'); if (panel) panel.open = true;
    if (target?.matches('details')) target.open = true;
  });
  revealHash();

  qa('pre').forEach(pre => {
    const button = document.createElement('button'); button.type = 'button'; button.className = 'copy-button'; button.textContent = 'Copiază';
    button.setAttribute('aria-label', 'Copiază textul acestui exemplu');
    button.addEventListener('click', async () => {
      const text = pre.querySelector('code')?.textContent || [...pre.childNodes].filter(node => node !== button).map(node => node.textContent).join('');
      try { await navigator.clipboard.writeText(text); button.textContent = 'Copiat ✓'; status.textContent = 'Text copiat în clipboard.'; }
      catch { button.textContent = 'Selectează textul'; status.textContent = 'Copierea automată nu este disponibilă. Selectează textul și folosește Ctrl+C.'; }
      setTimeout(() => button.textContent = 'Copiază', 2200);
    });
    pre.prepend(button);
  });
  let printState = [];
  window.addEventListener('beforeprint', () => {
    printState = qa('main details').map(panel => [panel, panel.open]);
    printState.forEach(([panel]) => panel.open = true);
  });
  window.addEventListener('afterprint', () => { printState.forEach(([panel, open]) => panel.open = open); printState = []; });
  q('[data-print]').addEventListener('click', () => window.print());

  qa('[data-launch-check]').forEach(input => {
    const key = 'crprint-launch-' + input.dataset.launchCheck;
    input.checked = storage.get(key, '0') === '1';
    input.addEventListener('change', () => storage.set(key, input.checked ? '1' : '0'));
  });
  let scrollQueued = false;
  function readingProgress() {
    scrollQueued = false;
    const height = document.documentElement.scrollHeight - window.innerHeight;
    q('.reading-line span').style.width = `${height > 0 ? Math.min(100, Math.max(0, window.scrollY / height * 100)) : 100}%`;
  }
  window.addEventListener('scroll', () => { if (!scrollQueued) { scrollQueued = true; requestAnimationFrame(readingProgress); } }, { passive: true });
  window.addEventListener('resize', readingProgress);
  new ResizeObserver(readingProgress).observe(q('main'));
  readingProgress();

  const calculator = q('#budget-calculator');
  if (calculator) {
    const f = name => Number(calculator.elements[name].value) || 0;
    const money = value => new Intl.NumberFormat('ro-RO', { maximumFractionDigits: 2 }).format(value);
    function update() {
      const monthly = Math.max(0, f('budget')), revenue = Math.max(0, f('revenue')), cost = Math.max(0, f('cost')), profit = Math.max(0, f('profit'));
      const rate = Math.min(100, Math.max(0, f('close'))) / 100;
      const contribution = revenue - cost, cpa = contribution - profit, cpl = cpa * rate;
      q('#calculator-result').innerHTML = `Medie zilnică Google orientativă: <strong>${money(monthly / 30.4)} lei</strong><br>Marjă înainte de reclame: <strong>${money(contribution)} lei</strong><br>CPA maxim pentru profitul dorit: <strong>${money(Math.max(0, cpa))} lei</strong><br>CPL calificat orientativ: <strong>${money(Math.max(0, cpl))} lei</strong><br>${cpa <= 0 ? 'Scenariul nu lasă buget pentru reclamă după profitul dorit. Ajustează prețul sau costul.' : 'Praguri economice, fără promisiune de rezultate.'}`;
    }
    calculator.addEventListener('input', update); update();
  }
})();
