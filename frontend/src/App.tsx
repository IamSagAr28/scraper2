import React, { useState, useEffect } from 'react';
import { Scale, Github, ExternalLink } from 'lucide-react';
import CauseListForm from './components/CauseListForm';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import SuccessMessage from './components/SuccessMessage';
import { FormData, CauseListResponse } from './types';
import { apiService } from './services/api';

function App() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState<CauseListResponse | null>(null);
  const [error, setError] = useState<string>('');
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);

  // Check API health on component mount
  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      await apiService.healthCheck();
      setIsHealthy(true);
    } catch (err) {
      setIsHealthy(false);
      console.error('API health check failed:', err);
    }
  };

  const handleFormSubmit = async (formData: FormData) => {
    setIsSubmitting(true);
    setError('');
    setResult(null);

    try {
      const response = await apiService.fetchCauseList({
        state: formData.state,
        district: formData.district,
        court_complex: formData.court_complex,
        court_name: formData.court_name || undefined,
        date: formData.date,
        case_type: formData.case_type,
      });

      setResult(response);

      // If successful and has download URL, trigger download
      if (response.success && response.pdf_url) {
        handleDownload(response.pdf_url, response.filename || 'cause_list.pdf');
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to fetch cause list';
      setError(errorMessage);
      console.error('Error fetching cause list:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDownload = async (url: string, filename: string) => {
    try {
      // Extract filename from URL
      const urlParts = url.split('/');
      const fileToDownload = urlParts[urlParts.length - 1];
      
      const blob = await apiService.downloadFile(fileToDownload);
      
      // Create download link
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);
    } catch (err) {
      console.error('Error downloading file:', err);
      setError('Failed to download the file. Please try again.');
    }
  };

  const clearMessages = () => {
    setError('');
    setResult(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <Scale className="h-8 w-8 text-primary-600 mr-3" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  Court Cause List Fetcher
                </h1>
                <p className="text-sm text-gray-500">
                  Real-time court cause list generator
                </p>
              </div>
            </div>
            
            {/* API Status Indicator */}
            <div className="flex items-center space-x-4">
              <div className="flex items-center">
                <div 
                  className={`w-3 h-3 rounded-full mr-2 ${
                    isHealthy === null 
                      ? 'bg-gray-400' 
                      : isHealthy 
                        ? 'bg-green-400' 
                        : 'bg-red-400'
                  }`}
                />
                <span className="text-sm text-gray-600">
                  API {isHealthy === null ? 'Checking...' : isHealthy ? 'Online' : 'Offline'}
                </span>
              </div>
              
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-500 hover:text-gray-700"
              >
                <Github className="h-5 w-5" />
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* API Offline Warning */}
        {isHealthy === false && (
          <ErrorMessage 
            message="API server is offline. Please ensure the backend server is running on http://localhost:8000"
            className="mb-6"
          />
        )}

        {/* Form */}
        <div className="mb-8">
          <CauseListForm 
            onSubmit={handleFormSubmit}
            isSubmitting={isSubmitting}
          />
        </div>

        {/* Results */}
        {error && (
          <ErrorMessage 
            message={error}
            onClose={clearMessages}
            className="mb-6"
          />
        )}

        {result && (
          <div className="mb-6">
            {result.success ? (
              <SuccessMessage 
                message={result.message}
                onClose={clearMessages}
              />
            ) : (
              <ErrorMessage 
                message={result.message}
                onClose={clearMessages}
              />
            )}
          </div>
        )}

        {/* Loading State */}
        {isSubmitting && (
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <LoadingSpinner size="lg" />
            <h3 className="mt-4 text-lg font-medium text-gray-900">
              Fetching Cause List
            </h3>
            <p className="mt-2 text-gray-600">
              This may take a few moments while we scrape the latest data...
            </p>
            <div className="mt-4 bg-blue-50 rounded-md p-4">
              <p className="text-sm text-blue-700">
                <strong>Please wait:</strong> We're accessing the official court websites 
                in real-time to fetch the most current cause list data.
              </p>
            </div>
          </div>
        )}

        {/* Features Section */}
        <div className="mt-12 bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Features</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">Real-time Data</h3>
              <p className="text-gray-600 text-sm">
                Fetches live cause list data directly from official court websites
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">PDF Generation</h3>
              <p className="text-gray-600 text-sm">
                Converts cause lists to clean, professional PDF documents
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">Bulk Download</h3>
              <p className="text-gray-600 text-sm">
                Download cause lists for all judges in a court complex at once
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">Multiple Sources</h3>
              <p className="text-gray-600 text-sm">
                Supports eCourts India and Delhi District Courts websites
              </p>
            </div>
          </div>
        </div>

        {/* Data Sources */}
        <div className="mt-8 bg-gray-50 rounded-lg p-6">
          <h3 className="font-semibold text-gray-800 mb-3">Data Sources</h3>
          <div className="space-y-2">
            <div className="flex items-center text-sm text-gray-600">
              <ExternalLink className="w-4 h-4 mr-2" />
              <span>Primary: </span>
              <a 
                href="https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline ml-1"
              >
                eCourts India Services
              </a>
            </div>
            <div className="flex items-center text-sm text-gray-600">
              <ExternalLink className="w-4 h-4 mr-2" />
              <span>Fallback: </span>
              <a 
                href="https://newdelhi.dcourts.gov.in/cause-list-daily-board/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline ml-1"
              >
                New Delhi District Courts
              </a>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-gray-500">
            <p>
              Court Cause List Fetcher - Built for educational and research purposes
            </p>
            <p className="mt-1">
              Data is fetched from publicly available official court websites
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
