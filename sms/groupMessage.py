import text
import firebase



def messageGroups(userId, groupIndexes, message):

    recipients = []

    # For each group find all the members of the group and add their numbers to the recipients list
    for groupIndex in groupIndexes:
        recipients.extend(findGroupMembers(userId, groupIndex))


    # check for numbers repeating and delete so that there is only one of each


    # send text to all the gathered recipients
    for phoneNumber in recipients:
        text.send(phoneNumber, message)





def findGroupMembers(userId, groupIndex):
    userData = firebase.get_user_data(userId)

    memberList = []

    for client in userData["clientData"]:
        for clientIndex in client["groups"]:
            if clientIndex == groupIndex:
                memberList.append(client["phoneNumber"])
                break

    return memberList









    