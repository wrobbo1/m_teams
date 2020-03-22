from datetime import datetime
from termcolor import cprint, colored
import colorama
import random


def get_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
        "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
    ]
    u_a = random.choice(user_agents)

    headers = {
        'User-Agent': u_a,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cache-Control': 'max-age=0'
    }

    return headers

class Logger():
    def __init__(self, inc_time=True, name=""):
        self.inc_time = inc_time
        self.name = (f"[{name}]" if name else "")
        colorama.init()

    def __timestamp(self):
        timestamp = str("[" + datetime.now().strftime("%H:%M:%S.%f")[:-3] + "]")
        return timestamp

    def log(self, text):
        if self.inc_time:
            print("{}{} {}".format(self.name,self.__timestamp(), colored(text, "magenta")))
            return
        else:
            print("{} {}".format(self.name,colored(text, "magenta")))
            return

    def success(self, text):
        if self.inc_time:
            print("{}{} {}".format(self.name,self.__timestamp(), colored(text, "green")))
            return
        else:
            print("{} {}".format(self.name,colored(text, "green")))
            return

    def warning(self, text):
        if self.inc_time:
            print("{}{} {}".format(self.name,self.__timestamp(), colored(text, "yellow")))
            return
        else:
            print("{} {}".format(self.name,colored(text, "yellow")))
            return

    def error(self, text):
        if self.inc_time:
            print("{}{} {}".format(self.name,self.__timestamp(), colored(text, "red")))
            return
        else:
            print("{} {}".format(self.name,colored(text, "red")))
            return

    def status(self, text):
        if self.inc_time:
            print("{}{} {}".format(self.name,self.__timestamp(), colored(text, "cyan")))
            return
        else:
            print("{} {}".format(self.name,colored(text, "cyan")))
            return


# Class for managing proxies
class ProxyManager:
    # Give option to include local host in list of proxies
    def __init__(self, uselocalhost=False):
        self.proxies = []
        self.use_localhost = uselocalhost

        # Formats proxies into dict format which requests accepts
        with open('proxies.txt') as f:
            for item in f.read().splitlines():
                if not item == '':
                    split = item.split(":")

                    # Checks for user pass format and formats accordingly
                    if len(split) == 4:
                        proxy_dict = [
                            item, {
                                'http': f'http://{split[2]}:{split[3]}@{split[0]}:{split[1]}',
                                'https': f'https://{split[2]}:{split[3]}@{split[0]}:{split[1]}'
                            }
                        ]
                        # Saves each proxy as a List object with the first element being the proxy and the second
                        # the formatted proxy
                        self.proxies.append(proxy_dict)
                    elif len(split) == 2:
                        proxy_dict = [
                            item, {
                                'http': f'http://{split[0]}:{split[1]}',
                                'https': f'https://{split[0]}:{split[1]}'
                            }
                        ]
                        self.proxies.append(proxy_dict)
                    else:
                        pass

        if self.use_localhost:
            localhost = None
            self.proxies.append(localhost)

    # Returns a proxy, and adds that proxy back to the end of the list so that it is not used again for a period of time
    def get_proxy(self):
        proxy_dict = self.proxies.pop(0)

        if proxy_dict:
            proxy = proxy_dict[1]
        else:
            proxy = proxy_dict
        
        self.proxies.append(proxy_dict)

        return proxy

    # Function to remove a proxy from use in this instance if it is banned/exceptionally slow etc
    def remove_proxy(self, proxy_formatted):
        for i in range(len(self.proxies)):
            if self.proxies[i][1] == proxy_formatted:
                del self.proxies[i]


# Returns the time in a specific format
def get_time():
    curtime = datetime.now().strftime("%d-%B-%Y %H:%M:%S")
    return curtime


# Function which takes a name and a list of keywords and verifies that they are all in the name
# (If a keyword is negative and begins with a - it will check that it is not in the name)
def process_keywords(item_name, keywords):
    for kw in keywords:
        # negative keyword check
        if kw[0] == "-":
            if kw[1:].lower() in item_name.lower():
                return False
        else:
            # checks for keywords using the 'or' format
            if "/" in kw:
                options = kw.split("/")
                found = False
                for option in options:
                    if option in item_name.lower():
                        found = True

                if not found:
                    return False
            # returns False if not in title
            elif kw.lower() not in item_name.lower():
                return False

    return True


# Takes multiple sets of keywords and tests a name against all of them, and returns True if any of the sets
# are all contained within the name
def process_keyword_sets(item_name, keyword_sets):
    for kw_set in keyword_sets:
        check = process_keywords(item_name, kw_set)
        if check:
            return True

    return False
            


