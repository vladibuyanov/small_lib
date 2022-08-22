function click_show() {
    let sm_btn = document.querySelectorAll('[id="show_more_btn"]');
    for (let i = 0; i < sm_btn.length; i++) {
        let number = i;
        sm_btn[i].addEventListener(
        'click',
        function show() {
            let about_book = document.querySelectorAll('[id=about_book]');
            if (about_book[number].style.display == 'none') {
              about_book[number].style.display = "block";
              sm_btn[i].innerHTML = '<- Close';
            }
            else {
                about_book[number].style.display = "none";
                sm_btn[i].innerHTML = 'Show more ->';
            }
        });
    }
}

click_show()
