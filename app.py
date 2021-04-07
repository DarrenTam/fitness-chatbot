from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

from service.chat_bot import start_chatbot

chat_bot_controller = False
app = Flask(__name__)

@app.route('/')
def health_check():
    global chat_bot_controller
    if not chat_bot_controller:
        chat_bot_controller=True
        start_chatbot()
    return 'up'

if __name__ == '__main__':
    app.run(port=8080)
