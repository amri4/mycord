// ── SEARCH INDEX ──
const INDEX = [
  { title: "Introduction", section: "Getting Started", id: "introduction" },
  { title: "Installation", section: "Getting Started", id: "installation" },
  { title: "Quick Start", section: "Getting Started", id: "quickstart" },
  { title: "mycord.Bot", section: "API Reference", id: "bot" },
  { title: "Bot.start()", section: "mycord.Bot", id: "bot-start" },
  { title: "Bot.run_bot()", section: "mycord.Bot", id: "bot-run_bot" },
  { title: "Bot.autoload_cogs()", section: "mycord.Bot", id: "bot-autoload_cogs" },
  { title: "Bot.get_env()", section: "mycord.Bot", id: "bot-get_env" },
  { title: "Database Proxy", section: "mycord.Bot", id: "bot-db-proxy" },
  { title: "mycord.Cog", section: "API Reference", id: "cog" },
  { title: "mycord.DB", section: "API Reference", id: "db" },
  { title: "DB.create_table()", section: "mycord.DB", id: "db-create_table" },
  { title: "DB.insert()", section: "mycord.DB", id: "db-insert" },
  { title: "DB.insert_replace()", section: "mycord.DB", id: "db-insert_replace" },
  { title: "DB.fetchone()", section: "mycord.DB", id: "db-fetchone" },
  { title: "DB.fetchall()", section: "mycord.DB", id: "db-fetchall" },
  { title: "DB.update()", section: "mycord.DB", id: "db-update" },
  { title: "DB.delete()", section: "mycord.DB", id: "db-delete" },
  { title: "DB.exists()", section: "mycord.DB", id: "db-exists" },
  { title: "DB.close()", section: "mycord.DB", id: "db-close" },
  { title: "mycord.Tools", section: "API Reference", id: "tools" },
  { title: "Tools.chance()", section: "mycord.Tools", id: "tools-chance" },
  { title: "Tools.timestamp()", section: "mycord.Tools", id: "tools-timestamp" },
  { title: "mycord.os", section: "API Reference", id: "mycord-os" },
  { title: "Minimal Bot", section: "Examples", id: "example-minimal" },
  { title: "Bot with Cogs", section: "Examples", id: "example-cogs" },
  { title: "Bot with Database", section: "Examples", id: "example-database" },
  { title: "Cog File", section: "Examples", id: "example-cog-file" },
  { title: "Moderation Cog", section: "Examples", id: "example-moderation" },
];

// ── SEARCH ──
const searchInput = document.getElementById('search');
const searchResults = document.getElementById('searchResults');

searchInput.addEventListener('input', () => {
  const q = searchInput.value.trim().toLowerCase();
  if (!q) { searchResults.classList.remove('open'); return; }

  const matches = INDEX.filter(item =>
    item.title.toLowerCase().includes(q) || item.section.toLowerCase().includes(q)
  ).slice(0, 8);

  if (!matches.length) { searchResults.classList.remove('open'); return; }

  searchResults.innerHTML = matches.map(item => `
    <div class="search-result-item" onclick="goTo('${item.id}')">
      <span class="res-title">${item.title}</span>
      <span class="res-section">${item.section}</span>
    </div>
  `).join('');
  searchResults.classList.add('open');
});

document.addEventListener('click', e => {
  if (!e.target.closest('.search-wrap')) {
    searchResults.classList.remove('open');
  }
});

function goTo(id) {
  searchResults.classList.remove('open');
  searchInput.value = '';
  const el = document.getElementById(id);
  if (el) { el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  closeSidebar();
}

// ── COPY BUTTONS ──
function copyCode(btn) {
  const pre = btn.closest('.codeblock').querySelector('pre');
  const text = pre.innerText;
  navigator.clipboard.writeText(text).then(() => {
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
  });
}

// ── ACTIVE NAV ON SCROLL ──
const sections = document.querySelectorAll('section[id], .method-card[id]');
const navLinks = document.querySelectorAll('.nav-link, .nav-sub');

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.id;
      navLinks.forEach(link => {
        const href = link.getAttribute('href');
        link.classList.toggle('active', href === '#' + id);
      });
    }
  });
}, { rootMargin: '-20% 0px -70% 0px', threshold: 0 });

sections.forEach(s => observer.observe(s));

// ── MOBILE SIDEBAR ──
const hamburger = document.getElementById('hamburger');
const sidebar   = document.getElementById('sidebar');
const overlay   = document.getElementById('overlay');

function openSidebar()  { sidebar.classList.add('open');  overlay.classList.add('open'); }
function closeSidebar() { sidebar.classList.remove('open'); overlay.classList.remove('open'); }

hamburger.addEventListener('click', () => {
  sidebar.classList.contains('open') ? closeSidebar() : openSidebar();
});
overlay.addEventListener('click', closeSidebar);

// close sidebar on nav click (mobile)
navLinks.forEach(link => {
  link.addEventListener('click', () => {
    if (window.innerWidth <= 768) closeSidebar();
  });
});
