"""
projekt_3.py: tretí projekt do Engeto Online Python Akadémie
autor: Peter Dudáš
email: hawk.pe@gmail.com
discord: Hellscythee
"""
import os
import requests
from bs4 import BeautifulSoup
import sys
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Nastavenie základnej konfigurácie logovania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("elections_scraper.log"),
    logging.StreamHandler()
])

def input_check():
    """
    Kontrola vstupných argumentov programu.
    """
    # Kontrola, či bol zadaný aspoň jeden pár URL a názov mesta
    if len(sys.argv) < 3 or len(sys.argv) % 2 != 1:
        logging.error("Požadovaný počet argumentov nebol zadaný alebo nie je správny. Spustite program znova.")
        exit()

    # Kontrola, či každý URL argument obsahuje správnu URL adresu
    for i in range(1, len(sys.argv), 2):
        if "https://volby.cz/pls/ps2017nss/ps32" not in sys.argv[i]:
            logging.error(f"URL parameter na pozícii {i} nie je platný. Zadajte platnú URL. Spustite program znova.")
            exit()

    logging.info("Program beží... Môže to chvíľu trvať...\n"
                 "Počkajte na potvrdenie.")

def get_response(url: str) -> str:
    """
    Získanie dát z URL.
    """
    response = requests.get(url)
    return response

def parse_response(response: str) -> BeautifulSoup:
    """
    Parsovanie HTML odpovede pomocou BeautifulSoup.
    """
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def get_table_row(soup: BeautifulSoup) -> list:
    """
    Získanie riadkov tabuľky z HTML.
    """
    tag_tr = soup.find_all("tr")
    table_row = []
    for table_r in tag_tr:
        table_row.append(table_r.get_text().strip().splitlines())
    return table_row

def get_number_of_city(table_row: list) -> list:
    """
    Získanie čísel miest z riadkov tabuľky.
    """
    city_number_list = []
    for sublist in table_row[2:]:
        if sublist[0] == "-" or sublist[0] == "Obec" or sublist[0] == "číslo":
            continue
        else:
            city_number_list.append(sublist[0])
    return city_number_list

def get_name_of_city(table_row: list) -> list:
    """
    Získanie názvov miest z riadkov tabuľky.
    """
    city_name_list = []
    for sublist in table_row[2:]:
        if sublist[1] == "název" or sublist[1] == "Výběrokrsku" or sublist[1] == "-":
            continue
        else:
            city_name_list.append(sublist[1])
    return city_name_list

def get_urls(soup: BeautifulSoup) -> list:
    """
    Získanie URL adries z HTML kódu.
    """
    tables = soup.find_all('table')
    url_list = []
    for table in tables:
        a_tags = table.find_all("a")
        for tag in a_tags:
            href = tag.get("href")
            if "vyber=" in href and href not in url_list:
                url_list.append(href)
    return url_list

def get_url_to_process(url_list: list) -> list:
    """
    Získanie URL adries na spracovanie.
    """
    url_base = "https://volby.cz/pls/ps2017nss/"
    urls_to_process = []
    for url in url_list:
        whole_url = url_base + url
        urls_to_process.append(whole_url)
    return urls_to_process

def process_url(urls_to_process: list) -> list:
    """
    Spracovanie URL adries pomocou vlákien.
    """
    processed_urls = []
    with ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(parse_response, get_response(url)): url for url in urls_to_process}
        for future in as_completed(future_to_url):
            processed_urls.append(future.result())
    return processed_urls

def get_voters_count(processed_urls: list) -> list:
    """
    Získanie počtu voličov z každého spracovaného URL.
    """
    voters_count = []
    for url in processed_urls:
        voters = url.find("td", {"class": "cislo"}, headers="sa2").get_text()
        voters_count.append(int(voters.replace("\xa0", "")))
    return voters_count

def get_envelopes(processed_urls: list) -> list:
    """
    Získanie počtu obálok z každého spracovaného URL.
    """
    envelopes_count = []
    for envelopes in processed_urls:
        envelope = envelopes.find("td", {"class": "cislo"}, headers="sa3").get_text()
        envelopes_count.append(int(envelope.replace("\xa0", "")))
    return envelopes_count

def get_valid_votes(processed_urls: list) -> list:
    """
    Získanie počtu platných hlasov z každého spracovaného URL.
    """
    valid_votes_count = []
    for votes in processed_urls:
        vote = votes.find("td", {"class": "cislo"}, headers="sa6").get_text()
        valid_votes_count.append(int(vote.replace("\xa0", "")))
    return valid_votes_count

def get_all_votes_for_each_party(processed_urls: list) -> list:
    """
    Získanie počtu hlasov pre každú stranu z každého spracovaného URL.
    """
    all_party_votes = []
    for url in processed_urls:
        votes = url.find_all("td", headers=["t1sb3", "t2sb3"])
        each_party_votes = []
        for vote in votes:
            if vote.get_text().strip() == "-":
                continue
            else:
                each_party_votes.append(vote.get_text().replace("\xa0", ""))
        all_party_votes.append(each_party_votes)
    return all_party_votes

def get_political_parties_names(soup: BeautifulSoup) -> list:
    """
    Získanie názvov politických strán z HTML kódu.
    """
    political_parties = []
    td_tags = soup.find_all("td", {"class": "overflow_name"})
    for tag in td_tags:
        political_parties.append(tag.get_text())
    return political_parties

def main(urls_and_names: list):
    """
    Hlavná funkcia programu.
    """
    logging.info("Spúšťanie kontroly vstupov...")
    input_check()

    for i in range(0, len(urls_and_names), 2):
        url = urls_and_names[i]
        location_name = urls_and_names[i + 1]
        
        logging.info(f"Parsovanie hlavnej stránky: {url}")
        soup = parse_response(get_response(url))
        city_codes = get_number_of_city(get_table_row(soup))
        city_names = get_name_of_city(get_table_row(soup))
        url_list = get_urls(soup)
        urls_to_process = get_url_to_process(url_list)
        logging.info("Spracovanie URL adries...")
        processed_urls = process_url(urls_to_process)
        reg_voters = get_voters_count(processed_urls)
        envelopes = get_envelopes(processed_urls)
        valid_votes = get_valid_votes(processed_urls)
        all_votes = get_all_votes_for_each_party(processed_urls)
        parties = get_political_parties_names(processed_urls[0])

        # Vytvorenie hlavičky CSV súboru s dátami
        header = ["code", "location", "registered voters", "envelopes", "valid votes", *parties]

        # Vytvorenie jedného zoznamu zozbieraných dát
        data = list(zip(city_codes, city_names, reg_voters, envelopes, valid_votes))

        # Pridanie všetkých hlasov do premennej data, vytvorenie zoznamu dát pre CSV
        for j in range(len(data)):
            data[j] = list(data[j]) + all_votes[j]

        filename = f"{location_name}.csv"
        to_csv(filename, {"header": header, "data": data})

    logging.info("Všetky dáta boli úspešne zozbierané.")

def to_csv(filename: str, data):
    """
    Zapísanie dát do CSV súboru.
    """
    try:
        with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(data["header"])
            # Zapísanie riadkov do CSV súboru
            for row in data["data"]:
                writer.writerow(row)

        logging.info(f"Program úspešne dokončený.\nVáš výstupný súbor: {filename} bol vytvorený")

    # Ošetrenie výnimky: PermissionError, môže sa objaviť, keď je súbor otvorený v inom programe
    except PermissionError:
        logging.error("Prístup odmietnutý. Súbor môže byť otvorený v inom programe.\nSkontrolujte a spustite program znova.")
        exit()

if __name__ == '__main__':
    urls_and_names = sys.argv[1:]
    main(urls_and_names)
