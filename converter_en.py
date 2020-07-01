from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import re
import os


class Converter:
    URL1 = 'https://wechselkurse-euro.de/'
    page1 = requests.get(URL1)
    soup1 = BeautifulSoup(page1.content, 'html.parser')
    currencies1 = soup1.find_all('td', class_='kurz_skratka')
    currencies2 = soup1.find_all('td', class_='kurz_kurz')

    symbols = []
    for line1 in currencies1:
        text = line1.renderContents()
        number = text.strip()
        symbols.append(number[-7:-4].decode("utf-8"))

    rates = []
    for line2 in currencies2:
        text = line2.renderContents()
        number = text.strip()
        rates.append(float(number))

    currencies = pd.DataFrame(list(zip(symbols, rates)), columns=['currency symbol', 'exchange rate for 1 Euro'])
    currencies = currencies.append({'currency symbol': 'EUR', 'exchange rate for 1 Euro': 1.0}, ignore_index=True)

    URL2 = 'https://www.currencyremitapp.com/world-currency-symbols/'
    page2 = requests.get(URL2)
    soup2 = BeautifulSoup(page2.content, 'html.parser')
    currencies3 = soup2.find_all('td')

    countries = []
    for line in currencies3:
        aux_country = re.findall('<td>.*</td>', str(line), 0)
        aux_country = ''.join(aux_country)
        aux_country = aux_country.replace('</td>',"")
        aux_country = aux_country.replace('<td>',"")
        countries.append(aux_country)
    countries

    country = []
    currency_name = []
    currency_symbol = []

    for enumer in enumerate(countries):
        if (enumer[0] + 4) % 5 == 0:
            country.append(enumer[1])
        elif (enumer[0] + 3) % 5 == 0:
            currency_name.append(enumer[1])
        elif (enumer[0] + 2) % 5 == 0:
            currency_symbol.append(enumer[1])

    countries = pd.DataFrame(data={"country": country,
                                   "currency name": currency_name,
                                   "currency symbol": currency_symbol})
    corrections1 = {
        "AFA": "AFN",
        "AON": "AOA",
        "AZM": "AZN",
        "EEK": "EUR",
        "GHC": "GHS",
        "LTL": "EUR",
        "LVL": "EUR",
        "XDR": "XDR",
        "MZM": "MZN",
        "SDD": "SDG",
        "SRG": "SRD",
        "TMM": "TMT",
        "VEB": "VEF",
        "WN": "KPW",
        "ZWD": "ZWR"
    }

    for i in countries["currency symbol"]:
        for k, v in corrections1.items():
            if k == i:
                countries["currency symbol"].replace(i, v, inplace=True)

    myrates = pd.merge(countries, currencies, how='outer', on='currency symbol')

    corrections2 = [
        ("BMD", "Bermuda", "Bermudian Dollar"),
        ("FKP", "Falkland Islands", "Pound"),
        ("KYD", "Cayman Islands", "Cayman Islands Dollar"),
        ("CUC", "Cuba", "Peso"),
        ("SHP", "Saint Helena", "Saint Helena pound")
    ]

    for i, j in myrates.iterrows():
        for k in corrections2:
            myrates.loc[myrates["currency symbol"] == k[0], ['country', 'currency name']] = k[1], k[2]
            myrates.loc[myrates["currency symbol"] == "EUR", 'currency name'] = "Euro"

    myrates = myrates.dropna()

    def convert(self):

        while True:
            from_currency = (input("Type in a symbol of a currency, which you would like to convert:\n")).upper()
            if from_currency in self.myrates['currency symbol'].unique():
                break
            else:
                print("There in no such a currency in our converter.")
                time.sleep(1)
        while True:
            to_currency = (input("Type in a symbol of a currency, which you would like to convert in:\n")).upper()
            if to_currency in self.myrates['currency symbol'].unique():
                break
            else:
                print("There in no such a currency in our converter.")
                time.sleep(1)
        while True:
            try:
                initial_amount = float(input("Type in an amount:\n"))
                aux_currency = float(initial_amount) / float(
                    self.myrates.loc[self.myrates['currency symbol'] == str(from_currency), 'exchange rate to 1 Euro'].iloc[0])
                end_amount = round(aux_currency * float(
                    self.myrates.loc[self.myrates['currency symbol'] == str(to_currency), 'exchange rate to 1 Euro'].iloc[0]), 2)
                result = str(initial_amount) + " " + from_currency.upper() + " = " + str(
                    end_amount) + " " + to_currency.upper()
                break
            except ValueError:
                print("Type in a number, not a string. Use comma as decimal separator.")
                time.sleep(3)
        return print(result)

    def print_table(self):

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        return print(self.myrates)

    def save_table(self):

        while True:
            try:
                path = input(
                    "Type in directory path, which you want to save the file in or hit 5 and ENTER to go back to the application options.\n")
                if path == '5':
                    break
                else:
                    file = input("Type in file name (without extension):\n")
                    filepath = str(os.path.join(path, file) + '.csv')
                    self.myrates.to_csv(filepath, header=True, index=False, encoding="ISO-8859-2")
                    print("File saved.")
                    time.sleep(1)
                    break
            except FileNotFoundError:
                print("Directory not found.")
                time.sleep(1)


class Communicator():
    clear = lambda: os.system('cls')
    clear()
    print('Welcome to the currency converter!\n')
    time.sleep(1)
    while True:
        try:
            action = int(input("""
Type in a number and hit ENTER:
(1) show currency exchange rates table
(2) convert currency
(3) save currency exchange rates table as .csv file
(4) close application
"""))
            if action == 1:
                Converter().print_table()
            elif action == 2:
                Converter().convert()
            elif action == 3:
                Converter().save_table()
            elif action == 4:
                print("Closing...")
                time.sleep(0.5)
                print("Application closed successfully.")
                time.sleep(1)
                break
            else:
                raise ValueError()
        except ValueError:
            print("Type in a number between 1 and 4.")
            time.sleep(1)