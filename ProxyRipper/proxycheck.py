import requests
import ProxyEngine
from threading import Thread

def check_proxy(object, timeout, attempts, callback, isAsync=False):

    STATUS = None
    for _ in range(attempts):

        for protocol_string in getProtocolsList(object.protocol):
            try:
                response = requests.get("https://www.myip.com", proxies={
                    'https': f"{protocol_string}://{object.ip}:{object.port}",
                    'http' : f"{protocol_string}://{object.ip}:{object.port}"
                }, timeout=timeout)

                if (response.status_code == 200):
                    object.setLatency(round(response.elapsed.microseconds / 1000))

                    if isAsync:
                        callback(object)
                        return
                    else:
                        return object
                else:
                    STATUS = None
            except requests.exceptions.ConnectTimeout:
                STATUS = None
            except requests.exceptions.ConnectionError:
                STATUS = None
            except Exception:
                STATUS = None
        # print("checked")
    if isAsync:
        callback(STATUS)
        return
    else:
        return STATUS

def checkUrl(url, timeout):
    try:
        return requests.get(url, timeout=timeout).status_code
    except Exception:
        return 404

def getProtocolsList(bitmap):
    protocols = []

    if ProxyEngine.ProxyEngine.checkProtocolExistence(bitmap, ProxyEngine.Protocol.SOCKS5):
        protocols.append('socks5')

    elif ProxyEngine.ProxyEngine.checkProtocolExistence(bitmap, ProxyEngine.Protocol.SOCKS4):
        protocols.append('socks4')

    elif ProxyEngine.ProxyEngine.checkProtocolExistence(bitmap, ProxyEngine.Protocol.HTTP):
        protocols.append('http')

    elif ProxyEngine.ProxyEngine.checkProtocolExistence(bitmap, ProxyEngine.Protocol.HTTPS):
        protocols.append('https')

    return protocols