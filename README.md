# Eye-Blink Detection System UI

A Flask-based web application that simulates an Eye-Blink Detection System with a modern, clean UI using Bootstrap 5.

## Features

- **Login System**: Simple username/password authentication
- **Dashboard**: Real-time system status with auto-updating blink counter
- **Morse Code Decoder**: Simulates converting blink patterns into text using Morse code
- **Live Signal**: Real-time signal graph with JavaScript-generated random values (~200ms updates)
- **Settings**: Adjustable threshold slider (0-100) with save functionality
- **Logs**: Table of blink timestamps stored during runtime
- **Modern UI**: Clean Bootstrap 5 interface with gradient backgrounds and smooth animations

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Login with any username and password (demo mode)

## Pages

### /login
- Simple authentication page
- Accepts any username/password combination

### /dashboard
- System status display
- Auto-incrementing blink counter (updates every 2 seconds)
- **Morse Code Decoder**: Converts simulated blink patterns into text
  - Shows current Morse pattern (dots and dashes)
  - Displays decoded text in real-time
  - Reset button to clear decoded text
- Session timer
- Quick action buttons

### /live-signal
- Real-time signal waveform graph
- Updates every ~200ms with random values
- "Blink Detected" alerts when random peaks occur
- Visual threshold indicator

### /settings
- Threshold slider (0-100)
- Save button to update detection sensitivity
- System information panel
- Help section

### /logs
- Table of all detected blinks with timestamps
- Signal strength for each detection
- Search and filter functionality
- Statistics panel

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5, Chart.js
- **Templates**: Jinja2
- **Data Storage**: In-memory Python lists and global variables (resets on server restart)
- **Simulation**: Random values generated for blink detection and signal data

## Notes

- This is a simulation/demo application with no hardware integration
- All data is stored in memory and will be lost when the server restarts
- Blink detection uses random values to simulate real sensor data
- The application runs in debug mode by default

## Project Structure

```
EOG/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── templates/
    ├── base.html         # Base template with navigation
    ├── login.html        # Login page
    ├── dashboard.html    # Dashboard with stats
    ├── live_signal.html  # Real-time signal graph
    ├── settings.html     # Settings page
    └── logs.html         # Blink logs table
```

## License

This is a demo project for educational purposes.
