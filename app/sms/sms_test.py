import sys
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException


def send_massage(phonenum, message):
    api_key = "NCSGLMHSQ2FTVZUA"
    api_secret = "6SJTTSSM27RIGTG3ERVXKFLKVWVEUHFI"

    params = dict()
    params['type'] = 'sms'
    params['to'] = phonenum
    params['from'] = '01044321237'
    params['text'] = message
    cool = Message(api_key, api_secret)

    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    # sys.exit()
