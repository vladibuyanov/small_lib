from myapp import create_app

""" Create app """
config_file_path = '../config.py'
app = create_app(config_file_path)


if __name__ == "__main__":
    app.run()
