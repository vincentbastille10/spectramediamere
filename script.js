/* script.js — Spectra Media AI */

// ============================================================
// NAV: scroll effect + mobile hamburger
// ============================================================
const nav = document.getElementById('nav');
const hamburger = document.getElementById('navHamburger');
const navMobile = document.getElementById('navMobile');

window.addEventListener('scroll', () => {
  if (window.scrollY > 60) {
    nav.classList.add('scrolled');
  } else {
    nav.classList.remove('scrolled');
  }
});

hamburger.addEventListener('click', () => {
  navMobile.classList.toggle('open');
});

// Close mobile menu on link click
navMobile.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => navMobile.classList.remove('open'));
});

// ============================================================
// SCROLL REVEAL
// ============================================================
const revealElements = document.querySelectorAll(
  '.studio-card, .betty-card, .industry-card, .approach-card, .why-item, .demo-feat, .contact-item, .section-header, .how-it-works, .why-card-main, .contact-form, .contact-info, .graal-copy, .graal-visual, .faq-item, .about-photo, .about-copy'
);

revealElements.forEach(el => el.classList.add('reveal'));

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const delay = entry.target.getAttribute('data-delay') || 0;
      setTimeout(() => entry.target.classList.add('visible'), parseInt(delay));
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

revealElements.forEach(el => revealObserver.observe(el));

// ============================================================
// DEMO LAUNCH
// ============================================================
function launchDemo() {
  const overlay = document.getElementById('demoOverlay');
  const iframe = document.getElementById('bettyIframe');

  overlay.style.opacity = '0';
  overlay.style.transition = 'opacity 0.4s ease';

  setTimeout(() => {
    overlay.style.display = 'none';
    iframe.style.display = 'block';
  }, 400);
}

// ============================================================
// CONTACT FORM SUBMISSION
// ============================================================
async function handleSubmit(e) {
  e.preventDefault();

  const form = document.getElementById('contactForm');
  const submitBtn = document.getElementById('submitBtn');
  const btnText = submitBtn.querySelector('.btn-submit-text');
  const btnLoading = submitBtn.querySelector('.btn-submit-loading');
  const successEl = document.getElementById('formSuccess');
  const errorEl = document.getElementById('formError');

  // Reset
  successEl.style.display = 'none';
  errorEl.style.display = 'none';

  // Loading state
  submitBtn.disabled = true;
  btnText.style.display = 'none';
  btnLoading.style.display = 'inline';

  const data = {
    name: form.name.value.trim(),
    company: form.company.value.trim(),
    email: form.email.value.trim(),
    project_type: form.project_type.value,
    message: form.message.value.trim(),
  };

  try {
    const response = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (response.ok && result.success) {
      successEl.style.display = 'block';
      form.reset();
    } else {
      throw new Error(result.error || 'Send failed');
    }
  } catch (err) {
    console.error(err);
    errorEl.style.display = 'block';
  } finally {
    submitBtn.disabled = false;
    btnText.style.display = 'inline';
    btnLoading.style.display = 'none';
  }
}

// ============================================================
// SMOOTH SCROLL FOR ANCHOR LINKS
// ============================================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const top = target.getBoundingClientRect().top + window.pageYOffset - 80;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// ============================================================
// MARQUEE: pause on hover
// ============================================================
const marqueeInner = document.querySelector('.marquee-inner');
if (marqueeInner) {
  marqueeInner.addEventListener('mouseenter', () => {
    marqueeInner.style.animationPlayState = 'paused';
  });
  marqueeInner.addEventListener('mouseleave', () => {
    marqueeInner.style.animationPlayState = 'running';
  });
}
