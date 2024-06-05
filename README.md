<h1 align="center">
  <br>
  <b>Electoral Analysis Platform</b>
  <br>
</h1>

<p align="center">
  The portal where the information is obtained is: <a href="https://prep2024.ine.mx/publicacion/nacional/presidencia/nacional/candidatura">PREP 2024 by INE</a>.
  <br>
</p>

This project involves developing a web scraper tailored for extracting information from the Programa de Resultados Electorales Preliminares 2024 (PREP) for the Federal Elections in Mexico (https://prep2024.ine.mx/publicacion/nacional/presidencia/nacional/candidatura). The purpose is to gather and process data to understand electoral trends and outcomes.

## Objective

The objective of this project is purely academic and has no commercial purpose. It is carried out with the intention of learning and practicing web scraping techniques. The aim is to aggregate the information to make it freely accessible for academic and research purposes.

## Description

The Programa de Resultados Electorales Preliminares (PREP) collects and disseminates preliminary electoral results for the Federal Elections in Mexico. This information includes data on votes counted, candidate performance, and overall election trends, helping to provide a snapshot of the election outcomes shortly after the polls close.

Results are collected in real-time from various polling stations across the country and are updated continuously to reflect the most current data available. The results displayed include the time they were reported; however, they are preliminary and subject to official validation. Therefore, they should be considered provisional until the final count is confirmed.

## Description

The Preliminary Electoral Results Program (PREP) begins publishing results on June 2 at 8:00 PM Central Time (UTC-6). These results are preliminary, for informational purposes only, and not legally binding.

On June 5, 2024, the District Counts commence, finalizing the electoral results for each of the 300 districts in the country.

This information is provided by Mexico's National Electoral Institute (INE).

## Technologies Used
![Python](https://img.shields.io/badge/Python-3.x-blue) 

The project is based on the following technologies:

- **Selenium**: Selenium is used to automate web navigation and extract information from the pages.
- **Python 3**: The primary programming language used in the development of the scraper. 
- **Web Scraping**: Web scraping techniques are employed to obtain data from web pages in an automated manner.

## Setting up the Virtual Environment and Installing Dependencies

Below are the steps to create a Python virtual environment and install the necessary dependencies:

1. **Clone the Repository:** Clone this repository to your local machine using the following command:
    ```
    git clone git@github.com:Anonymate054/PREP2024.git
    cd PREP2024
    ```

2. **Create a Virtual Environment:** Navigate to the project directory and create a virtual environment using the following command:
    ```
    python3 -m venv venv
    ```

3. **Activate the Virtual Environment:** Activate the virtual environment with the following command:
    - On Windows:
    ```
    venv\Scripts\activate
    ```
    - On macOS and Linux:
    ```
    source venv/bin/activate
    ```

4. **Install Dependencies:** Once the virtual environment is activated, install the project dependencies by running the following command:
    ```
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

5. **Get Drivers:** Download drivers by run following command:
    ```
    chmod +x get_drivers.sh
    sudo ./get_drivers.sh
    ```

6. **Run Notebooks:** Run pythons notebooks scripts.

With these steps, you will have successfully set up the virtual environment and installed all the necessary dependencies to run the scraper.

## Usage

To use the scraper, simply run the main script and follow the instructions provided in the code.