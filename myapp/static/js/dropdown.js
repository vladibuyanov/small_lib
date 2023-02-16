let dropdownButton = document.getElementById('dropdown-btn');
dropdownButton = dropdownButton.addEventListener('click', dropdown)

let dropdownMenu = document.querySelector('.dropdown-menu');

function dropdown() {
    dropdownMenu.classList.add('show');
}

window.addEventListener('click', (event) => {
  if (!event.target.matches('.btn')) {
    dropdownMenu.classList.remove('show');
  }
});
