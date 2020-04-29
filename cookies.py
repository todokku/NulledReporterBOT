from json import dump, load
from json.decoder import JSONDecodeError

def getcookies():
    try:
        with open('cookies.json', 'r') as r:
            cookies = load(r)
            if cookies:
                return cookies
    except FileNotFoundError:
        print('cookies.json is not found', end='')
        if input() == '':
            getcookies()
        else:
            pass
    except IndexError:
        print('Text is not in the correct format', end='')
        if input() == '':
            getcookies()
            print()
        else:
            pass
    except JSONDecodeError:
        appendCookies()

def appendCookies():
    cookies = {}
    neededCookiesList = ['nulledsession_id', 'nulledpass_hash', 'nulledmember_id', 'PHPSESSID']

    try:
        with open('cookies.json', 'r') as r:
            text = r.read()[:-2]
            if len(text) > 0:
                cont = True
            else:
                print('cookies.json is empty')
                cont = False

            if cont:
                eachCookie = text.split('; ')

                r.close()
                for c in eachCookie:
                    for nc in neededCookiesList:
                        if nc in c:
                            cookies[nc] = c.split('=')[1]

                with open('cookies.json', 'w') as w:
                    dump(cookies, w, indent=4)

            getcookies()
    except FileNotFoundError:
        print('cookies.json is not found', end='')
        if input() == '':
            appendCookies()
        else:
            pass
    except IndexError:
        print('Text is not in the correct format', end='')
        if input() == '':
            appendCookies()
            print()
        else:
            pass