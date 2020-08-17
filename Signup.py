import requests

import LoginInfo
from Parser import Parser


settings = {'USE_LOGIN': True,
            'USERNAME': LoginInfo.username,
            'PASSWORD': LoginInfo.password,
            'REQUESTED_CRNs': '84338, 93884, 91445, 89375, 91221, 91200, 91545, 83961, 83660',
            'SEMESTER': '202008',

            # Program settings
            'BASE_URL': 'https://oscar.gatech.edu/pls/bprod/',
            'LOGIN_URL': 'https://login.gatech.edu/cas/login?service=https://sso.sis.gatech.edu:443/ssomanager/c/SSB',
            'LT_ID': '<input type="hidden" name="lt" value="',
            'PAYLOAD_START': 'term_in=202008&RSTS_IN=DUMMY&assoc_term_in=DUMMY&CRN_IN=DUMMY&start_date_in=DUMMY'
                             '&end_date_in=DUMMY&SUBJ=DUMMY&CRSE=DUMMY&SEC=DUMMY&LEVL=DUMMY&CRED=DUMMY&GMOD=DUMMY'
                             '&TITLE=DUMMY&MESG=DUMMY&REG_BTN=DUMMY&MESG=DUMMY&'}

'''
# SESSID changes after each request and needs to be updated for future requests
def UpdateSESSID():
    SetCookie = str(response.headers['Set-Cookie']).split(';')
    SESSID = [c for i, c in enumerate(SetCookie) if 'SESSID=' in c][0]
    s.cookies.set(name='SESSID', value=SESSID[7:], domain='oscar.gatech.edu', path='/pls/bprod')'''


# Login and request current classes
s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
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


response = s.post(settings['BASE_URL'] + 'bwskfreg.P_AltPin',
                  data=dict(term_in=settings['SEMESTER']))
html = str(response.content)

if html.find('<h3>Current Schedule</h3>') == -1:
    raise Exception('Error logging in')


# Start generating payload by appending all current classes
htmlParser = Parser()
htmlParser.parse(html)

classPayload = settings['PAYLOAD_START'] + '&'.join(map(str, htmlParser.Classes))


# Finish payload by appending classes that need to be added
RequestedCRNs = set(settings['REQUESTED_CRNs'].replace(' ', '').split(','))
CurrentCRNs = set(map(lambda c: c.data['CRN_IN'], htmlParser.Classes))
CRNsToAdd = list(RequestedCRNs.difference(CurrentCRNs))  # [c for c in RequestedCRNs if c not in CurrentCRNs]

regs_row = len(htmlParser.Classes)  # Current number of classes
add_row = regs_row + len(CRNsToAdd)  # Total number of classes after adding new classes

PaddedCRNsToAdd = CRNsToAdd + [''] * (19 - add_row)  # Pads list with empty CRNs, 19 is the expected number of classes
for CRN in PaddedCRNsToAdd:
    classPayload += f'&RSTS_IN=RW&CRN_IN={CRN}&assoc_term_in=&start_date_in=&end_date_in='

# Add final payload information, will need to change to include signing up for waitlists
classPayload += f'regs_row={regs_row}&wait_row=0&add_row={add_row}&REG_BTN=Submit+Changes'


req = s.prepare_request(requests.Request('POST', settings['BASE_URL'] + 'bwckcoms.P_Regs', data=classPayload))
req.headers['Content-Type'] = 'application/x-www-form-urlencoded'
req.headers['Referer'] = 'https://oscar.gatech.edu/pls/bprod/bwskfreg.P_AltPin'
req.headers['Origin'] = 'https://oscar.gatech.edu'
req.headers['Host'] = 'oscar.gatech.edu'
req.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
req.headers['Accept-Encoding'] = 'gzip, deflate, br'
req.headers['Content-Type'] = 'application/x-www-form-urlencoded'
req.headers['Upgrade-Insecure-Requests'] = '1'

req._cookies['TESTID'] = 'set'

print('Prepared post request to sign up for ' + ', '.join(CRNsToAdd))
print(response.headers)
print(req.headers)
print(req._cookies)
if input('Send post request? (Y/N)').upper() == 'Y':
    response = s.send(req)
    print(response.status_code)
    print(response.content, file=open('response.html', 'w'))