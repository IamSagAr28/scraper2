import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { Calendar, Download, FileText, MapPin, Building, User, Clock } from 'lucide-react';
import { FormData, LoadingState, JudgeInfo } from '../types';
import { apiService } from '../services/api';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';
import SuccessMessage from './SuccessMessage';

interface CauseListFormProps {
  onSubmit: (data: FormData) => void;
  isSubmitting: boolean;
}

const CauseListForm: React.FC<CauseListFormProps> = ({ onSubmit, isSubmitting }) => {
  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm<FormData>();
  
  const [states, setStates] = useState<string[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);
  const [courts, setCourts] = useState<string[]>([]);
  const [judges, setJudges] = useState<JudgeInfo[]>([]);
  
  const [loading, setLoading] = useState<LoadingState>({
    states: false,
    districts: false,
    courts: false,
    judges: false,
    fetching: false,
  });
  
  const [error, setError] = useState<string>('');
  
  const watchedState = watch('state');
  const watchedDistrict = watch('district');
  const watchedCourtComplex = watch('court_complex');

  // Load states on component mount
  useEffect(() => {
    loadStates();
  }, []);

  // Load districts when state changes
  useEffect(() => {
    if (watchedState) {
      loadDistricts(watchedState);
      // Reset dependent fields
      setValue('district', '');
      setValue('court_complex', '');
      setValue('court_name', '');
      setDistricts([]);
      setCourts([]);
      setJudges([]);
    }
  }, [watchedState, setValue]);

  // Load courts when district changes
  useEffect(() => {
    if (watchedState && watchedDistrict) {
      loadCourts(watchedState, watchedDistrict);
      // Reset dependent fields
      setValue('court_complex', '');
      setValue('court_name', '');
      setCourts([]);
      setJudges([]);
    }
  }, [watchedState, watchedDistrict, setValue]);

  // Load judges when court complex changes
  useEffect(() => {
    if (watchedState && watchedDistrict && watchedCourtComplex) {
      loadJudges(watchedState, watchedDistrict, watchedCourtComplex);
      setValue('court_name', '');
      setJudges([]);
    }
  }, [watchedState, watchedDistrict, watchedCourtComplex, setValue]);

  const loadStates = async () => {
    try {
      setLoading(prev => ({ ...prev, states: true }));
      setError('');
      const statesList = await apiService.getStates();
      setStates(statesList);
    } catch (err) {
      setError('Failed to load states. Please try again.');
      console.error('Error loading states:', err);
    } finally {
      setLoading(prev => ({ ...prev, states: false }));
    }
  };

  const loadDistricts = async (state: string) => {
    try {
      setLoading(prev => ({ ...prev, districts: true }));
      setError('');
      const districtsList = await apiService.getDistricts(state);
      setDistricts(districtsList);
    } catch (err) {
      setError('Failed to load districts. Please try again.');
      console.error('Error loading districts:', err);
    } finally {
      setLoading(prev => ({ ...prev, districts: false }));
    }
  };

  const loadCourts = async (state: string, district: string) => {
    try {
      setLoading(prev => ({ ...prev, courts: true }));
      setError('');
      const courtsList = await apiService.getCourts(state, district);
      setCourts(courtsList);
    } catch (err) {
      setError('Failed to load court complexes. Please try again.');
      console.error('Error loading courts:', err);
    } finally {
      setLoading(prev => ({ ...prev, courts: false }));
    }
  };

  const loadJudges = async (state: string, district: string, courtComplex: string) => {
    try {
      setLoading(prev => ({ ...prev, judges: true }));
      setError('');
      const judgesResponse = await apiService.getJudges(state, district, courtComplex);
      setJudges(judgesResponse.judges);
    } catch (err) {
      setError('Failed to load judges. Please try again.');
      console.error('Error loading judges:', err);
    } finally {
      setLoading(prev => ({ ...prev, judges: false }));
    }
  };

  const handleFormSubmit = (data: FormData) => {
    setError('');
    onSubmit(data);
  };

  // Get today's date in YYYY-MM-DD format
  const today = new Date().toISOString().split('T')[0];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 flex items-center">
          <FileText className="mr-3 h-6 w-6 text-primary-600" />
          Court Cause List Fetcher
        </h2>
        <p className="mt-2 text-gray-600">
          Select court details and date to fetch the cause list in real-time
        </p>
      </div>

      {error && (
        <ErrorMessage 
          message={error} 
          onClose={() => setError('')}
          className="mb-6"
        />
      )}

      <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
        {/* State Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <MapPin className="inline w-4 h-4 mr-1" />
            State *
          </label>
          <select
            {...register('state', { required: 'State is required' })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            disabled={loading.states}
          >
            <option value="">
              {loading.states ? 'Loading states...' : 'Select State'}
            </option>
            {states.map((state) => (
              <option key={state} value={state}>
                {state}
              </option>
            ))}
          </select>
          {errors.state && (
            <p className="mt-1 text-sm text-red-600">{errors.state.message}</p>
          )}
        </div>

        {/* District Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <MapPin className="inline w-4 h-4 mr-1" />
            District *
          </label>
          <select
            {...register('district', { required: 'District is required' })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            disabled={!watchedState || loading.districts}
          >
            <option value="">
              {loading.districts ? 'Loading districts...' : 'Select District'}
            </option>
            {districts.map((district) => (
              <option key={district} value={district}>
                {district}
              </option>
            ))}
          </select>
          {errors.district && (
            <p className="mt-1 text-sm text-red-600">{errors.district.message}</p>
          )}
        </div>

        {/* Court Complex Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Building className="inline w-4 h-4 mr-1" />
            Court Complex *
          </label>
          <select
            {...register('court_complex', { required: 'Court Complex is required' })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            disabled={!watchedDistrict || loading.courts}
          >
            <option value="">
              {loading.courts ? 'Loading court complexes...' : 'Select Court Complex'}
            </option>
            {courts.map((court) => (
              <option key={court} value={court}>
                {court}
              </option>
            ))}
          </select>
          {errors.court_complex && (
            <p className="mt-1 text-sm text-red-600">{errors.court_complex.message}</p>
          )}
        </div>

        {/* Judge/Court Name Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <User className="inline w-4 h-4 mr-1" />
            Judge/Court Name (Optional)
          </label>
          <select
            {...register('court_name')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            disabled={!watchedCourtComplex || loading.judges}
          >
            <option value="">
              {loading.judges 
                ? 'Loading judges...' 
                : 'All Judges (Leave empty to fetch all cause lists)'
              }
            </option>
            {judges.map((judge, index) => (
              <option key={index} value={judge.name}>
                {judge.name} - {judge.designation}
              </option>
            ))}
          </select>
          <p className="mt-1 text-xs text-gray-500">
            Leave empty to fetch cause lists for all judges in the court complex
          </p>
        </div>

        {/* Date Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Calendar className="inline w-4 h-4 mr-1" />
            Date *
          </label>
          <input
            type="date"
            {...register('date', { required: 'Date is required' })}
            max={today}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          {errors.date && (
            <p className="mt-1 text-sm text-red-600">{errors.date.message}</p>
          )}
        </div>

        {/* Case Type Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Case Type
          </label>
          <select
            {...register('case_type')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="both">Both Civil & Criminal</option>
            <option value="civil">Civil Only</option>
            <option value="criminal">Criminal Only</option>
          </select>
        </div>

        {/* Submit Button */}
        <div className="pt-4">
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full bg-primary-600 text-white py-3 px-4 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {isSubmitting ? (
              <>
                <LoadingSpinner size="sm" />
                <span className="ml-2">Fetching Cause List...</span>
              </>
            ) : (
              <>
                <Download className="w-5 h-5 mr-2" />
                Fetch Cause List
              </>
            )}
          </button>
        </div>
      </form>

      {/* Instructions */}
      <div className="mt-8 p-4 bg-blue-50 rounded-md">
        <h3 className="text-sm font-medium text-blue-900 mb-2">Instructions:</h3>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>• Select State, District, and Court Complex from the dropdowns</li>
          <li>• Optionally select a specific Judge (leave empty for all judges)</li>
          <li>• Choose the date for which you want the cause list</li>
          <li>• Click "Fetch Cause List" to generate and download PDF(s)</li>
          <li>• Multiple PDFs will be compressed into a ZIP file</li>
        </ul>
      </div>
    </div>
  );
};

export default CauseListForm;
