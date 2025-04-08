document.addEventListener('DOMContentLoaded', () => {
  const submenuParents = document.querySelectorAll('.nav-item.has-submenu');

  submenuParents.forEach(parent => {
    const link = parent.querySelector('.nav-link');
    const submenu = parent.querySelector('.submenu');

    // Log submenu initialization
    console.log('Initializing submenu for:', link.textContent);

    link.addEventListener('click', event => {
      event.preventDefault();
      console.log('Clicked:', link.textContent);

      if (parent.classList.contains('active')) {
        // Collapse submenu
        parent.classList.remove('active');
        submenu.style.maxHeight = null; // Remove inline max-height to collapse
        console.log('Submenu collapsed.');
      } else {
        // Expand submenu
        parent.classList.add('active');
        submenu.style.maxHeight = submenu.scrollHeight + 'px';
        console.log('Submenu expanded. New height:', submenu.scrollHeight);
      }
    });
  });
});