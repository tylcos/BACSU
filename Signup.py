import requests

import LoginInfo
from Parser import Parser


settings = {'USE_LOGIN': False,
            'USERNAME': LoginInfo.username,
            'PASSWORD': LoginInfo.password,
            'REQUESTED_CRNs': '84338, 93884, 91445, 89375, 91221, 91200, 91545, 83961, 83660',
            'SEMESTER': '202008',

            # Program settings
            'BASE_URL': 'https://oscar.gatech.edu/pls/bprod/',
            'LOGIN_URL': 'https://login.gatech.edu/cas/login?service=https://sso.sis.gatech.edu:443/ssomanager/c/SSB',
            'LT_ID': '<input type="hidden" name="lt" value="',
            'PAYLOAD_START': 'term_in=202008&RSTS_IN=DUMMY&assoc_term_in=DUMMY&CRN_IN=DUMMY&start_date_in=DUMMY&end_date_in=DUMMY&SUBJ=DUMMY&CRSE=DUMMY&SEC=DUMMY&LEVL=DUMMY&CRED=DUMMY&GMOD=DUMMY&TITLE=DUMMY&MESG=DUMMY&REG_BTN=DUMMY&MESG=DUMMY&'}


s = requests.Session()

if settings['USE_LOGIN']:
    response = s.get(settings['LOGIN_URL'])

    # Read LT_ID, should change to use BeautifulSoup
    html = str(response.content)
    pos = html.index(settings['LT_ID']) + len(settings['LT_ID'])
    lt = html[pos:html.index('"', pos)]

    s.post(settings['LOGIN_URL'],
           data=dict(username=settings['USERNAME'],
                     password=settings['PASSWORD'],
                     lt=lt,
                     execution='e1s1',
                     _eventId='submit',
                     submit='LOGIN'))

    # Get current classes
    response = s.post(settings['BASE_URL'] + 'bwskfreg.P_AltPin',
                      data=dict(term_in=settings['SEMESTER']))
    html = str(response.content)
    print(html, file=open('response.html', 'w'))

    if html.find('<h3>Current Schedule</h3>') == -1:
        raise Exception('Error logging in')
else:
    html = open('response.html', 'r').read()


htmlParser = Parser()
htmlParser.parse(html)

classPayload = settings['PAYLOAD_START'] + '&'.join(map(str, htmlParser.Classes))
print(classPayload)
