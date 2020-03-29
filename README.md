````
     ██████╗  ██████╗████████╗ ██████╗     ███████╗ ██████╗ █████╗ ███╗   ██╗
    ██╔═══██╗██╔════╝╚══██╔══╝██╔═══██╗    ██╔════╝██╔════╝██╔══██╗████╗  ██║
    ██║   ██║██║        ██║   ██║   ██║    ███████╗██║     ███████║██╔██╗ ██║
    ██║   ██║██║        ██║   ██║   ██║    ╚════██║██║     ██╔══██║██║╚██╗██║
    ╚██████╔╝╚██████╗   ██║   ╚██████╔╝    ███████║╚██████╗██║  ██║██║ ╚████║
     ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝     ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝                                                                         

    [-h]     For help
    [-u]     URL to scan
    [-md]    Max downloads. Default 1000.
    [-far]   Link follow accept rules. Use single quotes.
    
    Example:
    ~:$ python crawler.py -u https://www.comandscan.com -md 5000 -far '(?si)https://www.commandscan.com.*'
    ~:$ 100%|████████████████████████████████████████| 5000/5000 [05:00<05:00, 30954.27it/s]
````

## Interactive Website scanner

### About
OctoScan is a no-frills, command-line website scanner. Essentially, you give it a URL and at least one follow accept rule
and OctoScan will write a report (.xslx) with all the assets it found and some metadata points, such as status code and headers.

### Dependencies
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - to help parse HTML.
- [Requests](https://requests.readthedocs.io/en/master/) - to help with HTTP requests.
- [tqdm](https://github.com/tqdm/tqdm) - easy to use, command-line progress bar maker.
- [XlsxWriter](https://xlsxwriter.readthedocs.io/) - xls(x) file reader/writer.

### Installation and usage
````
:$ git clone git@github.com:j-000/special-octo-scan.git
:S cd special-octo-scan
# Create and activate a virtual environment
(venv) :$ pip install -r reqs.txt
(venv) :$ python crawler.py -u https://www.comandscan.com -md 1000 -far '(?si)https://www.commandscan.com.*'
````

### Features
- [x] Basic website scanner.
- [x] Basic report.
    - Asset inventory
    - Asset metadata (HTTP status code, headers, size)
- [x] Easy to use interface. 

### Future
Possible features to come:
- [ ] WCAG 2.0 checker
- [ ] SEO checker


