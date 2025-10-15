export interface CauseListRequest {
  state: string;
  district: string;
  court_complex: string;
  court_name?: string;
  date: string;
  case_type?: 'civil' | 'criminal' | 'both';
}

export interface CauseListResponse {
  success: boolean;
  message: string;
  pdf_url?: string;
  pdf_urls?: string[];
  filename?: string;
}

export interface StateResponse {
  states: string[];
}

export interface DistrictResponse {
  districts: string[];
}

export interface CourtResponse {
  courts: string[];
}

export interface JudgeInfo {
  name: string;
  designation: string;
  court_number: string;
}

export interface JudgeResponse {
  judges: JudgeInfo[];
}

export interface FormData {
  state: string;
  district: string;
  court_complex: string;
  court_name: string;
  date: string;
  case_type: 'civil' | 'criminal' | 'both';
}

export interface LoadingState {
  states: boolean;
  districts: boolean;
  courts: boolean;
  judges: boolean;
  fetching: boolean;
}
