from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from typing import List
import os
import zipfile
from app.models.schemas import (
    CauseListRequest, CauseListResponse, StateResponse, 
    DistrictResponse, CourtResponse, JudgeResponse
)
from app.scrapers.ecourts_scraper import ECourtsScraper
from app.scrapers.delhi_courts_scraper import DelhiCourtsScraper
from app.scrapers.mock_scraper import MockScraper
from app.utils.pdf_generator import PDFGenerator

router = APIRouter()

# Initialize scrapers and PDF generator
ecourts_scraper = ECourtsScraper()
delhi_scraper = DelhiCourtsScraper()
mock_scraper = MockScraper()  # For testing without Chrome driver
pdf_generator = PDFGenerator()

@router.get("/states", response_model=StateResponse)
async def get_states():
    """Get list of states"""
    try:
        # Use mock scraper for now to avoid Chrome driver issues
        states = mock_scraper.get_states()
        return StateResponse(states=states)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching states: {str(e)}")

@router.get("/districts/{state}", response_model=DistrictResponse)
async def get_districts(state: str):
    """Get districts for a given state"""
    try:
        # Use mock scraper for now
        districts = mock_scraper.get_districts(state)
        return DistrictResponse(districts=districts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching districts: {str(e)}")

@router.get("/courts/{state}/{district}", response_model=CourtResponse)
async def get_courts(state: str, district: str):
    """Get court complexes for a given state and district"""
    try:
        # Use mock scraper for now
        courts = mock_scraper.get_court_complexes(state, district)
        return CourtResponse(courts=courts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching courts: {str(e)}")

@router.get("/judges/{state}/{district}/{court_complex}", response_model=JudgeResponse)
async def get_judges(state: str, district: str, court_complex: str):
    """Get judges for a given court complex"""
    try:
        # Use mock scraper for now
        judges = mock_scraper.get_judges(state, district, court_complex)
        return JudgeResponse(judges=judges)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching judges: {str(e)}")

@router.post("/fetch-causelist", response_model=CauseListResponse)
async def fetch_cause_list(request: CauseListRequest, background_tasks: BackgroundTasks):
    """Fetch cause list and generate PDF"""
    try:
        # Use mock scraper for now to avoid Chrome driver issues
        cause_lists = mock_scraper.fetch_cause_list(
            request.state,
            request.district,
            request.court_complex,
            request.court_name,
            request.date,
            request.case_type
        )
        
        if not cause_lists:
            return CauseListResponse(
                success=False,
                message="No cause lists found for the given criteria"
            )
        
        # Generate PDFs
        output_dir = pdf_generator.create_output_directory()
        pdf_files = pdf_generator.generate_multiple_cause_lists_pdf(cause_lists, output_dir)
        
        if not pdf_files:
            return CauseListResponse(
                success=False,
                message="Failed to generate PDF files"
            )
        
        # If multiple PDFs, create a zip file
        if len(pdf_files) > 1:
            zip_filename = f"cause_lists_{request.date}.zip"
            zip_path = os.path.join(output_dir, zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for pdf_file in pdf_files:
                    zipf.write(pdf_file, os.path.basename(pdf_file))
            
            # Schedule cleanup
            background_tasks.add_task(cleanup_files, [zip_path] + pdf_files)
            
            return CauseListResponse(
                success=True,
                message=f"Generated {len(pdf_files)} cause list PDFs",
                pdf_url=f"/download/{os.path.basename(zip_path)}",
                filename=zip_filename
            )
        else:
            # Single PDF
            pdf_file = pdf_files[0]
            background_tasks.add_task(cleanup_files, [pdf_file])
            
            return CauseListResponse(
                success=True,
                message="Generated cause list PDF",
                pdf_url=f"/download/{os.path.basename(pdf_file)}",
                filename=os.path.basename(pdf_file)
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching cause list: {str(e)}")

@router.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated PDF or ZIP file"""
    try:
        # Look for the file in recent output directories
        base_dir = "output"
        if not os.path.exists(base_dir):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Find the file in subdirectories
        file_path = None
        for root, dirs, files in os.walk(base_dir):
            if filename in files:
                file_path = os.path.join(root, filename)
                break
        
        if not file_path or not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Determine media type
        media_type = "application/pdf" if filename.endswith('.pdf') else "application/zip"
        
        return FileResponse(
            path=file_path,
            media_type=media_type,
            filename=filename
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")

def cleanup_files(file_paths: List[str]):
    """Background task to cleanup generated files after some time"""
    import time
    time.sleep(300)  # Wait 5 minutes before cleanup
    
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Court Cause List API is running"}
