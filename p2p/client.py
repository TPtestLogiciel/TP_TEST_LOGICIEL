import http.client
import json
import sys
import sched, time

# ######## POST

def post():
    print("-- post function called --")
    headers = {'Content-Type': 'application/json'}
    while(True):
        text_input = input('> ')
        data = {'username': 'edern', 'text': text_input}
        json_data = json.dumps(data)
        print(json_data)
        conn.request('POST', '/p2p_post', json_data, headers)
        
        if(__debug__):
            response = conn.getresponse()
            print("Status: {} and reason: {}".format(response.status, response.reason))
        
        if(text_input == 'close'):
            sys.exit()

# ####### GET

def get():
    print("-- get function called --")
    conn.request("GET", "/p2p_get")
    response = conn.getresponse()
    if(__debug__):
        print("Status: {} and reason: {}".format(response.status, response.reason))
    server_text = json.loads(response.read())
    print('< ' + server_text['text'])
    conn.close()

if __name__ == "__main__":
    conn = http.client.HTTPConnection('localhost', 8080)
    post()
    # get()