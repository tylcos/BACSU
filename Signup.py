import sys

import requests

from Parser import Parser


settings = {
    'REQUESTED_CRNs': '',
    'SEMESTER': '202108',
    'SESSID': '',

    # Program settings
    'BASE_URL': 'https://oscar.gatech.edu/pls/bprod/',
    'LOGIN_URL': 'https://sso.gatech.edu/cas/login',
}

# Login and request current classes
s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
s.cookies['SESSID'] = settings['SESSID']

response = s.post(settings['BASE_URL'] + 'bwskfreg.P_AltPin',
                  data={
                      'term_in': settings['SEMESTER']
                  })

responseStr = str(response.content)
if '<h3>Current Schedule</h3>' not in responseStr:
    raise Exception('Error logging in')


# Start generating payload by appending all current classes
htmlParser = Parser()
htmlParser.parse(responseStr)

payloadStart = f'term_in={settings["SEMESTER"]}&RSTS_IN=DUMMY&assoc_term_in=DUMMY&CRN_IN=DUMMY&start_date_in=DUMMY&end_date_in=DUMMY&SUBJ=DUMMY&CRSE=DUMMY&SEC=DUMMY&LEVL=DUMMY&CRED=DUMMY&GMOD=DUMMY&TITLE=DUMMY&MESG=DUMMY&REG_BTN=DUMMY&MESG=DUMMY&'
classPayload = payloadStart + '&'.join(map(str, htmlParser.Classes))

# Finish payload by appending classes that need to be added
RequestedCRNs = set(settings['REQUESTED_CRNs'].replace(' ', '').split(','))
CurrentCRNs = set(map(lambda c: c.data['CRN_IN'], htmlParser.Classes))
CRNsToAdd = list(RequestedCRNs.difference(CurrentCRNs))

regs_row = len(htmlParser.Classes)  # Current number of classes
add_row = 1 + regs_row + len(CRNsToAdd)  # Total number of classes after adding new classes, 1 for the dummy class in payloadStart

PaddedCRNsToAdd = CRNsToAdd + [''] * (19 - add_row)  # Pads list with empty CRNs, 19 is the expected number of classes
for CRN in PaddedCRNsToAdd:
    classPayload += f'&RSTS_IN=RW&CRN_IN={CRN}&assoc_term_in=&start_date_in=&end_date_in='

# Add final payload information, will need to change to include signing up for waitlists
classPayload += f'&regs_row={regs_row}&wait_row=0&add_row={add_row}&REG_BTN=Submit+Changes'


# Send finished payload
print('Prepared post request to sign up for ' + ', '.join(CRNsToAdd))
print(classPayload)
if input('Send post request? (Y/N)').upper() == 'Y':
    send = s.post(settings['BASE_URL'] + 'bwckcoms.P_Regs', data=classPayload)

    print(response.status_code)
    print(response.content, file=open('response.html', 'w'))
