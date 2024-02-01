from scripts import *
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import os

app = Flask(__name__)

def make_verifications():
    data = get_data_Notion_API()
    new_query_API = transform_API_data(data)
    
    try:
        saved_query = load_save_json()
    except FileNotFoundError:
        save_new_json(new_query_API)
        saved_query = load_save_json()

    verify_modifications(new_query_API, saved_query)

@app.route('/')
def home():
    return "Verificando o status do projeto..."

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=make_verifications, trigger='interval', seconds=10)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        app.run(port=5000, debug=True)
        
    except (KeyboardInterrupt, SystemExit):
        print('Stop')
        print('Scheduler is running:', scheduler.running)  # Verificar se o agendador está rodando
        scheduler.shutdown()
        print('Scheduler is running:', scheduler.running) 