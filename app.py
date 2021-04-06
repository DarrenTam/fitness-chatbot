from service.chat_bot import start_chatbot

from flask import Flask

app = Flask(__name__)


@app.route('/')
def health_check():
    return 'up'


if __name__ == '__main__':
    app.run(port=8080)
    start_chatbot()
