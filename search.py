#Sandra Wang 14772372
import json
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

_REFERER = 'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/sandrw2'

def _expected_search(data:[{}])-> bool:
    '''
    checks if data we found from searching is the data we expected
    returns True if it can successfully do the following actions
    else returns False
    '''
    try:
        dictionary = data[0]
        longitude = float(dictionary['lat'])
        lattitude = float(dictionary['lon'])
        return True
    except TypeError:
        return False
    except KeyError:
        return False
    except IndexError:
        return False
    except ValueError:
        return False

class Error(Exception):
    pass

class OnlineSearch:
    
    def __init__(self, location:str):
        self._location = location

    def search_geo(self):
        '''
        Sends request to nominatim and retrieves data
        if it fails to do so, it catches the exceptions and
        prints out the corresponding error message 
        '''
        url = self._create_url(self._location)
        response = None
        try:
            request = urllib.request.Request(url,headers = {'Referer': _REFERER}) 
            response = urllib.request.urlopen(request)
            json_text = response.read().decode(encoding = 'utf-8')
            data = json.loads(json_text)
            
            if _expected_search(data):
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

            
    def _create_url(self, location: str)-> str:
        '''
        given a location string, it parses the string and combines it with
        base url. Finally, returns the new URL
        '''
        place = [('q', location),('format','json')]
        location = urllib.parse.urlencode(place)
        url  =  'https://nominatim.openstreetmap.org/search?' + location
        return url

class FileSearch:
    def __init__(self, path:'path'):
        self._path = path

    def search_geo(self):
        '''
        searches the file with path object then retrieve data.
        If file can not be found, opened, or is in the wrong format
        then it catches the exception and prints out corresponding
        error message.
        '''
        the_file = None
        try:
            the_file = open(Path(self._path), 'r')
            the_string = the_file.read()
            data = json.loads(the_string)
            

            if _expected_search(data):
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

    
