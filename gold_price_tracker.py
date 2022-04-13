import requests
from bs4 import BeautifulSoup
import smtplib
import ssl
import os
import shutil
import getpass


def add_to_startup():
    user_name = getpass.getuser()
    startup_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % user_name
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = os.path.basename(os.path.realpath(__file__))
    bat_path = dir_path + '\\' + "open.bat"
    with open(bat_path, "w+") as bat_file:
        bat_file.write(f"cd {dir_path} \npython {file_name}")
    shutil.move(bat_path, startup_path)


def send_mail(message, receiver_email):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "mail@gmail.com" #podaj swoj mail
    password = "haslo" #podaj swoje haslo
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def number(word):
    for char in word:
        if char.isdecimal():
            continue
        else:
            word = word.replace(char, "")
    return int(word)


def take_data(search_products):
    data = {}
    web_url = 'https://skup.zlota.pl/ceny-skupu'
    soup = BeautifulSoup(requests.get(web_url).text, "html.parser")
    url_tab = soup.find(id="tabelka").attrs["src"]
    soup_tab = BeautifulSoup(requests.get(url_tab).text, "html.parser")
    list_products = soup_tab.find_all("td", attrs={"class": ("s6", "s7")})
    for product in list_products:
        for search_product in search_products:
            if product.next_element == search_product:
                data[search_product] = number(product.next_sibling.next_element)
    return data


def send_message():
    receiver_email = "mail@gmail.com" #podaj maila do ktorego ma byc wysylana informacja
    search_products = ["Krugerrand 1 uncja", "100 g"]
    search_prices = [7500, 24000]
    data = take_data(search_products)
    for key in data.keys():
        if search_prices[search_products.index(key)] <= data[key]:
            message = f"cena {key} = {data[key]}"
            send_mail(message, receiver_email)


if __name__ == '__main__':
    add_to_startup()
    send_message()