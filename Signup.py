import requests

import PayloadGenerator


settings = {
    # CRNs to sign up for seperated by ,
    'REQUESTED_CRNs': '',

    # SESSID Cookie. After copying the SESSID, close the browser tab where you copied it to
    # prevent the browser from using an old SESSID and signing you out
    'SESSID': '',

    # Semester code
    'SEMESTER': '202108'
}


def main():
    # Request current classes
    s = requests.Session()
    s.cookies['SESSID'] = settings['SESSID']
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
    s.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    s.headers['Accept-Language'] = 'en-US,en;q=0.5'
    s.headers['Accept-Encoding'] = 'gzip, deflate, br8'
    s.headers['Content-Type'] = 'application/x-www-form-urlencoded'
    s.headers['Origin'] = 'https://oscar.gatech.edu'
    s.headers['Referer'] = 'https://oscar.gatech.edu/'
    s.headers['Upgrade-Insecure-Requests'] = '1'
    s.headers['Connection'] = 'keep-alive'
    s.headers['Sec-Fetch-Dest'] = 'document'
    s.headers['Sec-Fetch-Mode'] = 'navigate'
    s.headers['Sec-Fetch-Site'] = 'same-origin'
    s.headers['Sec-Fetch-User'] = '?1'

    response = s.post('https://oscar.gatech.edu/pls/bprod/bwskfreg.P_AltPin', data={'term_in': settings['SEMESTER']})
    responseStr = str(response.content)

    if '<h3>Current Schedule</h3>' not in responseStr:
        raise Exception('Error logging in')


    # Check if user has time ticket


    # Send payload to sign up for classes
    classPayload = PayloadGenerator.GenerateSignupPayload(responseStr)

    s.headers['Referer'] = 'https://oscar.gatech.edu/bprod/bwckcoms.P_Regs'
    send = s.post('https://oscar.gatech.edu/bprod/bwckcoms.P_Regs', data=classPayload)


    print('Response code: ' + str(response.status_code))


if __name__ == "__main__":
    main()
