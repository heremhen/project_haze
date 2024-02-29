# Project Haze

## Prerequisites

- Python 3.11.x

## Installation

### Set up Python environment

``bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # For MacOS/Linux, use source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the script locally

```bash
rav run migration.revision
rav run migration.sync
rav run dev
```

Once the service is up and running, you can open your browser and go to `http://127.0.0.1:5000/` and execute `POST:health` option to check if the database is `up` and running.