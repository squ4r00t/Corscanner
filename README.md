## Corscanner
___
This tool helps you identify CORS misconfiguration in a website.

### Installation
___

```bash
git clone https://github.com/squ4r00t/Corscanner.git
cd Corscanner
python3 main.py -h
```

### Usage
___

**Basic Usage**
```bash
python3 main.py --url https://example.com/vulnerable/endpoint
```

If you know a valid origin that is accepted by the application you're testing, you can pass it to the tool with the `--valid-origin` parameter

> When using `--valid-origin`, provide the domain name without the scheme (http, https)

**With valid origin**
```bash
python3 main.py --url https://example.com/vulnerable/endpoint --valid-origin www.example.com
```

If you want to test multiple urls, you can give the tool the path to the file containing the list of urls through the `--file` parameter.

In this case, if you want to also provide a valid origin for each url, do it appending to each of them a comma (,) and the valid origin. Like this

```text
https://site1.com/vulnerable/endpoint,site1.com
https://site2.com/another/endpoint,www.site2.com
```

**Using a list of urls**
```bash
python3 main.py --file /opt/urls.txt
```
