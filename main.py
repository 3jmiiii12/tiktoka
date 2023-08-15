import os
import requests
import colorama
from colorama import Fore
from itertools import cycle
import random
import string
import time

# Initialize colorama
colorama.init()

# Define the header text
header_text = """
\033[36m
//   █████╗      ██╗███╗   ███╗██╗
//  ██╔══██╗     ██║████╗ ████║██║
//  ███████║     ██║██╔████╔██║██║
//  ██╔══██║██   ██║██║╚██╔╝██║██║
//  ██║  ██║╚█████╔╝██║ ╚═╝ ██║██║
//  ╚═╝  ╚═╝ ╚════╝ ╚═╝     ╚═╝╚═╝
//                                
-  By ALAJMI
- My Instagram : @05zs
-    My TikTok : @.ldd
\033[0m
"""

TELEGRAM_BOT_TOKEN = input("Enter your Telegram Bot Token: ")
TELEGRAM_CHAT_ID = input("Enter your Telegram Chat ID: ")

def fetch_proxies_from_url():
    urls = [
        "https://www.proxyscan.io/download?type=http",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    ]

    proxies = []
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                proxies.extend(response.text.splitlines())
            else:
                print(Fore.YELLOW + f"Failed to fetch proxies from {url} (Status code: {response.status_code})" + Fore.RESET)
        except requests.exceptions.RequestException as e:
            print(Fore.YELLOW + f"Failed to fetch proxies from {url} (Error: {str(e)})" + Fore.RESET)

    return proxies

def generate_random_email(length):
    random_part = ''.join(random.choices(string.ascii_lowercase, k=length))
    email = f"{random_part}@gmail.com"
    return email

def check_single_email(email):
    # Check the first URL
    first_url = f"https://website.3d5x.repl.co/tiktok/?email={email}"
    first_response = requests.get(first_url)

    if first_response.status_code == 200:
        # If status code is 200, check the second URL
        second_url = f"https://email.sajadmonther.repl.co/Email/Check/?email={email}"
        second_response = requests.get(second_url)

        try:
            email_response = second_response.json()

            if email_response.get('message') == 'Available':
                # Email is available (good)
                print(Fore.GREEN + email + " 😈 !" + Fore.RESET)
                send_telegram_message(f"NEW HIT {email} 😈 !")
                save_good_emails_to_file(email)
                return True
            else:
                # Email is not available (bad)
                print(Fore.RED + email + Fore.RESET)
        except requests.exceptions.JSONDecodeError as e:
            # Invalid JSON response from the second URL
            print(Fore.RED + email + Fore.RESET)
    else:
        # Invalid response from the first URL
        print(Fore.RED + email + Fore.RESET)

    return False

def check_list_email(email_list, proxies=None):
    if proxies:
        proxy_cycle = cycle(proxies)
        for email in email_list:
            proxy = next(proxy_cycle)
            proxy_dict = {"http": f"http://{proxy}"}
            check_single_email_with_proxy(email, proxy_dict)
    else:
        for email in email_list:
            check_single_email(email)

def check_single_email_with_proxy(email, proxy_dict):
    # Check the first URL using the proxy
    first_url = f"https://website.3d5x.repl.co/tiktok/?email={email}"
    try:
        first_response = requests.get(first_url, proxies=proxy_dict, timeout=10)

        if first_response.status_code == 200:
            # If status code is 200, check the second URL using the proxy
            second_url = f"https://email.sajadmonther.repl.co/Email/Check/?email={email}"
            second_response = requests.get(second_url, proxies=proxy_dict, timeout=10)
            email_response = second_response.json()

            if email_response.get('message') == 'Available':
                # Email is available (good)
                print(Fore.GREEN + email + " 😈 !" + Fore.RESET)
                send_telegram_message(f"NEW HIT {email} 😈 !")
                save_good_emails_to_file(email)
            else:
                # Email is not available (bad)
                print(Fore.RED + email + Fore.RESET)
        else:
            # Invalid response from the first URL
            print(Fore.RED + email + Fore.RESET)
    except Exception as e:
        print(Fore.RED + email + Fore.RESET + f" (Error: {str(e)})")

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        params = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        requests.get(url, params=params)
    except Exception as e:
        print(f"Failed to send Telegram message: {str(e)}")

def save_good_emails_to_file(email):
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    file_path = os.path.join(desktop_path, 'good_emails.txt')
    with open(file_path, 'a') as f:
        f.write(email + '\n')

def check_emails_by_length(email_length, total_emails, proxies=None):
    proxy_cycle = cycle(proxies) if proxies else None

    for i in range(total_emails):
        email = generate_random_email(email_length)
        proxy_dict = {"http": f"http://{next(proxy_cycle)}"} if proxies else None
        check_single_email_with_proxy(email, proxy_dict)

    print("\nFinished generating and checking emails.")
    print("Good emails saved as they are found.")

def main():
    # Print the header text in cyan color
    print(header_text)

    print("Options:")
    print("1 - Check Single Email")
    print("2 - Check List")
    print("3 - Create Emails and Check")

    option = input("Select an option (1, 2, or 3): ")

    if option == "1":
        email = input("Enter the email to check: ")
        check_single_email(email)
    elif option == "2":
        email_list_file = input("Enter the location of the email list: ")

        use_proxies_choice = input("Do you want to use proxies from URL or from a file? (url/file): ")
        use_proxies = use_proxies_choice.lower() == "url"

        proxies = None
        if use_proxies:
            while True:
                proxies = fetch_proxies_from_url()
                if proxies:
                    break
                else:
                    print(Fore.YELLOW + "Failed to fetch proxies. Retrying in 5 seconds..." + Fore.RESET)
                    time.sleep(5)
        else:
            proxy_file = input("Enter the location of the proxy list: ")
            proxies = read_proxy_list(proxy_file)

        try:
            # Open the file and read each email
            with open(email_list_file, 'r') as f:
                emails = f.read().splitlines()

            # Check the email list
            check_list_email(emails, proxies=proxies)

            print("\nFinished checking the email list.")
            print("Good emails saved as they are found.")

        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    elif option == "3":
        email_length = int(input("Enter the length of the email addresses to generate: "))
        total_emails = int(input("Enter the number of emails to generate and check: "))

        use_proxies_choice = input("Do you want to use proxies from URL or from a file? (url/file): ")
        use_proxies = use_proxies_choice.lower() == "url"

        proxies = None
        if use_proxies:
            while True:
                proxies = fetch_proxies_from_url()
                if proxies:
                    break
                else:
                    print(Fore.YELLOW + "Failed to fetch proxies. Retrying in 5 seconds..." + Fore.RESET)
                    time.sleep(5)
        else:
            proxy_file = input("Enter the location of the proxy list: ")
            proxies = read_proxy_list(proxy_file)

        check_emails_by_length(email_length, total_emails, proxies=proxies)

    else:
        print("Invalid option selected.")

if __name__ == "__main__":
    main()
