let show_info = document.getElementById('change_info_btn').addEventListener('click', show)
let info = document.getElementById('change_block')

function show() {
    if (info.style.display == 'none') {
        info.style.display = "block";
    }
    else {
        info.style.display = "none";
    }
}
