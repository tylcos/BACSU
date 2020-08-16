import requests

import LoginInfo
from Parser import Parser


settings = {'LOGIN': False,
            'USERNAME': LoginInfo.username,
            'PASSWORD': LoginInfo.password,
            'BASE_URL': 'https://oscar.gatech.edu/pls/bprod/',
            'LOGIN_URL': 'https://login.gatech.edu/cas/login?service=https://sso.sis.gatech.edu:443/ssomanager/c/SSB',
            'SEMESTER': '202008',
            'LT_ID': '<input type="hidden" name="lt" value="'}


s = requests.Session()

if settings['LOGIN']:
    response = s.get(settings['LOGIN_URL'])

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

    if html.find('<h3>Current Schedule</h3>') == -1:
        raise Exception('Error logging in')
else:
    html = open('html.txt', 'r').read()

htmlParser = Parser()
htmlParser.parse(html)

# response = s.get(settings['BASE_URL'] + 'bwckcoms.P_Regs')

for c in htmlParser.Classes:
    print(str(c))
print(response.content, file=open('response.html', 'w'))