
import groupMessage
import appointment
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

def check_database():
    appointment.oneMinute()

@app.route('/execute', methods=['POST'])
def execute_code():

    data = request.json
    print("Received data:", data)
    groupMessage.messageGroups(data["userId"], data["groupIndexes"], data["message"])
    return "Data processed", 200

if __name__ == '__main__':
    # Set up the scheduler to check the database every minute
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_database, 'interval', minutes=1)
    scheduler.start()
    
    # Start the Flask server
    app.run(debug=True)
