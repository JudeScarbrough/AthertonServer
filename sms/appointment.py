import firebase
import time
import text

def oneMinute():
    currentUnix = int(time.time())
    data = firebase.get_all_data()
    print(data)
    clientQueue = []

    for userKey, userData in data.items():
        if "appointmentData" in userData:
            
            minDelay = userData["appointmentData"]["minutesDelay"]

            for client in userData["clientData"]:
                compareTime = int(client["date"]) + (int(minDelay) * 60)

                if currentUnix >= compareTime and (not client.get("messageSent", False)):
                    message = makeAppointmentMessage(userData["appointmentData"], client)
                    clientQueue.append((client["phoneNumber"], message))
                    client["messageSent"] = True

    for phoneNumber, message in clientQueue:
        text.send(phoneNumber, message)

    firebase.update_user_data(data)

def makeAppointmentMessage(appointmentData, client):

    finalString = ""

    if appointmentData["firstName"] or appointmentData["lastName"]:
        finalString += appointmentData["firstText"]
        
    if appointmentData["firstName"]:
        finalString += client["firstName"]

    if appointmentData["lastName"]:
        finalString += " " + client["lastName"]

    finalString += appointmentData["secondText"]

    print(finalString)
    return finalString




