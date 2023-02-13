let show_info = document.getElementById('change_info_btn')
show_info = show_info.addEventListener('click', show)


function show() {
    let info = document.getElementById('change_block')
    if (info.style.display == 'none') {
        info.style.display = "block";
    }
    else {
        info.style.display = "none";
    }
}
