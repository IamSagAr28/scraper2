import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from app.models.schemas import CauseListData, CauseListEntry, JudgeInfo

class ECourtsScraper:
    def __init__(self):
        self.base_url = "https://services.ecourts.gov.in/ecourtindia_v6/"
        self.cause_list_url = f"{self.base_url}?p=cause_list/index"
        self.session = requests.Session()
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome driver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        return self.driver
    
    def close_driver(self):
        """Close the Chrome driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def get_states(self) -> List[str]:
        """Fetch list of states from eCourts website"""
        try:
            if not self.driver:
                self.setup_driver()
            
            self.driver.get(self.cause_list_url)
            time.sleep(3)
            
            # Find state dropdown
            state_select = Select(self.driver.find_element(By.ID, "state_code"))
            states = []
            
            for option in state_select.options[1:]:  # Skip first empty option
                if option.text.strip():
                    states.append(option.text.strip())
            
            return states
        except Exception as e:
            print(f"Error fetching states: {str(e)}")
            return []
    
    def get_districts(self, state: str) -> List[str]:
        """Fetch districts for a given state"""
        try:
            if not self.driver:
                self.setup_driver()
            
            self.driver.get(self.cause_list_url)
            time.sleep(3)
            
            # Select state
            state_select = Select(self.driver.find_element(By.ID, "state_code"))
            for option in state_select.options:
                if option.text.strip() == state:
                    state_select.select_by_visible_text(state)
                    break
            
            # Wait for districts to load
            time.sleep(3)
            
            district_select = Select(self.driver.find_element(By.ID, "dist_code"))
            districts = []
            
            for option in district_select.options[1:]:  # Skip first empty option
                if option.text.strip():
                    districts.append(option.text.strip())
            
            return districts
        except Exception as e:
            print(f"Error fetching districts: {str(e)}")
            return []
    
    def get_court_complexes(self, state: str, district: str) -> List[str]:
        """Fetch court complexes for a given state and district"""
        try:
            if not self.driver:
                self.setup_driver()
            
            self.driver.get(self.cause_list_url)
            time.sleep(3)
            
            # Select state
            state_select = Select(self.driver.find_element(By.ID, "state_code"))
            for option in state_select.options:
                if option.text.strip() == state:
                    state_select.select_by_visible_text(state)
                    break
            
            time.sleep(2)
            
            # Select district
            district_select = Select(self.driver.find_element(By.ID, "dist_code"))
            for option in district_select.options:
                if option.text.strip() == district:
                    district_select.select_by_visible_text(district)
                    break
            
            # Wait for court complexes to load
            time.sleep(3)
            
            court_select = Select(self.driver.find_element(By.ID, "court_code"))
            courts = []
            
            for option in court_select.options[1:]:  # Skip first empty option
                if option.text.strip():
                    courts.append(option.text.strip())
            
            return courts
        except Exception as e:
            print(f"Error fetching court complexes: {str(e)}")
            return []
    
    def get_judges(self, state: str, district: str, court_complex: str) -> List[JudgeInfo]:
        """Fetch judges for a given court complex"""
        try:
            if not self.driver:
                self.setup_driver()
            
            self.driver.get(self.cause_list_url)
            time.sleep(3)
            
            # Select state
            state_select = Select(self.driver.find_element(By.ID, "state_code"))
            for option in state_select.options:
                if option.text.strip() == state:
                    state_select.select_by_visible_text(state)
                    break
            
            time.sleep(2)
            
            # Select district
            district_select = Select(self.driver.find_element(By.ID, "dist_code"))
            for option in district_select.options:
                if option.text.strip() == district:
                    district_select.select_by_visible_text(district)
                    break
            
            time.sleep(2)
            
            # Select court complex
            court_select = Select(self.driver.find_element(By.ID, "court_code"))
            for option in court_select.options:
                if option.text.strip() == court_complex:
                    court_select.select_by_visible_text(court_complex)
                    break
            
            # Wait for judges to load
            time.sleep(3)
            
            judge_select = Select(self.driver.find_element(By.ID, "court_name"))
            judges = []
            
            for option in judge_select.options[1:]:  # Skip first empty option
                if option.text.strip():
                    # Parse judge info (usually contains court number, name, and designation)
                    judge_text = option.text.strip()
                    judges.append(JudgeInfo(
                        name=judge_text,
                        designation="Judge",  # Default designation
                        court_number=option.get_attribute("value") or ""
                    ))
            
            return judges
        except Exception as e:
            print(f"Error fetching judges: {str(e)}")
            return []
    
    def fetch_cause_list(self, state: str, district: str, court_complex: str, 
                        court_name: Optional[str], date: str, case_type: str = "both") -> List[CauseListData]:
        """Fetch cause list data from eCourts website"""
        try:
            if not self.driver:
                self.setup_driver()
            
            self.driver.get(self.cause_list_url)
            time.sleep(3)
            
            # Select state
            state_select = Select(self.driver.find_element(By.ID, "state_code"))
            for option in state_select.options:
                if option.text.strip() == state:
                    state_select.select_by_visible_text(state)
                    break
            
            time.sleep(2)
            
            # Select district
            district_select = Select(self.driver.find_element(By.ID, "dist_code"))
            for option in district_select.options:
                if option.text.strip() == district:
                    district_select.select_by_visible_text(district)
                    break
            
            time.sleep(2)
            
            # Select court complex
            court_select = Select(self.driver.find_element(By.ID, "court_code"))
            for option in court_select.options:
                if option.text.strip() == court_complex:
                    court_select.select_by_visible_text(court_complex)
                    break
            
            time.sleep(2)
            
            # Get all judges if no specific court name provided
            judge_select = Select(self.driver.find_element(By.ID, "court_name"))
            judges_to_process = []
            
            if court_name:
                # Find specific judge
                for option in judge_select.options[1:]:
                    if court_name in option.text:
                        judges_to_process.append((option.get_attribute("value"), option.text))
                        break
            else:
                # Get all judges
                for option in judge_select.options[1:]:
                    if option.text.strip():
                        judges_to_process.append((option.get_attribute("value"), option.text))
            
            cause_lists = []
            
            for judge_value, judge_name in judges_to_process:
                try:
                    # Select judge
                    judge_select = Select(self.driver.find_element(By.ID, "court_name"))
                    judge_select.select_by_value(judge_value)
                    
                    # Set date
                    date_input = self.driver.find_element(By.ID, "hearing_date")
                    date_input.clear()
                    date_input.send_keys(date)
                    
                    # Handle captcha (this is a limitation - would need manual intervention or OCR)
                    # For now, we'll skip captcha handling
                    
                    # Try both civil and criminal if case_type is "both"
                    case_types_to_try = []
                    if case_type == "both":
                        case_types_to_try = ["civil", "criminal"]
                    else:
                        case_types_to_try = [case_type]
                    
                    for ct in case_types_to_try:
                        try:
                            # Click appropriate button
                            if ct == "civil":
                                civil_btn = self.driver.find_element(By.NAME, "civil_btn")
                                civil_btn.click()
                            else:
                                criminal_btn = self.driver.find_element(By.NAME, "criminal_btn")
                                criminal_btn.click()
                            
                            time.sleep(3)
                            
                            # Parse the result table
                            entries = self._parse_cause_list_table()
                            
                            if entries:
                                cause_list_data = CauseListData(
                                    court_name=court_complex,
                                    judge_name=judge_name,
                                    date=date,
                                    case_type=ct,
                                    entries=entries
                                )
                                cause_lists.append(cause_list_data)
                            
                            # Go back to form
                            self.driver.back()
                            time.sleep(2)
                            
                        except Exception as e:
                            print(f"Error processing {ct} cases for {judge_name}: {str(e)}")
                            continue
                
                except Exception as e:
                    print(f"Error processing judge {judge_name}: {str(e)}")
                    continue
            
            return cause_lists
            
        except Exception as e:
            print(f"Error fetching cause list: {str(e)}")
            return []
    
    def _parse_cause_list_table(self) -> List[CauseListEntry]:
        """Parse cause list table from the webpage"""
        try:
            # Look for table containing cause list data
            tables = self.driver.find_elements(By.TAG_NAME, "table")
            entries = []
            
            for table in tables:
                rows = table.find_elements(By.TAG_NAME, "tr")
                
                for row in rows[1:]:  # Skip header row
                    cells = row.find_elements(By.TAG_NAME, "td")
                    
                    if len(cells) >= 3:  # Minimum expected columns
                        entry = CauseListEntry(
                            sr_no=cells[0].text.strip() if len(cells) > 0 else "",
                            case_number=cells[1].text.strip() if len(cells) > 1 else "",
                            case_title=cells[2].text.strip() if len(cells) > 2 else "",
                            petitioner=cells[3].text.strip() if len(cells) > 3 else "",
                            respondent=cells[4].text.strip() if len(cells) > 4 else "",
                            advocate=cells[5].text.strip() if len(cells) > 5 else "",
                            case_type=cells[6].text.strip() if len(cells) > 6 else "",
                            stage=cells[7].text.strip() if len(cells) > 7 else "",
                            purpose=cells[8].text.strip() if len(cells) > 8 else ""
                        )
                        entries.append(entry)
            
            return entries
            
        except Exception as e:
            print(f"Error parsing cause list table: {str(e)}")
            return []
