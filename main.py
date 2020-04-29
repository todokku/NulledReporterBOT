from cookies import getcookies
from re import findall
from dlog import dlog
from json import dump, load
from json.decoder import JSONDecodeError
from time import sleep
from sort import sort
import requests

def report():
    users = sort()

    try:
        users = load(open('bannable.json', 'r'))
    except (FileNotFoundError, JSONDecodeError):
        print("Error! 'bannable.json' does not exist or is poorly formated")
        sleep(2)

    for user in users:
        data = 'k=f8905075c7d79df2f68a89a806b9e61a&message=leecher&member_id={}&ctyp=profile&title={}'.format(user['id'], user['name'])
        reportReq = sess.post(
            url='https://www.nulled.to/index.php?app=core&module=reports&rcom=profiles&send=1',
            data=data
        )

        if reportReq.status_code == 200:
            print('Reported: ' + user['name'])

        sleep(10)

def getPages(sectionUrl):
    crackingpage = sess.get(sectionUrl)

    pages = []

    #fc Stands for 'for check'
    fcposts = findall(r'(?<=<a itemprop=\"url\" id=\"tid-link-)(.*)href=\"(.*)\/\" title=\'(.*?)(?=\' class=\'topic_title highlight_unread\'>)', crackingpage.text)
    for post in fcposts:
        postDate = post[2]
        if 'January 2020' in postDate or 'February 2020'in postDate or 'March 2020' in postDate or 'April 2020' in postDate or 'started  Today' in postDate or 'started  Yesterday' in postDate:
            pages.append({'url': post[1], 'name': post[2].split(' - ')[0]})

    return pages

def getData(userblock):
    # Regex pattern declarations
    nr = r'(?<=<span class=\'hide\' itemprop=\"name\">)(.*?)(?=<\/span)'
    pr = "(?<=data-entry-pid=')(.*?)(?=')"
    uidr = r'(?<=href="https:\/\/www\.nulled\.to\/user\/)(.*?)(?=-)'
    tr = '(?<=Threads: <span class=\"ml-auto\">)(.*?)(?=<)'
    postr = '(?<=Posts: <span class=\"ml-auto\">)(.*?)(?=<)'

    # Finding regex pattern in the response
    name = findall(nr, userblock)[0]
    pid = findall(pr, userblock)[0]
    uid = findall(uidr, userblock)[0]
    threads = int(findall(tr, userblock)[0]) + 1
    postr = int(findall(postr, userblock)[0])

    # User is reportable if post/thread ratio is lower than 40
    reportable = True if postr/threads > 40 else False

    userinfo = {'name': name, 'id': uid, 'postid': pid, 'threads': threads, 'posts': postr, 'reportable': reportable}
    return userinfo

def checkPost(page):
    # Seperates html response in blocks, which are easier to manipulate in terms of Regex
    usersBlocks = findall(r'<span class=\'hide\' itemprop="name">[\w\W]*?<div class=\'post_date\'>', page.text)
    usernames = []

    # Appends userinfo to global user list if it's not there
    for userb in usersBlocks:
        userinfo = getData(userb)
        if userinfo['name'] not in usernames:
            users.append(userinfo)
            usernames = [data['name'] for data in users]
    with open('data.json', 'w') as w:
        dump(users, w, indent=4)

def while_loop(url, name):
    print('Checking \'' + name + '\'')
    pagenumber = 1
    # This is to get Status code 200 in the beginning
    parsereq = sess.get('http://1.1.1.1/')
    lbefore = len(users)

    # While loop that is going until it meets code 301 (This appears when page doesn't exist)
    while parsereq.status_code != 301:
        parsereq = sess.get(url=url + str(pagenumber), allow_redirects=False)
        checkPost(parsereq)
        pagenumber+=1
        print('Checking on page ' + str(pagenumber))
        sleep(5)
    
    print('Parsed ' + str(len(users)-lbefore) + ' users\n')
    sleep(2)

if __name__ == '__main__':
    # Try and read the data.json, create new one if it doesn't exist or isn't readable by JSON
    try:
        users = load(open('data.json', 'r'))
    except (FileNotFoundError, JSONDecodeError):
        open('data.json', 'w').close()
        users = []

    # Header, cookie declarations
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36 Edg/81.0.416.64',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'Content-Type': 'application/x-www-form-urlencoded'
    }

    cookies = getcookies()

    sess = requests.Session()
    sess.headers.update(headers)
    sess.cookies.update(cookies)


    print('Select your mode:\n1. Report users\n2. Parse users\n')
    choice = input('> ')

    if choice == '1':
        report()
    elif choice == '2':
        sectionUrl = input('Type URL for the section:\n>> ')

        pages = getPages(sectionUrl)
        print('Parsed ' + str(len(pages)) + ' pages!\n')

        for page in pages:
            while_loop(page['url'] + '/page-', page['name'])