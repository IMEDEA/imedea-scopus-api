import ssh_tunnel
import utils
import urllib2


class Auth:

    def __init__(self, api_key, choice=None, tunnel_url=None, tunnel_port=None):
        ssh_tunnel.init_proxy(tunnel_url, tunnel_port)
        self.api_key = api_key
        url = 'http://api.elsevier.com/authenticate?platform=SCOPUS'
        if choice:
            url += '&choice=' + choice
        header = {
            'Accept': 'application/json',
            'X-ELS-APIKey': api_key
        }
        try:
            res = utils.get_json_from_url(url, header)
            self.token = res['authenticate-response']['authtoken']
        except urllib2.HTTPError as e:
            print "Error authenticating"
            utils.print_http_error(e)
            exit(-1)

    def getheader(self):
        return {
                'X-ELS-APIKey': self.api_key,
                'X-ELS-Authtoken': self.token,
                'Accept': 'application/json'
        }

