---

# Elections Scraper

## Popis

Tento projekt je scraper pre výsledky parlamentných volieb v Českej republike z roku 2017. Skript sťahuje volebné dáta zo zadaného URL a ukladá ich do CSV súboru.

URL by malo odkazovať na konkrétny región (napríklad Brno-město), a skript následne stiahne dáta pre všetky obce v tomto regióne.

## Inštalácia

1. **Vytvorte virtuálne prostredie**:

    Na Windows:
    python -m venv venv
    .\venv\Scripts\Activate
    ```

    Na MacOS/Linux:
    python3 -m venv venv
    source venv/bin/activate
    ```

2. **Inštalácia požadovaných knižníc**:

   pip install -r requirements.txt
   ```

## Spustenie

Na spustenie programu sú potrebné dva argumenty:
1. URL volebného regiónu (nájdete kliknutím na "X" v stĺpci "Výběr obce").
2. Názov výstupného súboru (napríklad "Praha"). Prípona `.csv` sa pridá automaticky.

### Príklad na spustenie pre jedno miesto:

Na Windows (PowerShell):
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6202" "brno"
```

Na MacOS/Linux (Bash):
python3 main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6202" "brno"
```

### Príklad na spustenie pre viacero miest naraz (Brno a Praha):

Na Windows (PowerShell):
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6202" "brno" "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" "praha"
```

Na MacOS/Linux (Bash):
python3 main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6202" "brno" "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" "praha"
```

### Vysvetlenie:
Skript stiahne a spracuje volebné údaje pre oba regióny a uloží ich do samostatných súborov `brno.csv` a `praha.csv`.

## Príklad výstupu

Výstupný CSV súbor bude obsahovať nasledujúce stĺpce:

- Kód obce
- Názov obce
- Registrovaní voliči
- Vydané obálky
- Platné hlasy
- Počet hlasov pre každú politickú stranu

## Kód

Tu je stručný prehľad toho, čo robí jednotlivá časť kódu:

### Kontrola vstupov (input_check):
- Overuje, či bol zadaný správny počet argumentov.
- Ak výstupný súbor už existuje, vyžaduje potvrdenie od používateľa na jeho prepísanie.

### Sťahovanie a parsovanie HTML (get_response, parse_response):
- Sťahuje HTML obsah zadaného URL.
- Parsuje HTML obsah pomocou BeautifulSoup.

### Funkcie na extrakciu dát:
- **get_table_row**: Extrahuje riadky z HTML tabuľky.
- **get_number_of_city**: Extrahuje kódy obcí.
- **get_name_of_city**: Extrahuje názvy obcí.
- **get_urls**: Extrahuje URL pre detailné výsledky.
- **get_url_to_process**: Konštruuje úplné URL na spracovanie.
- **process_url**: Paralelne spracováva URL na stiahnutie a parsovanie dát.
- **get_voters_count**: Extrahuje počet registrovaných voličov.
- **get_envelopes**: Extrahuje počet vydaných obálok.
- **get_valid_votes**: Extrahuje počet platných hlasov.
- **get_all_votes_for_each_party**: Extrahuje počet hlasov pre každú stranu.
- **get_political_parties_names**: Extrahuje názvy politických strán.

### Hlavná funkcia (main):
- Koordinuje vykonanie všetkých funkcií.
- Zhromažďuje všetky extrahované dáta do jednej štruktúry.
- Vráti dáta pripravené na zápis do CSV súboru.

### Zápis do CSV (to_csv):
- Zapíše zhromaždené dáta do zadaného CSV súboru.

### Logging:
- Obsahuje detailné logovanie pomocou logging knižnice, čo umožňuje lepšie sledovanie priebehu a diagnostiku.

### Multi-threading:
- Používa ThreadPoolExecutor na spracovanie viacerých URL súčasne, čo urýchľuje celý proces.

### Viaceré URL a súbory:
- Riešenie umožňuje zadávať viacero URL a názvov súborov naraz, pričom pre každý pár sa vytvorí samostatný CSV súbor.

### Detailná kontrola vstupov:
- Zahŕňa detailnú kontrolu vstupov, aby sa zabezpečilo, že používateľ zadal správny počet argumentov a že argumenty majú platnú URL.

VSTUP A VYSTUP : 
PS C:\Users\HAWKp\OneDrive\Desktop\Engeto_Elections_Scraper-master> python main.py  "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2110"  "Praha"
>> 
2024-05-15 21:27:31,008 - INFO - Spúšťanie kontroly vstupov...
2024-05-15 21:27:31,009 - INFO - Program beží... Môže to chvíľu trvať...
Počkajte na potvrdenie.
2024-05-15 21:27:31,009 - INFO - Parsovanie hlavnej stránky: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2110
2024-05-15 21:27:31,555 - INFO - Spracovanie URL adries...
2024-05-15 21:28:06,306 - INFO - Program úspešne dokončený.
Váš výstupný súbor: Praha.csv bol vytvorený
2024-05-15 21:28:06,307 - INFO - Všetky dáta boli úspešne zozbierané.

