let dropdownButton = document.getElementById('dropdown-btn');
let dropdownMenu = document.querySelector('.dropdown-menu');

dropdownButton.addEventListener('click', () => {
  dropdownMenu.classList.toggle('show');
});

window.addEventListener('click', (event) => {
  if (!event.target.matches('.btn')) {
    dropdownMenu.classList.remove('show');
  }
});
