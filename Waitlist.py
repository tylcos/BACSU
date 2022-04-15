import requests
import time
import winsound
import webbrowser
import clipboard


requestedCRNs = ''
requestInterval = 60

baseURL = 'https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in=202208&crn_in='


def updateSeats():
    for i, crn in enumerate(crns):
        url = baseURL + crn
        try:
            html = str(s.get(url, timeout=2).content)

            pos = [html.index("dddefault")]
            seats = []
            for posIndex in range(6):
                pos.append(html.index("dddefault", pos[posIndex] + 1) + 11)
                seats.append(int("".join([c for c in html[pos[-1]:pos[-1] + 3] if c.isdigit()])))

            totalSeats = seats[0]
            currentSeats = seats[1]
            remainingSeats = seats[2]
            waitList = seats[4]
            remainingWaitList = seats[5]

            if totalSeats < 1 or totalSeats != currentSeats + remainingSeats:
                print('Invalid class CRN: ' + crn)

            if remainingSeats > 0:
                if hasOpenSeats[i] < 2:
                    hasOpenSeats[i] = 2

                    winsound.Beep(2000, 500)
                    clipboard.copy(crn)
                    webbrowser.open(url, new=2)

                print('Seat available in CRN: ' + crn + ' with ' + str(currentSeats) + ' out of ' + str(totalSeats))
            elif remainingWaitList > 0:
                if hasOpenSeats[i] < 1:
                    hasOpenSeats[i] = 1

                    winsound.Beep(2000, 500)
                    clipboard.copy(crn)
                    webbrowser.open(url, new=2)

                print('Waitlist seat available in CRN: ' + crn + ' with ' + str(remainingWaitList) + ' out of ' + str(waitList))
            else:
                hasOpenSeats[i] = False
        except Exception as e:
            print('Error reaching ' + url + ' with error: ' + str(e))


# Request classes
s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                          '(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

crns = requestedCRNs.replace(' ', '').split(',')
hasOpenSeats = [0] * len(crns)  # True if a class has open seats

requestNumber = 0
while True:
    print('\nMaking Request ' + str(requestNumber))
    requestNumber += 1
    requestTime = time.time()
    updateSeats()

    if not any(hasOpenSeats):
        print('No seats available in any classes')

    sleepTime = requestTime + requestInterval - time.time()
    if sleepTime > 0:
        time.sleep(sleepTime)
    else:
        print('Requests taking longer than given time interval of ' + str(requestInterval))
