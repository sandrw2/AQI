#Sandra Wang 14772372
import json
import urllib.error
import urllib.request
import urllib.parse
from pathlib import Path

_REFERER = 'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/sandrw2'

def _expected_reverse(data:dict):
    '''
    checks if data if in the expected format. Function tries to find display_name
    field. If field does not exist and exceptions occur, function returns False.
    Otherwise, function returns True
    '''
    try:
        
        place = data['display_name']
        return True
    except IndexError:
        return False
    except KeyError:
        return False
    except TypeError:
        return False
    except ValueError:
        return False
    
        
        
class Error(Exception):
    pass

class OnlineReverse:
    def __init__(self, center:(float,float)):
        self._lattitude = center[0]
        self._longitude = center[1]

    def reverse_geo(self):
        '''
        Requests and retrieves information from Nominatim website using the longitude
        and lattiude that was given. If exceptions occur while doing so, function
        catches them and prints corresponding error message. 
        '''
        url = self._create_url(self._lattitude,self._longitude)
        response = None
        try:
            request = urllib.request.Request(url,headers = {'Referer': _REFERER}) 
            response = urllib.request.urlopen(request)
            json_text = response.read().decode(encoding = 'utf-8')
            data = json.loads(json_text)
            
            if _expected_reverse(data):
                return data
            else:
                print('FAILED')
                print(f'{response.status} {url}')
                print('FORMAT')
                raise Error
            
        
        except urllib.error.HTTPError as e:
            print('FAILED')
            print(f'{e.code} {url}')
            print('NOT 200')
            raise Error
        except urllib.error.URLError:
            print('FAILED')
            print(url)
            print('NETWORK')
            raise Error 
        except ValueError:
            print('FAILED')
            print(f'{response.status} {url}')
            print('FORMAT')
            raise Error

        finally:
            if response!= None:
                response.close()


    def _create_url(self,lattitude,  longitude)-> str:
        '''
        Given longitude and lattitude, function parses them and combines
        them with the base ur. Finally, function returns the the new_url
        '''
        place = [('lat', float(lattitude)),('lon',float(longitude)),('format','json')]
        location = urllib.parse.urlencode(place)
        url  =  'https://nominatim.openstreetmap.org/reverse?' + location
        return url




   

class FileReverse:
    def __init__(self,path: 'path'):
        self._path = path
        
    def reverse_geo(self):
        '''
        Using the path attribute, function searches for the file and retrieves
        data from it. If exceptions occur, function cathes them and then
        prints out the corresponding error message 
        '''
        the_file = None
        try:
            the_file = open(Path(self._path), 'r')
            the_string = the_file.read()
            data = json.loads(the_string)
            
            if _expected_reverse(data):
                return data
            else:
                print('FAILED')
                print(self._path)
                print('FORMAT')
                raise Error
        
                
        except FileNotFoundError:
            print('FAILED')
            print(self._path)
            print('MISSING')
            raise Error
        except OSError:
            print('FAILED')
            print(self._path)
            print('MISSING')
            raise Error
        except ValueError:
            print('FAILED')
            print(self._path)
            print('FORMAT')
            raise Error
        finally:
            if the_file != None:
                the_file.close()


