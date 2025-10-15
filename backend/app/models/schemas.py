from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class CauseListRequest(BaseModel):
    state: str
    district: str
    court_complex: str
    court_name: Optional[str] = None
    date: str
    case_type: Optional[str] = "both"  # civil, criminal, or both

class CauseListResponse(BaseModel):
    success: bool
    message: str
    pdf_url: Optional[str] = None
    pdf_urls: Optional[List[str]] = None
    filename: Optional[str] = None

class StateResponse(BaseModel):
    states: List[str]

class DistrictResponse(BaseModel):
    districts: List[str]

class CourtResponse(BaseModel):
    courts: List[str]

class JudgeInfo(BaseModel):
    name: str
    designation: str
    court_number: str

class JudgeResponse(BaseModel):
    judges: List[JudgeInfo]

class CauseListEntry(BaseModel):
    sr_no: Optional[str]
    case_number: Optional[str]
    case_title: Optional[str]
    petitioner: Optional[str]
    respondent: Optional[str]
    advocate: Optional[str]
    case_type: Optional[str]
    stage: Optional[str]
    purpose: Optional[str]

class CauseListData(BaseModel):
    court_name: str
    judge_name: str
    date: str
    case_type: str
    entries: List[CauseListEntry]
