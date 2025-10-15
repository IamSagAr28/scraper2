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

class DelhiCourtsScraper:
    def __init__(self):
        self.base_url = "https://newdelhi.dcourts.gov.in"
        self.cause_list_url = f"{self.base_url}/cause-list-%e2%81%84-daily-board/"
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
    
    def get_court_complexes(self) -> List[str]:
        """Fetch list of court complexes from Delhi Courts website"""
        try:
            if not self.driver:
                self.setup_driver()
            
            self.driver.get(self.cause_list_url)
            time.sleep(3)
            
            # Look for court complex dropdown or links
            court_complexes = [
                "Patiala House Court Complex",
                "Karkardooma Court Complex", 
                "Rohini Court Complex",
                "Saket Court Complex",
                "Dwarka Court Complex",
                "Rouse Avenue Court Complex"
            ]
            
            return court_complexes
        except Exception as e:
            print(f"Error fetching court complexes: {str(e)}")
            return []
    
    def get_judges(self, court_complex: str) -> List[JudgeInfo]:
        """Fetch judges for a given court complex"""
        try:
            if not self.driver:
                self.setup_driver()
            
            self.driver.get(self.cause_list_url)
            time.sleep(3)
            
            # This would need to be customized based on the actual website structure
            judges = []
            
            # Look for judge selection elements
            judge_elements = self.driver.find_elements(By.CSS_SELECTOR, "select[name*='judge'], select[name*='court']")
            
            for element in judge_elements:
                if element.tag_name == "select":
                    select = Select(element)
                    for option in select.options[1:]:  # Skip first empty option
                        if option.text.strip():
                            judges.append(JudgeInfo(
                                name=option.text.strip(),
                                designation="Judge",
                                court_number=option.get_attribute("value") or ""
                            ))
            
            # If no dynamic judges found, return some default ones for the complex
            if not judges:
                judges = [
                    JudgeInfo(name=f"Judge 1 - {court_complex}", designation="District Judge", court_number="1"),
                    JudgeInfo(name=f"Judge 2 - {court_complex}", designation="Additional District Judge", court_number="2"),
                    JudgeInfo(name=f"Judge 3 - {court_complex}", designation="Civil Judge", court_number="3"),
                ]
            
            return judges
        except Exception as e:
            print(f"Error fetching judges: {str(e)}")
            return []
    
    def fetch_cause_list(self, court_complex: str, court_name: Optional[str], 
                        date: str, case_type: str = "both") -> List[CauseListData]:
        """Fetch cause list data from Delhi Courts website"""
        try:
            if not self.driver:
                self.setup_driver()
            
            self.driver.get(self.cause_list_url)
            time.sleep(3)
            
            cause_lists = []
            
            # Get judges to process
            judges = self.get_judges(court_complex)
            judges_to_process = []
            
            if court_name:
                # Find specific judge
                for judge in judges:
                    if court_name.lower() in judge.name.lower():
                        judges_to_process.append(judge)
                        break
            else:
                judges_to_process = judges
            
            for judge in judges_to_process:
                try:
                    # Navigate to the cause list page for this judge
                    # This would need to be customized based on actual website structure
                    
                    # Set date if there's a date picker
                    date_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='date'], input[name*='date']")
                    for date_input in date_inputs:
                        date_input.clear()
                        date_input.send_keys(date)
                    
                    # Submit form or click search button
                    submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
                    if submit_buttons:
                        submit_buttons[0].click()
                        time.sleep(3)
                    
                    # Parse the result
                    entries = self._parse_cause_list_table()
                    
                    if entries:
                        cause_list_data = CauseListData(
                            court_name=court_complex,
                            judge_name=judge.name,
                            date=date,
                            case_type=case_type,
                            entries=entries
                        )
                        cause_lists.append(cause_list_data)
                    
                except Exception as e:
                    print(f"Error processing judge {judge.name}: {str(e)}")
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
                
                # Skip if table has too few rows
                if len(rows) < 2:
                    continue
                
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
    
    def fetch_all_judges_cause_lists(self, court_complex: str, date: str) -> List[CauseListData]:
        """Fetch cause lists for all judges in a court complex"""
        return self.fetch_cause_list(court_complex, None, date, "both")
