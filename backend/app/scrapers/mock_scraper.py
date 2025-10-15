from typing import List
from app.models.schemas import JudgeInfo, CauseListData, CauseListEntry

class MockScraper:
    """Mock scraper for testing without Chrome driver dependencies"""
    
    def get_states(self) -> List[str]:
        """Return mock list of states"""
        return [
            "Delhi",
            "Maharashtra", 
            "Karnataka",
            "Tamil Nadu",
            "Gujarat",
            "Rajasthan",
            "Uttar Pradesh",
            "West Bengal",
            "Andhra Pradesh",
            "Telangana"
        ]
    
    def get_districts(self, state: str) -> List[str]:
        """Return mock districts for a state"""
        if state.lower() == "delhi":
            return ["Delhi"]
        elif state.lower() == "maharashtra":
            return ["Mumbai", "Pune", "Nagpur", "Nashik"]
        elif state.lower() == "karnataka":
            return ["Bangalore", "Mysore", "Hubli", "Mangalore"]
        else:
            return [f"{state} District 1", f"{state} District 2", f"{state} District 3"]
    
    def get_court_complexes(self, state: str, district: str) -> List[str]:
        """Return mock court complexes"""
        if state.lower() == "delhi":
            return [
                "Patiala House Court Complex",
                "Karkardooma Court Complex", 
                "Rohini Court Complex",
                "Saket Court Complex",
                "Dwarka Court Complex",
                "Rouse Avenue Court Complex"
            ]
        else:
            return [
                f"{district} District Court Complex",
                f"{district} Sessions Court Complex",
                f"{district} Civil Court Complex"
            ]
    
    def get_judges(self, state: str, district: str, court_complex: str) -> List[JudgeInfo]:
        """Return mock judges for a court complex"""
        judges = []
        for i in range(1, 6):  # 5 mock judges
            judges.append(JudgeInfo(
                name=f"Hon'ble Judge {i} - {court_complex}",
                designation="District Judge" if i <= 2 else "Additional District Judge",
                court_number=str(i)
            ))
        return judges
    
    def fetch_cause_list(self, state: str, district: str, court_complex: str, 
                        court_name: str = None, date: str = None, case_type: str = "both") -> List[CauseListData]:
        """Return mock cause list data"""
        
        # Get judges to process
        judges = self.get_judges(state, district, court_complex)
        judges_to_process = []
        
        if court_name:
            # Find specific judge
            for judge in judges:
                if court_name.lower() in judge.name.lower():
                    judges_to_process.append(judge)
                    break
        else:
            judges_to_process = judges
        
        cause_lists = []
        
        for judge in judges_to_process:
            # Create mock cause list entries
            entries = []
            for i in range(1, 11):  # 10 mock cases per judge
                entry = CauseListEntry(
                    sr_no=str(i),
                    case_number=f"CC/{i:03d}/2024",
                    case_title=f"Sample Case {i} vs State",
                    petitioner=f"Petitioner {i}",
                    respondent=f"Respondent {i}",
                    advocate=f"Advocate {i}",
                    case_type="Civil" if i % 2 == 0 else "Criminal",
                    stage="Arguments",
                    purpose="Hearing"
                )
                entries.append(entry)
            
            # Create cause list data
            cause_list_data = CauseListData(
                court_name=court_complex,
                judge_name=judge.name,
                date=date or "2024-10-15",
                case_type=case_type,
                entries=entries
            )
            cause_lists.append(cause_list_data)
        
        return cause_lists
