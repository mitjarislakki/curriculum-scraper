# Simple webscraper for Curricula from Aalto University

```python
pip3 install requests beautifulsoup4 pyyaml
```

Current usage:
- Replace `url` in [scraper.py](./scraper.py) with a link in the format:
    - EN: `https://www.aalto.fi/en/programmes/<programme>/curriculum-<start-year>-<end-year>`
    - FI: `https://www.aalto.fi/fi/ohjelmat/<programme>/opetussuunnitelma-<start-year>-<end-year>`

(note that there is no check for it currently)