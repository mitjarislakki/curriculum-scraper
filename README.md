# Simple webscraper for Curricula from Aalto University

```python
pip3 install requests beautifulsoup4 pyyaml
```

Usage:

```
python3 scraper.py --url <url> --out <filename> (-nc -nn -ne -np)
```

- `url` should follow the format (no check for it currently):
    - EN: `https://www.aalto.fi/en/programmes/<programme>/curriculum-<start-year>-<end-year>`
    - FI: `https://www.aalto.fi/fi/ohjelmat/<programme>/opetussuunnitelma-<start-year>-<end-year>`
- filename does not add a file extension automatically
- nc, nn, ne, np disable course code, name, credits and period respectively