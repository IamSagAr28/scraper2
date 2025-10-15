# 🏛️ Court Cause List Fetcher

A comprehensive full-stack web application that fetches court cause lists in **real-time** from official Indian court websites and generates professional downloadable PDFs.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green.svg)

## 🚀 Quick Start

**Get started in 5 minutes:**

1. **Setup**: Run `setup.bat` 
2. **Backend**: Run `run-backend.bat`
3. **Frontend**: Run `run-frontend.bat`
4. **Use**: Open http://localhost:3000

📖 **Detailed guide**: See [QUICKSTART.md](QUICKSTART.md)

## ✨ Key Features

### 🌐 **Real-time Data Fetching**
- Scrapes live data from official court websites
- No cached data - always current information
- Supports multiple court systems across India

### 📋 **Smart Form Interface** 
- Cascading dropdowns: State → District → Court Complex → Judge
- Form validation with helpful error messages
- Date picker with intelligent restrictions

### 📄 **Professional PDF Generation**
- Clean, well-formatted court cause lists
- Bulk download: All judges in ZIP format
- Includes metadata and timestamps

### 🔄 **Bulk Operations**
- Fetch cause lists for all judges at once
- Efficient batch processing
- Progress tracking and status updates

### 📱 **Modern UI/UX**
- Responsive design for all devices
- Loading states and error handling
- Intuitive step-by-step workflow

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | React 18 + TypeScript + TailwindCSS |
| **Backend** | FastAPI + Python 3.8+ |
| **Web Scraping** | Selenium + Chrome WebDriver |
| **PDF Generation** | ReportLab |
| **UI Icons** | Lucide React |
| **HTTP Client** | Axios |

## 📁 Project Structure

```
court-cause-list/
├── 📁 frontend/                 # React TypeScript frontend
│   ├── 📁 src/
│   │   ├── 📁 components/      # Reusable UI components
│   │   ├── 📁 services/        # API service layer
│   │   ├── 📁 types/           # TypeScript definitions
│   │   └── 📄 App.tsx          # Main application
│   └── 📄 package.json
├── 📁 backend/                 # FastAPI Python backend
│   ├── 📁 app/
│   │   ├── 📁 api/            # REST API endpoints
│   │   ├── 📁 scrapers/       # Web scraping modules
│   │   ├── 📁 utils/          # PDF generation & utilities
│   │   └── 📁 models/         # Data models & schemas
│   ├── 📄 requirements.txt
│   └── 📄 main.py
├── 📄 setup.bat               # One-click setup script
├── 📄 QUICKSTART.md          # 5-minute setup guide
├── 📄 FEATURES.md            # Detailed feature list
└── 📄 DEPLOYMENT.md          # Production deployment guide
```

## 🎯 Usage Example

### For Delhi Courts:
```
1. State: Delhi
2. District: Delhi  
3. Court Complex: Patiala House Court Complex
4. Judge: [Leave empty for all judges]
5. Date: [Select date]
6. Click "Fetch Cause List"
```

**Result**: ZIP file with PDFs for each judge's cause list

### For Other States:
```
1. State: [Any state from dropdown]
2. District: [Auto-populated]
3. Court Complex: [Auto-populated] 
4. Judge: [Optional - specific judge]
5. Date: [Select date]
6. Click "Fetch Cause List"
```

**Result**: Single PDF or ZIP based on selection

## 🌐 Supported Data Sources

| Source | Coverage | Status |
|--------|----------|--------|
| **eCourts India** | All Indian states & districts | ✅ Primary |
| **Delhi District Courts** | Delhi court complexes | ✅ Fallback |
| **Future Sources** | High Courts, Tribunals | 🔄 Planned |

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/states` | Get list of all states |
| `GET` | `/api/districts/{state}` | Get districts for state |
| `GET` | `/api/courts/{state}/{district}` | Get court complexes |
| `GET` | `/api/judges/{state}/{district}/{court}` | Get judges list |
| `POST` | `/api/fetch-causelist` | Generate cause list PDF |
| `GET` | `/api/download/{filename}` | Download generated files |

## 🔧 Configuration

### Environment Variables

**Backend** (`.env`):
```env
DEBUG=True
PORT=8000
CORS_ORIGINS=["http://localhost:3000"]
SCRAPING_TIMEOUT=30
```

**Frontend** (`.env`):
```env
REACT_APP_API_URL=http://localhost:8000/api
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup guide |
| [FEATURES.md](FEATURES.md) | Complete feature overview |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment |
| [TESTING.md](TESTING.md) | Testing procedures |

## 🚦 System Requirements

### Minimum Requirements:
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **Node.js**: 16 or higher  
- **Chrome**: Latest version
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space

### Development Requirements:
- **Git**: For version control
- **VS Code**: Recommended editor
- **Postman**: For API testing (optional)

## 🛡️ Legal & Compliance

- ✅ **Ethical Scraping**: Respects robots.txt and rate limits
- ✅ **Public Data**: Only accesses publicly available information
- ✅ **No Storage**: Doesn't store personal or case data
- ✅ **Terms Compliance**: Adheres to website terms of service

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

## 📞 Support & Issues

- 🐛 **Bug Reports**: Use GitHub Issues
- 💡 **Feature Requests**: Use GitHub Discussions  
- 📧 **Support**: Check documentation first
- 💬 **Community**: Join our discussions

## 📈 Roadmap

### Version 2.0 (Planned)
- [ ] High Court integration
- [ ] Tribunal support  
- [ ] Advanced filtering
- [ ] Case tracking
- [ ] Email notifications
- [ ] Mobile app

### Version 1.1 (Next)
- [ ] Caching system
- [ ] Better error recovery
- [ ] Performance optimizations
- [ ] Additional court sources

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **eCourts India** for providing public access to court data
- **Delhi District Courts** for transparent cause list publishing
- **Open Source Community** for the amazing tools and libraries

---

**Built with ❤️ for the legal community and citizens of India**

[![GitHub stars](https://img.shields.io/github/stars/username/court-cause-list?style=social)](https://github.com/username/court-cause-list)
[![GitHub forks](https://img.shields.io/github/forks/username/court-cause-list?style=social)](https://github.com/username/court-cause-list)

**Ready to get started?** 👉 [Quick Start Guide](QUICKSTART.md)
