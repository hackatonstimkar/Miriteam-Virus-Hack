

def addItem(eventId, itemCode):
    return r"'action':'addItem', 'eventId':'{}', 'itemCode':'{}'".format(eventId,itemCode)


def setStatus(eventId, requestEventId, state, items, total):
    return r"'action' : 'SetStatus', 'eventId': '{}', 'requestEventId' :'{}', 'state' : '{}', items : '{}', 'total' : '{}'".format(eventId, requestEventId, state, items, total)

def extInfo(eventId, requestEventId, info):
    return r"'action' : 'extInfo','eventId' : '{}', 'requestEventId' : '{}', 'info' : '{}'".format(eventId, requestEventId, info)

def subscribe(eventId, frequency, types):
    return r"'action' : 'subscribe', 'eventId' : '{}', 'frequency': '1000', 'type' : 'Weight'"

def cancel():
    return r"'action' : 'cancel'"

def deleteTransaction():
    return r"'action' : 'deleteTransaction'"

def deleteAll(eventId, itemCode):
    return r"'action' : 'deleteAll', 'eventId' : '{}', 'itemCode' : '{}'".format(eventId, itemCode)

def deletePosition(eventId, itemNumber):
    return r"'action' : 'deletePosition', 'eventId' : '{}', 'itemNumber': '{}' ".format(eventId, itemNumber)



