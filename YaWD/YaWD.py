import easywebdav
import base64
import requests 
import sys
import hashlib
from requests.auth import AuthBase
import xml.etree.cElementTree as xml

def convertbytes(value, key='bytes'):
    values = {"bytes": 1,
              "kilo": 2 ** 10,
              "mega": 2 ** 20,
              "giga": 2 ** 30,
              "tera": 2 ** 40}
    return str(int(value) // values[key])

#add PROPPATCH method into exception class
easywebdav.OperationFailed._OPERATIONS.update(dict(PROPPATCH ="change of properties",
                                                   COPY="copy any files"),
                                                   MOVE="move any file")


class YandexAuth(AuthBase):
    def __init__(self, username=None, password=None, token=None):
        if token or (username and password):
            self.username = username
            self.password = password
            self.token = token
        else:
            raise Exception()

    def __call__(self, r):
        if self.token:
            auth = 'OAuth {0}'.format(self.token)
        else:
            b_auth = b'{0}:{1}'.format(self.username, self.password)
            auth = 'Basic {0}'.format(base64.b64encode(b_auth))
        r.headers['Authorization'] = auth
        return r


class YaD(easywebdav.Client):
    def __init__(self, username=None, password=None, token=None):
        self.baseurl = 'https://webdav.yandex.ru'
        self.cwd = '/'
        self.session = requests.session()
        self.session.verify = True
        self.session.stream = True
        self.session.auth = YandexAuth(username, password, token)   
        
    def _disk_size(self, xmlteg, size):
        headers = {'Depth': '0'}
        body = '''
            <D:propfind xmlns:D="DAV:">
              <D:prop>
                <D:{0}/>
              </D:prop>
            </D:propfind>
            '''.format(xmlteg)
        response = self._send('PROPFIND', '/', (207, 301), headers=headers, data=body)

        tree = xml.fromstring(response.content)
        return convertbytes(tree.find('.//{DAV:}%s' % xmlteg).text, size)        
        
    def disk_free(self, size='bytes'):
        #size = "bytes", "kilo", "mega", "giga", "tera"
        return self._disk_size('quota-available-bytes', size)
    
    def disk_busy(self, size='bytes'):
        #size = "bytes", "kilo", "mega", "giga", "tera"
        return self._disk_size('quota-used-bytes', size)
    
    def _publish(self, path, tag1, value=''):
        body = '''
            <propertyupdate xmlns="DAV:">
              <{0}>
                <prop>
                  <public_url xmlns="urn:yandex:disk:meta">{1}</public_url>
                </prop>
              </{0}>
            </propertyupdate>
            '''.format(tag1, value)
        response = self._send('PROPPATCH', path, (207, 301), data=body)
        tree = xml.fromstring(response.content)
        return tree.find(".//{urn:yandex:disk:meta}public_url").text         
    
    def publish(self, path):
        return self._publish(path, 'set', value='true')
    
    def unpublish(self, path):
        return self._publish(path, 'remove') is None
    
    def ispublish(self, path):
        headers = {'Depth': '0'}
        body = '''
            <propfind xmlns="DAV:">
              <prop>
                <public_url xmlns="urn:yandex:disk:meta"/>
              </prop>
            </propfind>
            '''
        response = self._send('PROPFIND', path, (207, 301), headers=headers, data=body)
        tree = xml.fromstring(response.content)
        return tree.find(".//{urn:yandex:disk:meta}public_url").text is None      
    
    def ls(self, remote_path='/'):
        return super(YaD, self).ls(remote_path)

    def _upload(self, fileobj, remote_path):
        headers = {'Etag': hashlib.md5(bytes(fileobj)).hexdigest(),
                   'Sha256': hashlib.sha256(bytes(fileobj)).hexdigest(),
                   'Content-Length': sys.getsizeof(fileobj),}      
        response = self._send('PUT', remote_path, (100, 200, 201, 204),
                              headers=headers, data=fileobj)
        if response.status_code == 100:
            self._send('PUT', remote_path, (200, 201, 204), data=fileobj)
    
    def getlogin(self):
        #if you use OAuth
        response = self._send('GET', "/?userinfo", (200, 301))
        return response.headers.get('login')
    
    def copy(self, from_, to):
        headers = {'Destination': to}
        self._send('COPY', from_, 201, headers=headers)
        
    def move(self, from_, to):
        headers = {'Destination': to}
        self._send('MOVE', from_, 201, headers=headers)        
