# Testing Guide

## Manual Testing Checklist

### Frontend Testing
- [ ] Form validation works correctly
- [ ] State dropdown loads and populates
- [ ] District dropdown updates when state changes
- [ ] Court complex dropdown updates when district changes
- [ ] Judge dropdown updates when court complex changes
- [ ] Date picker restricts future dates
- [ ] Case type selection works
- [ ] Loading states display correctly
- [ ] Error messages display and can be dismissed
- [ ] Success messages display properly
- [ ] Responsive design works on mobile/tablet
- [ ] API status indicator shows correct status

### Backend Testing
- [ ] Health check endpoint responds
- [ ] States endpoint returns data
- [ ] Districts endpoint works with valid state
- [ ] Courts endpoint works with valid state/district
- [ ] Judges endpoint works with valid parameters
- [ ] Cause list fetching works end-to-end
- [ ] PDF generation creates valid files
- [ ] ZIP creation works for multiple PDFs
- [ ] File download endpoint serves files correctly
- [ ] Error handling returns appropriate HTTP codes
- [ ] CORS headers are set correctly

### Integration Testing
- [ ] Frontend can communicate with backend
- [ ] Form submission triggers backend API
- [ ] File download works from frontend
- [ ] Error messages propagate correctly
- [ ] Loading states sync with API calls

## Test Cases

### Test Case 1: Basic Cause List Fetch
1. Select "Delhi" as state
2. Select "Delhi" as district
3. Select "Patiala House Court Complex"
4. Leave judge field empty
5. Select today's date
6. Click "Fetch Cause List"
7. Verify PDF download starts

### Test Case 2: Specific Judge Selection
1. Complete form with specific judge selected
2. Verify single PDF is generated
3. Check PDF contains correct judge information

### Test Case 3: Error Handling
1. Try with invalid date (future date)
2. Try with incomplete form
3. Verify appropriate error messages

### Test Case 4: Multiple Judges
1. Select court complex without specific judge
2. Verify multiple PDFs are generated
3. Check ZIP file contains all PDFs

## API Testing with curl

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Get States
```bash
curl http://localhost:8000/api/states
```

### Get Districts
```bash
curl http://localhost:8000/api/districts/Delhi
```

### Fetch Cause List
```bash
curl -X POST http://localhost:8000/api/fetch-causelist \
  -H "Content-Type: application/json" \
  -d '{
    "state": "Delhi",
    "district": "Delhi", 
    "court_complex": "Patiala House Court Complex",
    "date": "2024-01-15",
    "case_type": "both"
  }'
```

## Performance Testing

### Load Testing
- Test with multiple concurrent requests
- Monitor memory usage during PDF generation
- Check response times for different court complexes
- Verify system handles timeout scenarios gracefully

### Stress Testing
- Test with maximum number of judges in a complex
- Generate large PDFs with many case entries
- Test file cleanup mechanisms
- Monitor Chrome driver resource usage

## Browser Compatibility

### Supported Browsers
- [ ] Chrome 90+
- [ ] Firefox 88+
- [ ] Safari 14+
- [ ] Edge 90+

### Mobile Testing
- [ ] iOS Safari
- [ ] Android Chrome
- [ ] Responsive breakpoints work correctly

## Known Limitations

1. **Captcha Handling**: Current implementation cannot handle captchas automatically
2. **Rate Limiting**: No built-in rate limiting for court website requests
3. **Session Management**: No persistent sessions for court websites
4. **Offline Mode**: Application requires internet connection
5. **Large Datasets**: Memory usage may be high for courts with many cases

## Debugging Tips

### Backend Debugging
- Check Chrome driver logs in console
- Monitor network requests to court websites
- Verify PDF file generation in output directory
- Check FastAPI logs for detailed error information

### Frontend Debugging
- Use browser developer tools to check API calls
- Monitor React component state changes
- Check console for JavaScript errors
- Verify network tab for failed requests

### Common Issues
1. **Chrome driver crashes**: Restart the backend service
2. **PDF generation fails**: Check file permissions in output directory
3. **Court website changes**: Update scraping selectors
4. **CORS issues**: Verify backend CORS configuration
