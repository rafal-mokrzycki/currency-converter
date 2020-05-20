import requests
from bs4 import BeautifulSoup
URL = 'https://wechselkurse-euro.de/'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
currencies = soup.find_all('td', class_='kurz_kurz')

symbols = []
for title in currencies:
    symbols.append(str(title.get('title'))[-3:])

rates = []
for currency in currencies:
    text = currency.renderContents()
    number = text.strip()
    rates.append(float(number))

rates = dict(zip(symbols, rates))

rates['EUR'] = 1.0


def converter():

    from_currency = input("Type in a symbol of a currency which you want to convert and hit ENTER:\n")
    if from_currency.upper() not in rates:
        print("Wrong currency symbol.")
    else:
        to_currency = input("Type in a symbol of a currency which you want to convert into and hit ENTER:\n")
        if to_currency.upper() not in rates:
            print("Wrong currency symbol.")
        else:
            initial_amount = float(input("Type in an amount that you want to convert and hit ENTER:\n"))
            try:
                aux_currency = float(initial_amount) / (rates[from_currency.upper()])
                end_amount = round(aux_currency * rates[to_currency.upper()], 2)
                print(str(initial_amount) + " " + from_currency.upper() + " = " + str(end_amount) + " " + to_currency.upper())
            except ValueError:
                print("You must type in a number.")
                
converter()