# Twitch Twitter Handle Scraper

A web application that scrapes Twitter handles from Twitch channel pages. Upload a CSV of Twitch usernames and get back a CSV with their corresponding Twitter handles.

## Features

- 📁 Upload CSV files with Twitch usernames
- 🔍 Scrapes Twitter handles from Twitch channel pages
- 💾 Download results as CSV
- 🎨 Simple, modern web UI
- 🚀 Runs locally on your machine

## Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. (Optional) If you want to use Selenium for JavaScript-rendered pages, you'll also need ChromeDriver:
   - Download from: https://chromedriver.chromium.org/
   - Or install via: `brew install chromedriver` (macOS) or `apt-get install chromium-chromedriver` (Linux)

### Running the Application

1. Start the Flask server:

```bash
python app.py
```

2. Open your web browser and navigate to:

```
http://127.0.0.1:5000
```

## Usage

1. **Prepare your CSV file**: Create a CSV file with Twitch usernames in the first column. Example:

```csv
TheoryForge
ninja
shroud
```

2. **Upload the CSV**: Click the upload area or drag and drop your CSV file.

3. **Process**: Click the "Process CSV" button. The scraper will visit each Twitch channel page and extract the Twitter handle.

4. **Download Results**: Once processing is complete, click "Download Results" to get a CSV file with the Twitch usernames and their corresponding Twitter handles.

### Options

- **Use Selenium**: Check this box if the basic scraper doesn't work (Twitch pages are JavaScript-rendered). Requires ChromeDriver to be installed.

## CSV Format

### Input CSV
Your input CSV should have Twitch usernames in the first column:

```csv
username1
username2
username3
```

### Output CSV
The output CSV will have two columns:

```csv
Twitch Username,Twitter Handle
username1,@twitterhandle1
username2,Not found
username3,@twitterhandle3
```

## How It Works

The scraper:
1. Takes a list of Twitch usernames from your CSV
2. Visits each Twitch channel page (e.g., `twitch.tv/username`)
3. Searches for Twitter links in the page HTML
4. Extracts the Twitter handle from the link URL
5. Returns results in a CSV format

The scraper looks for links with the pattern `https://twitter.com/username` in the page's HTML structure.

## Troubleshooting

- **"Not found" results**: Some Twitch users may not have Twitter accounts linked, or the page structure may have changed.
- **Selenium errors**: Make sure ChromeDriver is installed and in your PATH if using the Selenium option.
- **Rate limiting**: The scraper includes delays between requests to be respectful. If you're scraping many users, the process may take some time.

## Notes

- The scraper includes a 1-second delay between requests to be respectful to Twitch's servers.
- Twitch pages are JavaScript-rendered, so you may need to use the Selenium option for best results.
- This tool is for personal use. Make sure to comply with Twitch's Terms of Service and robots.txt.

## License

This project is provided as-is for personal use.

