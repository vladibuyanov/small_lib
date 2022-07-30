from myapp import create_app

start_message = 'App was started'
print(start_message)

if __name__ == "__main__":
    create_app().run(host='0.0.0.0', port=5000)
