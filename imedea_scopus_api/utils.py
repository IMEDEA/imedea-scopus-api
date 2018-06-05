import urllib2
import json


def get_json_from_url(url, header):
    json_response = None
    try:
        request = urllib2.Request(url, headers=header)
        urlopen = urllib2.urlopen(request)
        response = urlopen.read()
        json_response = json.loads(response)
    except urllib2.HTTPError as e:
        raise e
    except ValueError:
        print "Error decoding json for " + url
    return json_response


def print_http_error(e):
    print e
    print "Reason:"
    if e.code == 300:
        print "You have multiple choices, add choice=YOUR_CHOICE as ELSClient constructor parameter"
    elif e.code == 400:
        print "Invalid request: invalid information submitted"
    elif e.code == 401:
        print "Authenticate error: missing or invalid credentials"
    elif e.code == 403:
        print "Authorization/Entitlements Error: User cannot be authenticated or entitlements " \
              "cannot be validated."
    elif e.code == 405:
        print "Invalid HTTP method"
    elif e.code == 406:
        print "Invalid Mime Type"
    elif e.code == 429:
        print "Quota exceeded associated to the API Key"
    elif e.code == 500:
        print "General error: backend processing error"

