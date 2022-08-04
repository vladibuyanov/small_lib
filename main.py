from myapp import create_app


def start_app():
    host, port = '0.0.0.0', 8000
    start_message = 'App was started'
    print(start_message)
    create_app().run()


if __name__ == "__main__":
    start_app()
