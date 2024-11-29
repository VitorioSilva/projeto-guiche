document.addEventListener('scroll', function() {
    const header = document.querySelector('header');

    if (window.scrollY > 50) {
      header.classList.add('hidden');
    } else {
      header.classList.remove('hidden');
    }
  });