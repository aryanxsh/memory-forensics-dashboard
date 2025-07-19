from flask import Flask, render_template, request, redirect, send_from_directory, url_for, jsonify
import subprocess
import os
import json
from datetime import datetime
import glob

app = Flask(__name__)
app.config['VOL_OUT'] = os.path.join('static', 'volatility_output')
app.config['YARA_OUT'] = os.path.join('static', 'yara_output')

os.makedirs(app.config['VOL_OUT'], exist_ok=True)
os.makedirs(app.config['YARA_OUT'], exist_ok=True)

def get_file_stats():
    """Get statistics about files and reports"""
    vol_files = len(os.listdir(app.config['VOL_OUT'])) if os.path.exists(app.config['VOL_OUT']) else 0
    yara_files = len(os.listdir(app.config['YARA_OUT'])) if os.path.exists(app.config['YARA_OUT']) else 0
    
    # Count YARA rules
    yara_rules = 0
    if os.path.exists('scripts/rules'):
        yara_rules = len(glob.glob('scripts/rules/*.yar')) + len(glob.glob('scripts/rules/*.yara'))
    
    # Get last scan time
    last_scan = "Never"
    vol_files_list = os.listdir(app.config['VOL_OUT']) if os.path.exists(app.config['VOL_OUT']) else []
    yara_files_list = os.listdir(app.config['YARA_OUT']) if os.path.exists(app.config['YARA_OUT']) else []
    
    all_files = vol_files_list + yara_files_list
    if all_files:
        # Get the most recent file modification time
        latest_time = 0
        for file in all_files:
            file_path = os.path.join(app.config['VOL_OUT'] if file in vol_files_list else app.config['YARA_OUT'], file)
            if os.path.exists(file_path):
                mod_time = os.path.getmtime(file_path)
                if mod_time > latest_time:
                    latest_time = mod_time
        
        if latest_time > 0:
            last_scan = datetime.fromtimestamp(latest_time).strftime('%Y-%m-%d %H:%M')
    
    return {
        'vol_files': vol_files,
        'yara_files': yara_files,
        'yara_rules': yara_rules,
        'last_scan': last_scan,
        'total_files': vol_files + yara_files
    }

# Homepage
@app.route('/')
def index():
    stats = get_file_stats()
    return render_template('index.html', stats=stats)

# API endpoint for stats
@app.route('/api/stats')
def api_stats():
    return jsonify(get_file_stats())

# Run Volatility GUI
@app.route('/run-volatility', methods=['POST'])
def run_volatility():
    try:
        subprocess.Popen(['python', 'scripts/volatility_gui.py'])  # Launch GUI separately
        return jsonify({'status': 'success', 'message': 'Volatility GUI launched successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to launch Volatility: {str(e)}'})

# Run YARA GUI
@app.route('/run-yara', methods=['POST'])
def run_yara():
    try:
        subprocess.Popen(['python', 'scripts/yara_scanner.py'])  # Launch GUI separately
        return jsonify({'status': 'success', 'message': 'YARA Scanner GUI launched successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to launch YARA Scanner: {str(e)}'})

# Show available Volatility reports
@app.route('/volatility-reports')
def volatility_reports():
    files = []
    if os.path.exists(app.config['VOL_OUT']):
        files = [f for f in os.listdir(app.config['VOL_OUT']) if os.path.isfile(os.path.join(app.config['VOL_OUT'], f))]
    return render_template('files.html', tool='volatility', files=files)

# Show YARA logs
@app.route('/yara-logs')
def yara_logs():
    files = []
    if os.path.exists(app.config['YARA_OUT']):
        files = [f for f in os.listdir(app.config['YARA_OUT']) if os.path.isfile(os.path.join(app.config['YARA_OUT'], f))]
    return render_template('files.html', tool='yara', files=files)

# Serve output files
@app.route('/view/<tool>/<filename>')
def view_file(tool, filename):
    folder = app.config['VOL_OUT'] if tool == 'volatility' else app.config['YARA_OUT']
    file_path = os.path.join(folder, filename)
    
    if not os.path.exists(file_path):
        return "File not found", 404
    
    # Check if it's a text file that should be displayed in browser
    text_extensions = ['.txt', '.log', '.json', '.csv', '.html']
    if any(filename.lower().endswith(ext) for ext in text_extensions):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{filename}</title>
                <style>
                    body {{ font-family: 'Courier New', monospace; margin: 20px; background: #f8f9fa; }}
                    .content {{ background: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    .header {{ background: #007bff; color: white; padding: 10px 20px; margin: -20px -20px 20px -20px; border-radius: 5px 5px 0 0; }}
                    pre {{ white-space: pre-wrap; word-wrap: break-word; }}
                </style>
            </head>
            <body>
                <div class="content">
                    <div class="header">
                        <h3>{filename}</h3>
                    </div>
                    <pre>{content}</pre>
                </div>
            </body>
            </html>
            """
        except Exception as e:
            return f"Error reading file: {str(e)}", 500
    
    return send_from_directory(folder, filename)

# API endpoint to check if tools are running
@app.route('/api/tool-status')
def tool_status():
    # This is a simplified check - in a real implementation you'd track actual process status
    return jsonify({
        'volatility': 'ready',
        'yara': 'ready'
    })

# API endpoint to get recent activity
@app.route('/api/recent-activity')
def recent_activity():
    activities = [
        {
            'action': 'System initialized',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'info'
        },
        {
            'action': 'YARA rules loaded successfully',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'success'
        },
        {
            'action': 'Volatility3 framework ready',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'success'
        }
    ]
    return jsonify(activities)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
