import axios from 'axios';
import {
  StateResponse,
  DistrictResponse,
  CourtResponse,
  JudgeResponse,
  CauseListRequest,
  CauseListResponse,
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Get list of states
  getStates: async (): Promise<string[]> => {
    const response = await api.get<StateResponse>('/states');
    return response.data.states;
  },

  // Get districts for a state
  getDistricts: async (state: string): Promise<string[]> => {
    const response = await api.get<DistrictResponse>(`/districts/${encodeURIComponent(state)}`);
    return response.data.districts;
  },

  // Get court complexes for a state and district
  getCourts: async (state: string, district: string): Promise<string[]> => {
    const response = await api.get<CourtResponse>(
      `/courts/${encodeURIComponent(state)}/${encodeURIComponent(district)}`
    );
    return response.data.courts;
  },

  // Get judges for a court complex
  getJudges: async (state: string, district: string, courtComplex: string): Promise<JudgeResponse> => {
    const response = await api.get<JudgeResponse>(
      `/judges/${encodeURIComponent(state)}/${encodeURIComponent(district)}/${encodeURIComponent(courtComplex)}`
    );
    return response.data;
  },

  // Fetch cause list
  fetchCauseList: async (request: CauseListRequest): Promise<CauseListResponse> => {
    const response = await api.post<CauseListResponse>('/fetch-causelist', request);
    return response.data;
  },

  // Download file
  downloadFile: async (filename: string): Promise<Blob> => {
    const response = await api.get(`/download/${filename}`, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Health check
  healthCheck: async (): Promise<{ status: string; message: string }> => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default apiService;
