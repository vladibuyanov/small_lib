from tests.login_logout import Test_login_logout

url = 'http://127.0.0.1:5000'
user_email = 'vladibuyanov@gmail.com'
psw = '12345'


def test_login_logout():
    main_test = Test_login_logout(url)
    main_test.go_to_login()
    main_test.login(user_email, psw)
    main_test.logout()


if __name__ == "__main__":
    test_login_logout()
