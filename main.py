from myapp import create_app


def start_app(app):
    host = '0.0.0.0'
    port = 8000
    start_message = 'App was started'
    print(start_message)
    app.run(host=host, port=port)


if __name__ == "__main__":
    start_app(create_app())
