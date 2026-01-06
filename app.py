from flask import Flask, render_template, request, jsonify, send_file
import csv
import io
from scraper import scrape_twitch_usernames
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'File must be a CSV'}), 400
        
        # Read CSV file
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        
        # Extract usernames from CSV column titled 'twitch_username'
        usernames = []
        for row in csv_input:
            if 'twitch_username' in row and row['twitch_username'].strip():
                usernames.append(row['twitch_username'].strip())
        
        if not usernames:
            return jsonify({'error': 'No usernames found in CSV'}), 400
        
        # Scrape Twitter handles (Twitch pages are JavaScript-rendered, so we use Selenium)
        results = scrape_twitch_usernames(usernames, use_selenium=True)
        
        # Create output CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Twitch Username', 'Twitter Handle'])
        for result in results:
            writer.writerow([result['twitch_username'], result['twitter_handle']])
        
        output.seek(0)
        
        # Save to temporary file
        output_filename = 'output.csv'
        with open(output_filename, 'w', newline='', encoding='utf-8') as f:
            f.write(output.getvalue())
        
        return jsonify({
            'success': True,
            'message': f'Successfully scraped {len(results)} usernames',
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download')
def download_file():
    try:
        if os.path.exists('output.csv'):
            return send_file('output.csv', as_attachment=True, download_name='twitter_handles.csv')
        else:
            return jsonify({'error': 'No output file found. Please upload and process a CSV first.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

