from tests.test_login import test_login
from tests.login import test_go_to_login
from tests.test_logout import test_logout

url = 'http://127.0.0.1:5000'
email = 'vladibuyanov@gmail.com'
psw = '12345'


def test_login_logout():
    assert test_go_to_login() == 'http://192.168.0.100:5000/login'
    assert test_login(email, psw) == 'http://192.168.0.100:5000/'
    assert test_logout() == 'http://192.168.0.100:5000/login'


if __name__ == "__main__":
    # test_go_to_login()
    # test_login(email, psw)
    # test_logout()
    test_login_logout()
