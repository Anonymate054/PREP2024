import os 
import re
import time
import json
import numpy as np
import pandas as pd
import lxml.html as html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.support import expected_conditions as EC

def string_to_array(input_string):
    lines = input_string.split('\n')
    result = []
    for line in lines:
        if line.strip():
            elements = line.split(',')
            for element in elements:
                element = element.strip()
                result.append(element)
    return result

def parse_arr(arr):
    category = arr.pop(0)
    json_data = {}
    json_data['category'] = category.strip()
    json_data['attributes'] = {}
    for i in range(0, len(arr), 2):
        key = arr[i].strip()
        value = arr[i + 1]
        json_data['attributes'][key] = value
    return json_data

def create_json_file(json_data, file_name):
    with open(f'{file_name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)

def append_to_fails(json_data,page):
    try:
        try:
            with open('app/links/fails_page_{}.json'.format(page), 'r') as file:
                fails_data = json.load(file)
        except FileNotFoundError:
            fails_data = []
        fails_data.append(json_data)
        with open('app/links/fails_page_{}.json'.format(page), 'w') as file:
            json.dump(fails_data, file, indent=4)
        print("Data added successfully to fails.json.")
    except Exception as e:
        print(f"Error appending data to fails.json: {e}")

def remove_from_fails_by_id(id_to_remove, page):
    try:
        try:
            with open('app/links/fails_page_{}.json'.format(page), 'r') as file:
                fails_data = json.load(file)
        except FileNotFoundError:
            fails_data = []

        for json_object in fails_data:
            if json_object.get("id") == id_to_remove:
                fails_data.remove(json_object)
                break

        with open('app/links/fails_page_{}.json'.format(page), 'w') as file:
            json.dump(fails_data, file, indent=4)

        print(f"Element with id {id_to_remove} successfully removed from fails_page_{page}.json.")
    except Exception as e:
        print(f"Error removing element from fails_page_{page}.json: {e}")

def create_folder_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"The folder '{folder_name}' has been created.")
    else:
        print(f"The folder '{folder_name}' already exists.")

def parse_election_data(data: str) -> dict:
    # Extract name using regular expression
    name_match = re.search(r'([A-Za-zÁÉÍÓÚáéíóúÑñ\s]+)Total de votos', data)
    name = name_match.group(1).strip() if name_match else ''

    # Extract total votes using regular expression
    total_votes_match = re.search(r'Total de votos([0-9,]+)', data)
    total_votes = int(total_votes_match.group(1).replace(',', '')) if total_votes_match else 0

    # Extract percentage using regular expression
    percent_match = re.search(r'Porcentaje([0-9.]+)\s%', data)
    percent = float(percent_match.group(1).replace(',', '.')) / 100 if percent_match else 0.0

    # Extract votes in territory national using regular expression
    national_votes_match = re.search(r'En Territorio Nacional([0-9,]+)', data)
    national_votes = int(national_votes_match.group(1).replace(',', '')) if national_votes_match else 0

    # Extract votes abroad using regular expression
    abroad_votes_match = re.search(r'En el Extranjero([0-9,]+)', data)
    abroad_votes = int(abroad_votes_match.group(1).replace(',', '')) if abroad_votes_match else 0

    return {
        'name': name,
        'total_votes': total_votes,
        'percent': percent,
        'national_votes': national_votes,
        'abroad_votes': abroad_votes
    }

def parse_to_array(input_string):
    """
    Parses a given string into an array of 19 elements.
    The first element is the text, and the following 18 elements are integers.

    Args:
    input_string (str): The input string to be parsed.

    Returns:
    list: A list with 19 elements, where the first element is a string and the next 18 are integers.
    """
    # Split the input string into parts
    parts = input_string.split()
    
    # Check if the input starts with "Sección"
    if parts[0] == "Sección":
        # Combine "Sección" and the following number
        text = "Sección " + parts[1]
        num_start_index = 2
    else:
        # Identify the position where the numbers start
        for i in range(len(parts)):
            try:
                # Try converting the part to an integer (after removing commas)
                int(parts[i].replace(',', ''))
                num_start_index = i
                break
            except ValueError:
                continue
        if num_start_index is None:
            raise ValueError("No numerical elements found in the input string.")
        # The text is everything before the first number
        text = ' '.join(parts[:num_start_index])
    
    # The remaining parts should be converted to integers
    numbers = [int(part.replace(',', '')) for part in parts[num_start_index:]]
    
    # Ensure that we have exactly 18 numbers in the result
    if len(numbers) != 18:
        raise ValueError("The input string does not contain the correct number of numerical elements.")

    # Combine the text and the numbers into a single list
    result = [text] + numbers

    return result

def parse_votes_and_percentages(input_string):
    """
    Parse the input string to extract total votes and percentages into a dictionary.

    Args:
        input_string (str): The input string containing vote and percentage data.

    Returns:
        dict: A dictionary with parsed data.
    """
    result = {}
    
    # Regular expression to match "Total de votos" followed by number and "Porcentaje" followed by percentage
    pattern = re.compile(r"Total de votos\s+([\d,]+)\s+Porcentaje\s+([\d.]+)%")
    
    # Find all matches in the input string
    matches = pattern.findall(input_string)
    keys = ['PAN', 'PRI', 'PRD', 'V', 'PT', 'MC', 'M', 'PA+PRI+PRD', 'PAN+PRI', 'PAN+PRD', 'PRI+PRD', 'V+PT+M', 'V+PT', 'V+M', 'PT+M']

    # Iterate over matches and construct the dictionary
    for i, (votes, percentage) in enumerate(matches, 1):
        key = keys[i-1]
        result[key] = {
            'Total votes': int(votes.replace(',', '')),
            'Percentage': f"{float(percentage) / 100:.6f}"
        }
    
    return result

def json_to_dataframe(votes_json):
    """
    Converts a JSON object containing vote data into a pandas DataFrame.

    Args:
        votes_json (dict): JSON object with vote data.

    Returns:
        pd.DataFrame: DataFrame with the vote data.
    """
    # Convert the JSON object to a DataFrame
    df = pd.DataFrame.from_dict(votes_json, orient='index')
    
    # Convert the 'Percentage' column to float
    df['Percentage'] = df['Percentage'].astype(float)
    df.columns = ['Total de votos', 'Porcentaje']
    
    return df

def json_states_to_pandas(json_data):
    """
    Converts a JSON object containing state vote data into a pandas DataFrame.

    Args:
        json_data (dict): JSON object with state vote data.

    Returns:
        pd.DataFrame: DataFrame with the combined vote data.
    """
    data = []

    for state, candidates in json_data.items():
        for candidate_id, candidate_info in candidates.items():
            row = {
                'State': state,
                'Candidate ID': candidate_id,
                'Name': candidate_info['name'],
                'Total Votes': candidate_info['total_votes'],
                'Percentage': candidate_info['percent'],
                'National Votes': candidate_info['national_votes'],
                'Abroad Votes': candidate_info['abroad_votes']
            }
            data.append(row)
    
    df = pd.DataFrame(data)
    return df

def get_info_district_votes_in_CR(driver):
    headers = ['Sección', 'PAN', 'PRI', 'PRD', 'V', 'PT', 'MC', 'M', 'PA+PRI+PRD', 'PAN+PRI', 'PAN+PRD', 'PRI+PRD', 'V+PT+M', 'V+PT', 'V+M', 'PT+M', 'Candidaturas no registradas', 'Votos nulos', 'Total']
    list_elemnts = driver.find_elements(By.TAG_NAME, "tr")
    new_list = [elemnent.text for elemnent in list_elemnts]
    new_list.pop(0)
    rows = [parse_to_array(elem) for elem in new_list]
    df = pd.DataFrame(rows, columns=headers)
    time.sleep(5)
    # driver.close() # Revisar
    return df

def get_info_district_section(driver):
    contenedor = driver.find_element(By.XPATH, "/html/body/app-root/app-federal/div/div/div[3]/app-secciones/div/div[1]/div[2]/app-votos-partido/div[2]")
    lista_elementos = contenedor.find_elements(By.TAG_NAME, "div")
    first = lista_elementos.pop(0)
    result = parse_votes_and_percentages(first.get_attribute('textContent'))
    return result

def get_districts_list(driver,XPATH):
    dropdown = Select(driver.find_element(By.XPATH,XPATH))
    district = [option.text for option in dropdown.options]
    district.pop(0)
    return district

def get_states_list(driver,XPATH):
    dropdown = Select(driver.find_element(By.XPATH,XPATH))
    states = [option.text for option in dropdown.options]
    states.pop(0)
    return states

def get_states_json(state_list):
    return {index: state for index, state in enumerate(state_list)}

def get_states_districs_json(states_dict, XPATH, url, s, chrome_options):
    states_districs = {}
    for index, state_name in enumerate(states_dict.values()):
        print(f'Scrapping {state_name} with id {index+1} and url = {url.format(state=index+1)}')
        with webdriver.Chrome(service=s, options=chrome_options) as driver:
            driver.get(url.format(state=index+1))
            driver.maximize_window()
            states_districs[state_name] = get_districts_list(driver,XPATH)
            driver.close()
    return states_districs

# if __name__ == "__main__":
# 	run()