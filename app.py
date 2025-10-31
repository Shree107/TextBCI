from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Global variables for simulation
blink_count = 0
blink_logs = []
threshold = 50
system_status = "Active"
morse_blinks = []  # Store blink timings for Morse code
decoded_text = ""  # Decoded Morse code text

# Morse code dictionary
MORSE_CODE = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
    '----.': '9', '/': ' '
}

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple authentication (username and password can be anything)
        if username and password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Please enter username and password")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    global blink_count, system_status, decoded_text
    return render_template('dashboard.html', 
                         blink_count=blink_count,
                         system_status=system_status,
                         decoded_text=decoded_text,
                         username=session.get('username', 'User'))

@app.route('/api/blink-update')
def blink_update():
    """API endpoint to simulate blink detection with Morse code"""
    global blink_count, blink_logs, morse_blinks, decoded_text
    
    # Randomly increment blink count (30% chance)
    blink_detected = False
    morse_pattern = ""
    
    if random.random() < 0.3:
        blink_count += 1
        blink_detected = True
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        blink_logs.append({
            'id': len(blink_logs) + 1,
            'timestamp': timestamp,
            'signal_strength': random.randint(60, 100)
        })
        
        # Simulate Morse code pattern (dot or dash)
        morse_pattern = random.choice(['.', '-'])
        morse_blinks.append(morse_pattern)
        
        # Try to decode when we have enough patterns
        if len(morse_blinks) >= 2:
            # Simulate word completion after 5-7 blinks
            if len(morse_blinks) >= random.randint(5, 7):
                morse_str = ''.join(morse_blinks)
                if morse_str in MORSE_CODE:
                    decoded_text += MORSE_CODE[morse_str]
                morse_blinks.clear()
    
    return jsonify({
        'blink_count': blink_count,
        'system_status': system_status,
        'blink_detected': blink_detected,
        'morse_pattern': morse_pattern,
        'decoded_text': decoded_text,
        'current_morse': ''.join(morse_blinks)
    })

@app.route('/api/reset-morse', methods=['POST'])
def reset_morse():
    """Reset Morse code text"""
    global decoded_text, morse_blinks
    decoded_text = ""
    morse_blinks.clear()
    return jsonify({'success': True, 'decoded_text': decoded_text})

@app.route('/live-signal')
def live_signal():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    return render_template('live_signal.html', threshold=threshold)

@app.route('/api/signal-data')
def signal_data():
    """API endpoint to generate random signal data"""
    # Generate random signal value (0-100)
    signal_value = random.randint(0, 100)
    
    # Detect blink if signal exceeds threshold (random peaks)
    blink_detected = signal_value > threshold and random.random() < 0.2
    
    if blink_detected:
        global blink_count, blink_logs
        blink_count += 1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        blink_logs.append({
            'id': len(blink_logs) + 1,
            'timestamp': timestamp,
            'signal_strength': signal_value
        })
    
    return jsonify({
        'signal_value': signal_value,
        'blink_detected': blink_detected,
        'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3]
    })

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    global threshold
    
    if request.method == 'POST':
        threshold = int(request.form.get('threshold', 50))
        return render_template('settings.html', 
                             threshold=threshold, 
                             success=True)
    
    return render_template('settings.html', threshold=threshold)

@app.route('/logs')
def logs():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    # Reverse the list to show most recent first
    recent_logs = list(reversed(blink_logs))
    
    return render_template('logs.html', logs=recent_logs, total_blinks=blink_count)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
