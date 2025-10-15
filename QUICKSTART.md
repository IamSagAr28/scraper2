# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher  
- Chrome browser installed
- Git (optional)

### Step 1: Setup
```bash
# Double-click the setup file or run in command prompt
setup.bat
```

### Step 2: Start Backend
```bash
# Double-click or run in command prompt
run-backend.bat
```
Backend will start at: http://localhost:8000

### Step 3: Start Frontend
```bash
# In a new terminal, double-click or run
run-frontend.bat
```
Frontend will open at: http://localhost:3000

### Step 4: Use the Application
1. **Select State**: Choose from the dropdown (e.g., "Delhi")
2. **Select District**: Will auto-populate based on state
3. **Select Court Complex**: Choose the court complex
4. **Select Judge** (Optional): Leave empty for all judges
5. **Choose Date**: Pick the date for cause list
6. **Click "Fetch Cause List"**: Download will start automatically

## 🎯 Example Usage

### For Delhi Courts:
1. State: `Delhi`
2. District: `Delhi` 
3. Court Complex: `Patiala House Court Complex`
4. Judge: `Leave empty for all judges`
5. Date: `Today's date or any past date`
6. Case Type: `Both Civil & Criminal`

### For Other States:
1. State: `Any state from dropdown`
2. District: `Select after state loads`
3. Court Complex: `Select after district loads`
4. Continue with date and case type selection

## 📋 What You'll Get

- **Single Judge**: One PDF file with that judge's cause list
- **All Judges**: ZIP file containing PDFs for each judge
- **Professional Format**: Clean, printable PDF documents
- **Complete Data**: Case numbers, parties, advocates, etc.

## ⚠️ Important Notes

### First Time Setup
- Chrome driver will be downloaded automatically
- Initial startup may take a few minutes
- Internet connection required for real-time data

### Troubleshooting
- **Backend won't start**: Check if Python is installed and in PATH
- **Frontend won't start**: Check if Node.js is installed
- **No data found**: Try different date or court complex
- **Chrome errors**: Restart the backend service

### Performance Tips
- **Faster Results**: Select specific judge instead of all judges
- **Better Success**: Use recent dates (within last 30 days)
- **Avoid Overload**: Don't make multiple requests simultaneously

## 🔧 Configuration (Optional)

### Backend Configuration
Edit `backend/.env` (create from `.env.example`):
```env
DEBUG=True
PORT=8000
LOG_LEVEL=INFO
```

### Frontend Configuration  
Edit `frontend/.env` (create from `.env.example`):
```env
REACT_APP_API_URL=http://localhost:8000/api
```

## 📞 Support

### Common Issues
1. **Port conflicts**: Change ports in configuration files
2. **Firewall blocking**: Allow Python and Node.js through firewall
3. **Antivirus interference**: Add project folder to exclusions
4. **Chrome not found**: Install Chrome browser

### Getting Help
- Check `TESTING.md` for detailed testing procedures
- Review `DEPLOYMENT.md` for production setup
- See `FEATURES.md` for complete feature list
- Check console logs for error details

## 🎉 Success Indicators

✅ **Backend Ready**: Console shows "Uvicorn running on http://0.0.0.0:8000"  
✅ **Frontend Ready**: Browser opens to http://localhost:3000  
✅ **API Connected**: Green dot shows "API Online" in the header  
✅ **Dropdowns Working**: State dropdown populates with options  
✅ **Download Working**: PDF downloads when form is submitted  

## 🚀 Next Steps

1. **Test Different Courts**: Try various states and court complexes
2. **Explore Features**: Test bulk download and different case types  
3. **Customize**: Modify styling or add new features
4. **Deploy**: Use `DEPLOYMENT.md` for production setup
5. **Contribute**: Submit improvements or bug fixes

---

**Ready to fetch your first cause list? Start with the setup script and follow the steps above!** 🎯
