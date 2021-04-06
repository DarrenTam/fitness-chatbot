from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

from service.chat_bot import start_chatbot

chat_bot_controller = False
app = Flask(__name__)
# sched = BackgroundScheduler(daemon=True)
#
#
# def start_chatbot():
#     global chat_bot_controller
#     chat_bot_controller = True
#     start_chatbot()
#
#
# sched.add_job(start_chatbot, 'interval', seconds=1, id="123")
# sched.start()
#

@app.route('/')
def health_check():
    # if chat_bot_controller:
    #     sched.remove_all_jobs()
    return 'up'

if __name__ == '__main__':
    app.run()
