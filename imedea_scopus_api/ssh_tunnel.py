import socket
import urllib.request, urllib.error, urllib.parse
import socks


def init_proxy(tunnerl_url, tunnel_port):
    if tunnel_port:
        if not tunnerl_url:
            tunnerl_url = "127.0.0.1"
        try:
            # socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", int(tunnel_port))
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", int(tunnel_port))
            socket.socket = socks.socksocket
            # Connection check
            # urllib.request.urlopen("http://127.0.0.1")
        except socks.ProxyConnectionError:
            print(("Tunnel port sent "
                   "{}"
                   ", but an exception occurred while connecting to tunnel, program will exit...\n"
                   "Check if you need tunneling, if not remove tunnel port {{port}} parameter from els_client constructor.")\
                   .format(tunnel_port))
            exit(-1)
