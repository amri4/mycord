const DARK_MODE_KEY = 'mycord-dark-mode';

function applyDarkMode(enabled) {
  document.body.classList.toggle('dark-mode', enabled);
  document.body.classList.toggle('light-mode', !enabled);
  const toggle = document.getElementById('dark-mode-toggle');
  if (toggle) {
    toggle.textContent = enabled ? 'Light mode' : 'Dark mode';
  }
}

function loadDarkModeSetting() {
  const saved = localStorage.getItem(DARK_MODE_KEY);
  if (saved !== null) {
    return saved === 'true';
  }
  return true;
}

function toggleDarkMode() {
  const enabled = !document.body.classList.contains('dark-mode');
  applyDarkMode(enabled);
  localStorage.setItem(DARK_MODE_KEY, enabled);
}

window.addEventListener('DOMContentLoaded', () => {
  applyDarkMode(loadDarkModeSetting());
  const header = document.querySelector('.wy-side-nav-search') || document.querySelector('body');
  if (header) {
    const wrapper = document.createElement('div');
    wrapper.className = 'dark-mode-toggle-wrapper';
    const button = document.createElement('button');
    button.id = 'dark-mode-toggle';
    button.type = 'button';
    button.addEventListener('click', toggleDarkMode);
    wrapper.appendChild(button);
    header.insertAdjacentElement('afterend', wrapper);
  }
});
