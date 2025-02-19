import requests
from bs4 import BeautifulSoup
import yaml

# Page URL
url = "https://www.aalto.fi/en/programmes/masters-programme-in-computer-communication-and-information-sciences/curriculum-2024-2026"

if __name__ == "__main__":
    # Fetch HTML
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Dict for the data
    programs = {}

    # Find all h2 elements (contains all program names, but also fluff)
    for h2 in soup.find_all("h2"):
        program_name = h2.get_text(strip=True)
        print(program_name)

        # Next div should be the container for the programme, containg all dropdowns (majors, study tracks)
        next_div = h2.find_next_sibling("div", class_="listing-accordion__container")

        if next_div:
            for h3 in next_div.find_all("h3"): # For all H3 in the div
                track_name = h3.get_text(strip=True)
                b = h3.find("button")
                container_id = b.get("id") if b else None # Find id of the button associated with the H3
                # Matching the div containing the table with the id
                table_div = h3.find_next_sibling("div", {"aria-labelledby" : container_id})
                if table_div:
                    courses = []
                    # Find all table elements from this div that aren't colspan. Assumes table always has 4 columns
                    for row in table_div.select("tbody tr"):
                        cols = row.find_all("td")
                        if cols and "colspan" not in cols[0].attrs:
                            course_name = cols[0].text.strip()
                            courses.append({
                                "code": cols[0].text.strip(),
                                "name": cols[1].text.strip(),
                                "ECTS": cols[2].text.strip(),
                                "period": cols[3].text.strip()
                            })

                    # Add to the dict
                    if(track_name and len(courses)>0):
                        if program_name not in programs:
                            programs[program_name] = [] # List created for key
                        # Major and its courses added as list element
                        programs[program_name].append({
                            "major": track_name,
                            "courses": courses
                    })

    # Convert to YAML
    yaml_output = yaml.dump({"programs": programs}, default_flow_style=False, sort_keys=False)

    # Print YAML
    print(yaml_output)

    # Save to a file
    with open("programs.yaml", "w") as file:
        file.write(yaml_output)

    print("Scraped course codes saved to programs.yaml")
