# Burnout Monitor

A real-time web application that monitors user interactions to detect potential burnout indicators and provide personalized recommendations.

![Burnout Monitor Dashboard](https://images.pexels.com/photos/3755755/pexels-photo-3755755.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2)

## Features

- 🖱️ Real-time mouse and keyboard activity monitoring
- ⏰ Screen time tracking and analysis
- 📊 Application usage tracking
- 🔍 Burnout risk assessment using ML algorithms
- 💡 Personalized recommendations
- 📈 Historical data visualization
- 🔒 Local data storage for privacy

## Tech Stack

- **Backend**: Python with Flask
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Monitoring**: pynput for input tracking
- **Analysis**: scikit-learn for risk assessment
- **Data Storage**: Local JSON storage
- **UI Components**: Font Awesome icons, Google Fonts

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/burnout-monitor.git
cd burnout-monitor
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python src/burnout_monitor.py
```

2. Open your web browser and navigate to:
```
http://localhost:8000
```

The application will start monitoring your computer usage and display:
- Current mouse and keyboard activity
- Screen time statistics
- Real-time burnout risk assessment
- Personalized recommendations

## Project Structure

```
burnout_monitor/
├── src/
│   ├── burnout_monitor.py        # Main application entry
│   ├── monitoring/
│   │   ├── interaction_monitor.py # Input monitoring
│   │   └── burnout_analysis.py   # Risk analysis
│   └── storage/
│       └── data_storage.py       # Data management
├── static/
│   └── js/
│       └── dashboard.js          # Frontend functionality
├── templates/
│   ├── layout.html              # Base template
│   ├── index.html              # Dashboard page
│   └── history.html            # History page
├── data/                       # Data storage directory
├── requirements.txt            # Python dependencies
└── README.md                  # Documentation
```

## Privacy

All monitoring data is stored locally on your machine in the `data` directory. No information is sent to external servers. The application uses JSON files to store:
- Activity metrics
- Screen time data
- Risk assessments
- Usage patterns

## Data Storage

Metrics are saved periodically in JSON format with the following structure:
```json
{
    "timestamp": "2023-01-01T12:00:00",
    "metrics": {
        "mouse_clicks": 150,
        "key_presses": 1000,
        "screen_time": 120,
        "current_app": "Chrome",
        "risk_level": "low"
    }
}
```

## Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- UI design inspired by modern dashboard layouts
- Icons provided by Font Awesome
- Typography by Google Fonts
- Background image from Pexels

## Support

If you encounter any issues or have questions, please:
1. Check the existing issues
2. Create a new issue with a detailed description
3. Include your system information and any relevant logs

---

Built with ❤️ for developer wellbeing
