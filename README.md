# Yandex Metrica Dashboard

Interactive analytics dashboard for website traffic using Yandex Metrica API.
Built with Python, SQLite and Streamlit, deployed on VPS with automated data collection.

## Features

* Daily traffic statistics (visits, users, pageviews)
* Search queries analysis
* Traffic sources breakdown
* Devices analytics
* Conversion tracking (goals)
* Average time on site visualization
* Period selection (7 / 30 / 90 / 365 days)
* Automated data collection (cron)
* Fast performance via SQLite storage

## Tech Stack

* Python
* Streamlit
* SQLite
* Requests (API)
* Pandas
* Plotly (optional for charts)
* VPS (Linux, systemd)
* Cron jobs

## Architecture

Yandex Metrica API
↓
Python collector (cron job)
↓
SQLite database
↓
Streamlit dashboard

## Installation

### 1. Clone repository

```bash
git clone https://github.com/your_username/yandex_metrica_dashboard.git
cd yandex_metrica_dashboard
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment variables

Create `.env` file:

```env
METRIKA_TOKEN=your_yandex_metrica_token
METRIKA_COUNTER_ID=your_counter_id
```

## Run project

### Collect data

```bash
python collector.py
```

### Start dashboard

```bash
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

## Automation (cron)

Example (every 30 minutes):

```bash
*/30 * * * * /path/to/python /path/to/collector.py >> collector.log 2>&1
```

## Dashboard Includes

* KPI metrics (visits, users, pageviews)
* Time series visualization
* Traffic sources with engagement (avg time)
* Device distribution
* Search queries performance
* Conversions (goals)

## Example Use Cases

* Marketing performance analysis
* Traffic quality monitoring
* Conversion tracking
* SEO and paid traffic insights
* Business reporting

## Screenshots

Add screenshots of your dashboard here

## Future Improvements

* Period comparison (like Yandex Metrica)
* User authentication
* Docker containerization
* Telegram notifications
* Advanced visualizations

## Author

Mykyta Driha

## Project Status

Production-ready MVP
Actively improving

