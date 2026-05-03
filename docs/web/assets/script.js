// CINA Web Demo — minimal vanilla JS
// Loads data.json, animates counters, smooth-scroll, theme toggle (future).

(async function() {
  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const id = a.getAttribute('href');
      if (id === '#') return;
      const el = document.querySelector(id);
      if (el) {
        e.preventDefault();
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Animate counters in hero
  const targets = {
    'stat-rubric': { end: 4.76, decimals: 2 },
    'stat-stances': { end: 98, decimals: 0 },
    'stat-findings': { end: 8, decimals: 0 },
  };

  const animateCounter = (id, end, decimals) => {
    const el = document.getElementById(id);
    if (!el) return;
    const duration = 1200;
    const start = performance.now();
    const tick = (t) => {
      const p = Math.min((t - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = (end * eased).toFixed(decimals);
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };

  // Trigger when hero in view
  const hero = document.querySelector('.hero');
  if (hero) {
    const io = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        Object.entries(targets).forEach(([id, { end, decimals }]) => {
          animateCounter(id, end, decimals);
        });
        io.disconnect();
      }
    }, { threshold: 0.3 });
    io.observe(hero);
  }

  // Section scroll-fade
  const sections = document.querySelectorAll('.section');
  const sio = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.opacity = 1;
        e.target.style.transform = 'translateY(0)';
      }
    });
  }, { threshold: 0.1 });
  sections.forEach(s => {
    s.style.opacity = 0;
    s.style.transform = 'translateY(20px)';
    s.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    sio.observe(s);
  });

  // Load data.json (for future interactive expansion)
  try {
    const res = await fetch('assets/data.json');
    const data = await res.json();
    window.CINA_DATA = data;  // expose for console exploration
    console.log('CINA data loaded:', {
      countries: Object.keys(data.stage1_country_issue_matrix || {}).length,
      stances: data.stage1_total_stances,
      leiden_communities: Object.keys(data.stage2_leiden_communities || {}).length,
    });
  } catch (e) {
    console.warn('data.json fetch failed (likely served offline):', e);
  }

  // Active section highlight in nav (optional)
  const navLinks = document.querySelectorAll('.nav-main a[href^="#"]');
  const sectionsToWatch = Array.from(navLinks).map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  if (sectionsToWatch.length) {
    const activeIO = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          navLinks.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + e.target.id));
        }
      });
    }, { rootMargin: '-50% 0px -50% 0px' });
    sectionsToWatch.forEach(s => activeIO.observe(s));
  }

  console.log('CINA Web Demo loaded — github.com/zxsa0716/cina');
})();
