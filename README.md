       _____                                          _  _____                 
      / ____|                                        | |/ ____|                
     | |     ___  _ __ ___  _ __ ___   __ _ _ __   __| | (___   ___ __ _ _ __  
     | |    / _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` |\___ \ / __/ _` | '_ \ 
     | |___| (_) | | | | | | | | | | | (_| | | | | (_| |____) | (_| (_| | | | |
      \_____\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|_____/ \___\__,_|_| |_|                                
    
    [-h]     For help
    [-u]     URL to scan
    [-md]    Max downloads. Default 1000.
    [-far]   Link follow accept rules. User singe quotes.
    
    Example:
    ~:$ python crawler.py -u https://www.comandscan.com -md 5000 -far '(?si)https://www.commandscan.com.*'
    ~:$ 100%|████████████████████████████████████████| 5000/5000 [05:00<05:00, 30954.27it/s]

## Interactive Website scanner

### About
CommandScan is a no-frills, command-line website scanner. Essentially, you give it a URL and at least one follow accept rule
and CommandScan will write a report (.xslx) with all the assets it found and some metadata points, such as status code and headers.

### Dependencies
- BeautifulSoup - to help parse HTML.
- Requests - to help with HTTP requests.
- tqdm - easy to use, command-line progress bar maker.
- XlsxWriter - xls(x) file reader/writer.

### Installation

### Features
- [x] Basic website scanner.
- [x] Basic report.
    - Asset inventory
    - Asset metadata
- [x] Easy to use interface. 

### Future


