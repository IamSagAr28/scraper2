# Deployment Guide

## Local Development

### Prerequisites
- Python 3.8+
- Node.js 16+
- Chrome browser (for web scraping)

### Setup
1. Run the setup script:
   ```bash
   setup.bat
   ```

2. Start the backend:
   ```bash
   run-backend.bat
   ```

3. Start the frontend (in a new terminal):
   ```bash
   run-frontend.bat
   ```

4. Open http://localhost:3000 in your browser

## Production Deployment

### Backend (FastAPI)

#### Option 1: Render/Railway
1. Create a new service
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables as needed

#### Option 2: Heroku
1. Create `Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
2. Deploy using Heroku CLI or GitHub integration

#### Option 3: VPS/Cloud Server
1. Install Python and dependencies
2. Use gunicorn or uvicorn with systemd service
3. Set up nginx as reverse proxy
4. Configure SSL certificate

### Frontend (React)

#### Option 1: Vercel
1. Connect GitHub repository
2. Set build command: `npm run build`
3. Set output directory: `build`
4. Add environment variable: `REACT_APP_API_URL`

#### Option 2: Netlify
1. Connect GitHub repository
2. Set build command: `npm run build`
3. Set publish directory: `build`
4. Add environment variables in site settings

#### Option 3: Static Hosting
1. Run `npm run build`
2. Upload `build` folder contents to any static hosting service

## Environment Variables

### Backend
- `DEBUG`: Set to `False` in production
- `HOST`: `0.0.0.0` for production
- `PORT`: Port number (usually provided by hosting service)
- `CORS_ORIGINS`: Add your frontend domain

### Frontend
- `REACT_APP_API_URL`: Your backend API URL

## Important Notes

### Web Scraping Considerations
- The application uses Selenium with Chrome for web scraping
- In production, you may need to:
  - Install Chrome/Chromium on the server
  - Use headless mode (already configured)
  - Handle rate limiting and captchas
  - Consider using proxy services for reliability

### Legal Compliance
- Ensure compliance with website terms of service
- Respect robots.txt files
- Implement appropriate rate limiting
- Consider caching to reduce server load

### Performance Optimization
- Implement Redis caching for frequently requested data
- Use CDN for static assets
- Optimize PDF generation for large datasets
- Consider background job processing for long-running scraping tasks

## Troubleshooting

### Common Issues
1. **Chrome driver not found**: Install Chrome and ensure chromedriver is in PATH
2. **CORS errors**: Check CORS_ORIGINS configuration in backend
3. **Timeout errors**: Increase timeout values for slow court websites
4. **Memory issues**: Optimize PDF generation for large cause lists

### Monitoring
- Set up logging for scraping activities
- Monitor API response times
- Track success/failure rates for different court websites
- Implement health checks for all services
