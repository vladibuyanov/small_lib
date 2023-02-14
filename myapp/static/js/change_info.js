let change_info = document.getElementById('change_info_btn')
change_info = change_info.addEventListener('click', show)


function show() {
    let info = document.getElementById('change_block')
    if (info.style.display == "none") {
        info.style.display = "flex";
    }
    else {
        info.style.display = "none";
    }
}
