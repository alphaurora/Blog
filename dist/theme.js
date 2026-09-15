(() => {
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  let choice = null;
  try { choice = localStorage.getItem('alpha-theme'); } catch {}
  if (!['light', 'dark'].includes(choice)) choice = null;
  function apply(theme) {
    document.documentElement.dataset.theme = theme;
    const button = document.querySelector('.theme-toggle');
    if (button) {
      button.textContent = theme === 'dark' ? '☀ 浅色' : '◐ 深色';
      button.setAttribute('aria-label', theme === 'dark' ? '切换浅色模式' : '切换深色模式');
      button.setAttribute('aria-pressed', String(theme === 'dark'));
    }
  }
  apply(choice || (media.matches ? 'dark' : 'light'));
  document.addEventListener('DOMContentLoaded', () => {
    apply(document.documentElement.dataset.theme);
    document.querySelector('.theme-toggle').addEventListener('click', () => {
      choice = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('alpha-theme', choice); } catch {}
      apply(choice);
    });
  });
  media.addEventListener('change', () => { if (!choice) apply(media.matches ? 'dark' : 'light'); });
})();
