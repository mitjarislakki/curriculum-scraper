"""
The MIT License

Copyright 2025 Mitja Rislakki

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import requests
from bs4 import BeautifulSoup
import yaml
import argparse
import unicodedata

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Aalto Curriculum Scraper',
                                   description='Scrapes course information from the given Aalto curriculum URL')
    parser.add_argument('-u', "--url", required=True, action='store')
    parser.add_argument('-o', "--out", action='store', default='programmes.yaml')
    parser.add_argument('-nc',"--no-code", action='store_false')
    parser.add_argument('-nn',"--no-name", action='store_false')
    parser.add_argument('-ne',"--no-ects", action='store_false')
    parser.add_argument('-np',"--no-period", action='store_false')

    args = parser.parse_args()
    url = args.url
    conditions = {
        "code": args.no_code,
        "name": args.no_name,
        "ECTS": args.no_ects,
        "period": args.no_period
    }

    # Fetch HTML
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Dict for the data
    programmes = {}

    # Find all h2 elements (contains all program names, but also fluff)
    for h2 in soup.find_all("h2"):
        program_name = h2.get_text(strip=True)
        # print(program_name)

        # Next div should be the container for the programme, containg all dropdowns (majors, study tracks)
        next_div = h2.find_next_sibling("div", class_="listing-accordion__container")

        if next_div:
            for h3 in next_div.find_all("h3"): # For all H3 in the div
                track_name = h3.get_text(strip=True)
                b = h3.find("button")
                container_id = b.get("id") if b else None # Find id of the button associated with the H3
                # Matching the div containing the table with the id
                table_div = None if not container_id else h3.find_next_sibling("div", {"aria-labelledby" : container_id})
                if table_div:
                    courses = []
                    # Find all table elements from this div that aren't colspan. Assumes table always has 4 columns
                    for row in table_div.select("tbody tr"):
                        cols = row.find_all("td")
                        if cols and "colspan" not in cols[0].attrs:
                            course_name = cols[0].text.strip()
                            courses.append({
                                key: value
                                for key, value in
                                    {
                                    "code": cols[0].text.strip(),
                                    "name": cols[1].text.strip(),
                                    "ECTS": cols[2].text.strip(),
                                    "period": cols[3].text.strip()
                                    }.items()
                                if conditions.get(key, False)
                            })

                    # Add to the dict
                    if(track_name and len(courses)>0):
                        if program_name not in programmes:
                            programmes[program_name] = [] # List created for key
                        # Major and its courses added as list element
                        programmes[program_name].append({
                            "major": track_name,
                            "courses": courses
                    })

    # Convert to YAML
    yaml_output = yaml.dump(programmes, default_flow_style=False, sort_keys=False, allow_unicode=False)

    # TODO: clean the random Unicode
    # for char in yaml_output:
    #     if ord(char) > 127:  # Non-ASCII characters
    #         print(f"Found Unicode {char} (U+{ord(char):04X})")
    # yaml_output = yaml_output.replace("\u2010", "-")
    # yaml_output = unicodedata.normalize('NFKD', yaml_output)

    # Save to a file
    with open(args.out, "w", encoding='utf-8') as file:
        file.write(yaml_output)

    print(f"Scraped course codes saved to {args.out}")
