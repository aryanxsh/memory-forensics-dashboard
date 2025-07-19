# Memory Forensics Dashboard

>  Advanced memory forensics and malware analysis toolkit with a modern web-based dashboard

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Features

- **Modern Web Dashboard**: Beautiful, responsive interface built with Bootstrap 5
- **Volatility3 Integration**: Advanced memory forensics analysis
- **YARA Scanner**: Pattern-based malware detection with 491+ rules
- **Real-time Statistics**: Live updates of reports, rules, and scan status
- **File Management**: View, download, and analyze generated reports
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Professional UI**: Gradient backgrounds, animations, and modern UX

## 📋 Prerequisites

- Python 3.7 or higher
- Windows 10/11 (for Windows-specific memory analysis)
- Administrator privileges (for some Volatility operations)
- Git (for cloning the repository)

## 🛠️ Installation

### Quick Start

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/aryanxsh/memory-forensics-dashboard.git
   cd memory-forensics-dashboard
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Dashboard:**
   ```bash
   python app.py
   ```

4. **Access the Dashboard:**
   Open your browser and navigate to: `http://localhost:5000`

### Directory Structure

```
memory-forensics-dashboard/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore rules
├── static/               # Static files and outputs
│   ├── css/             # Custom CSS styles
│   ├── js/              # JavaScript functionality
│   ├── volatility_output/ # Volatility analysis results
│   └── yara_output/      # YARA scan results
├── templates/            # HTML templates
│   ├── index.html        # Main dashboard
│   └── files.html        # File listing page
├── scripts/              # Analysis scripts
│   ├── volatility_gui.py # Volatility GUI
│   ├── yara_scanner.py  # YARA Scanner GUI
│   └── rules/           # YARA rule collection (491+ rules)
├── start.bat            # Windows startup script
├── start.sh             # Linux/Mac startup script
└── volatility3/         # Volatility3 framework
```

## 🎯 Usage Guide

### Dashboard Overview

The dashboard provides:
- **Quick Stats**: Real-time counts of reports, YARA rules, and threats
- **Analysis Tools**: Easy access to Volatility and YARA scanners
- **Reports Section**: View and manage generated analysis files
- **Recent Activity**: Track system operations and tool status

### Volatility Analysis

1. Click "Launch Volatility GUI" from the dashboard
2. Select your memory dump file (.dmp, .raw, .img, .vmem)
3. Choose analysis plugins (processes, network, registry, etc.)
4. Review generated reports in the "Volatility Reports" section

**Available Plugins:**
- `windows.pslist` - Process listing
- `windows.pstree` - Process tree
- `windows.dlllist` - DLL listing
- `windows.filescan` - File scanning
- `windows.registry.hivelist` - Registry analysis
- `windows.malfind` - Malware detection
- And many more...

### YARA Scanning

1. Click "Launch YARA Scanner" from the dashboard
2. Select target files or directories
3. Choose YARA rule sets (APT groups, malware families, etc.)
4. Review scan results in the "YARA Scan Logs" section

**YARA Rule Categories:**
- **APT Groups**: Advanced Persistent Threat detection
- **Malware Families**: Known malware signatures
- **Exploit Kits**: Common exploit frameworks
- **Ransomware**: Various ransomware families
- **RATs**: Remote Access Trojans
- **Webshells**: Web-based backdoors

### Viewing Reports

- **Volatility Reports**: Memory analysis artifacts, process lists, network connections
- **YARA Logs**: Malware detection results, threat classifications
- **File Downloads**: Download reports for external analysis
- **In-browser Viewing**: Text-based reports display directly in browser

## 🔧 Configuration

### YARA Rules

The project includes an extensive collection of 491+ YARA rules:
- **APT Groups**: Advanced Persistent Threat detection rules
- **Malware Families**: Known malware family signatures
- **Exploit Kits**: Detection for common exploit frameworks
- **Ransomware**: Various ransomware detection patterns
- **RATs**: Remote Access Trojan signatures
- **Webshells**: Web-based backdoor detection

### Output Directories

- `static/volatility_output/`: Volatility analysis results
- `static/yara_output/`: YARA scan logs and reports

## 📊 API Endpoints

The dashboard provides several API endpoints:

- `GET /api/stats`: Get real-time statistics
- `GET /api/tool-status`: Check tool availability
- `GET /api/recent-activity`: Get recent system activities
- `POST /run-volatility`: Launch Volatility GUI
- `POST /run-yara`: Launch YARA Scanner

## 🎨 Customization

### Styling

The dashboard uses Bootstrap 5 with custom CSS. Key styling classes:
- `.hero-section`: Main header with gradient background
- `.tool-card`: Analysis tool cards with hover effects
- `.stats-card`: Statistics cards with gradient backgrounds
- `.file-card`: File listing cards

### Adding New Tools

1. Create your tool script in the `scripts/` directory
2. Add a new route in `app.py`
3. Update the dashboard template to include your tool
4. Add appropriate styling and icons

## 🔒 Security Considerations

- **File Permissions**: Ensure proper file permissions for output directories
- **Network Access**: The dashboard runs on `0.0.0.0:5000` by default
- **Administrator Rights**: Some Volatility operations require elevated privileges
- **Memory Dumps**: Handle sensitive memory dumps with appropriate security measures
- **YARA Rules**: Keep rules updated for latest threat detection

##  Troubleshooting

### Common Issues

1. **Port Already in Use:**
   ```bash
   # Change port in app.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

2. **Missing Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Permission Errors:**
   - Run as Administrator for Windows memory analysis
   - Check file permissions for output directories

4. **Volatility Not Found:**
   - Ensure volatility3 directory is present
   - Check Python path and dependencies

5. **YARA Rules Not Loading:**
   - Verify scripts/rules directory exists
   - Check for syntax errors in YARA files

### Debug Mode

Enable debug mode for detailed error messages:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

##  Performance Tips

- **Large Memory Dumps**: Use appropriate Volatility plugins for large files
- **YARA Rules**: Optimize rule sets for your specific use case
- **Output Management**: Regularly clean up old reports
- **Resource Monitoring**: Monitor system resources during analysis

<<<<<<< HEAD
## 🚀 Quick Commands

### Windows
```bash
# Start with batch file
start.bat

# Or manually
python app.py
```

### Linux/Mac
```bash
# Start with shell script
./start.sh

# Or manually
python3 app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request
=======
##  Quick Commands

### Windows
```bash
# Start with batch file
start.bat
>>>>>>> 805aa973abf3a76798c7558c89cca21b6e89cbb6

# Or manually
python app.py
```

<<<<<<< HEAD
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
=======
### Linux/Mac
```bash
# Start with shell script
./start.sh
>>>>>>> 805aa973abf3a76798c7558c89cca21b6e89cbb6

# Or manually
python3 app.py
```

##  Acknowledgments

- **Volatility Foundation**: For the Volatility3 framework
- **YARA Project**: For the pattern matching engine
- **Bootstrap Team**: For the responsive CSS framework
- **Font Awesome**: For the icon library
- **Flask Team**: For the web framework

##  Support

For issues and questions:
- Create an issue on [GitHub](https://github.com/aryanxsh/memory-forensics-dashboard/issues)
- Check the troubleshooting section
- Review the documentation

<<<<<<< HEAD
## 📊 Project Stats
=======
##  Project Stats
>>>>>>> 805aa973abf3a76798c7558c89cca21b6e89cbb6

- **514 files** committed
- **158,667 lines** of code
- **491+ YARA rules** included
- **Modern web interface** with Bootstrap 5
- **Real-time dashboard** with live statistics

---

<<<<<<< HEAD
**⭐ Star this repository if you find it useful!**

**🔗 Repository**: https://github.com/aryanxsh/memory-forensics-dashboard
=======

** Repository**: https://github.com/aryanxsh/memory-forensics-dashboard
>>>>>>> 805aa973abf3a76798c7558c89cca21b6e89cbb6
