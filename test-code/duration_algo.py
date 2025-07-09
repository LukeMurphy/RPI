
import datetime as dt
import datetime
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont


class EventObject:
    startDate = dt
    endDate = dt
    duration = 0

    def __init__(self):
        """
        Purpose:
        """


eventList = [
    ["A", "5/1/2025", "7/2/2025"],
    ["B", "5/3/2025", "5/9/2025"],
    ["B2", "5/6/2025", "5/8/2025"],
    ["C", "5/2/2025", "5/9/2025"],
    ["E", "5/8/2025", "5/22/2025"],
    ["D", "5/10/2025", "5/23/2025"],
    ["F", "5/20/2025", "6/1/2025"],
    ["G", "5/26/2025", "6/1/2025"],
    ["H", "5/30/2025", "6/6/2025"],
    ["J", "6/1/2025", "6/11/2025"],
    ["I", "6/19/2025", "6/27/2025"],
    ["K", "7/3/2025", "7/12/2025"],
]

eventArray = []
eventsArray = []
for element in eventList:
    eObj = EventObject()
    eObj.startDate = dt.datetime.strptime(element[1], "%m/%d/%Y").date()
    eObj.endDate = dt.datetime.strptime(element[2], "%m/%d/%Y").date()
    eObj.name = element[0]
    # eObj.duration = element[2]
    eventArray.append(eObj)
    eventsArray.append([eObj.startDate, eObj.endDate, eObj.name])
    # eventsArray.append([eObj.startDate])

    # print(eObj.startDate)

# sort on end date
eventsArray.sort(key=lambda x: x[1])
finalList = [eventsArray[0]]
lastEventAdded = finalList[-1]

def doActions(lastEventAdded):

    # print(f"First event is {lastEventAdded}")
    # print("-------------")
    # for feV in eventsArray:
    #     print(feV)

    for _event in eventsArray:
        # print(f"\nTest {_event[2]} {_event}")
        if _event[0] < lastEventAdded[1]:
            # print(f"Eliminate {_event}")
            pass
        elif _event != lastEventAdded:
            finalList.append(_event)
            lastEventAdded = _event


    print("-------------")
    for feV in finalList:
        print(feV)

doActions(lastEventAdded)



# Thanks Sourcert AI for this optimized version
from collections import namedtuple

Event = namedtuple('Event', ['start', 'end', 'name'])

def select_non_overlapping_events(events):
    """Selects the maximum set of non-overlapping events sorted by end date."""
    events = sorted(events, key=lambda x: x.end)
    final = []
    last_end = None
    for event in events:
        if last_end is None or event.start >= last_end:
            final.append(event)
            last_end = event.end
    return final

# Convert your eventsArray to Event objects
events = [Event(start, end, name) for start, end, name in eventsArray]
# finalList = select_non_overlapping_events(events)
# for event in finalList:
    # print(event)



def drawTheEventList():
    resultImage = Image.new("RGB", (600,400))
    resultImageDraw = ImageDraw.Draw(resultImage)
    resultImageDraw.rectangle((0,0,600,400), fill = (225,225,225))

    # specified font size
    font = ImageFont.truetype(r'/Users/lamshell/Documents/Dev/LEDELI/RPI/assets/fonts/roboto/Roboto-Black.ttf', 16) 

    _initX = 50
    _initY = 50
    _incrementalDays = 0
    _barHeight = 10
    _dayWidth = 5
    _barGap = 10

    _startDayString = "5/1/2025"
    _startDay = dt.datetime.strptime(_startDayString, "%m/%d/%Y").date()

    _title = "Events sorted by end-date, max non-overlapping selected"
    _title = "Events sorted by start-date, max non-overlapping selected"
    eventsArray.sort(key=lambda x: x[0])

    resultImageDraw.text((10 ,10 ), _title, font = font, align ="right", fill = (0,0,0)) 

    for _incrementalEvent, feV in enumerate(eventsArray):
        dayDiff = feV[1]-feV[0]
        print(f"Event {feV[2]} duration {dayDiff.days}")
        _fromStart = (feV[0] - _startDay)
        _x1 = _initX + _fromStart.days * _dayWidth
        _x2 = _x1 + dayDiff.days * _dayWidth

        _y1 = _initY +_incrementalEvent * (_barHeight + _barGap)
        _y2 = _y1 + _barHeight

        resultImageDraw.text((_x2 + 10 ,_y1 - 5), feV[2], font = font, align ="right", fill = (0,0,0)) 

        if feV in finalList :
            resultImageDraw.rectangle((_x1,_y1,_x2,_y2), fill = (255,0,0))
        else :
            resultImageDraw.rectangle((_x1,_y1,_x2,_y2), fill = (0,0,100))

        _incrementalDays += dayDiff.days
    resultImage.save("result.png")

drawTheEventList()