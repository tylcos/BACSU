import Signup
import ClassParser


def GenerateSignupPayload(currentClassesHTML):
    payloadStart = f'term_in={Signup.settings["SEMESTER"]}&RSTS_IN=DUMMY&assoc_term_in=DUMMY&CRN_IN=DUMMY&start_date_in=DUMMY&end_date_in=DUMMY&SUBJ=DUMMY&CRSE=DUMMY&SEC=DUMMY&LEVL=DUMMY&CRED=DUMMY&GMOD=DUMMY&TITLE=DUMMY&MESG=DUMMY&REG_BTN=DUMMY&MESG=DUMMY&'

    # Append all current classes
    classParser = ClassParser.ClassParser(currentClassesHTML)
    classPayload = payloadStart + '&'.join(map(str, classParser.Classes))

    # Append classes to sign up for
    RequestedCRNs = set(Signup.settings['REQUESTED_CRNs'].replace(' ', '').split(','))
    CurrentCRNs = set(map(lambda c: c.data['CRN_IN'], classParser.Classes))
    CRNsToAdd = list(RequestedCRNs.difference(CurrentCRNs))

    regs_row = len(classParser.Classes)  # Current number of classes
    add_row = 1 + regs_row + len(CRNsToAdd)  # Total number of classes after adding new classes, 1 for the dummy class in payloadStart
    PaddedCRNsToAdd = CRNsToAdd + [''] * (19 - add_row)  # Pads list with empty CRNs, 19 is the expected number of classes

    for CRN in PaddedCRNsToAdd:
        classPayload += f'&RSTS_IN=RW&CRN_IN={CRN}&assoc_term_in=&start_date_in=&end_date_in='

    # Add final payload information, will need to change to include signing up for waitlists
    classPayload += f'&regs_row={regs_row}&wait_row=0&add_row={add_row}&REG_BTN=Submit+Changes'

    return classPayload
