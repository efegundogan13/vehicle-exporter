# Vehicle Exporter (Baubuddy API Task Project)

This project processes vehicle data fetched from the Baubuddy API and compares it with a local CSV file. It extracts only the vehicles that match by `rnr` and have a valid inspection date (`hu`), then exports them into a well-formatted Excel file. If vehicles have `labelIds`, those are resolved into label names and colors.

## 📁 Project Structure

- `test.py`: A preliminary script to inspect the API data and log which vehicles have `hu` and/or `labelIds`. This was used to identify conflicts and filtering criteria before the main logic.
- `server/main.py`: Flask server that handles CSV upload, fetches vehicle data from Baubuddy API, filters based on `hu` and `rnr`, and resolves `labelIds`.
- `client.py`: Sends the CSV to the server, receives the processed vehicle data, and generates an Excel file according to user-defined keys and coloring options.
- `requirements.txt`: Lists all required Python libraries.
- `vehicles.csv`: Example CSV file containing local vehicle `rnr` data.

## 🚧 Highlights

- Only vehicles that exist in the CSV **and** contain a valid `hu` value are included.
- Most vehicles either have `hu` or `labelIds`, but not both — this led to natural filtering.
- `test.py` was used to inspect and confirm that `hu` and `labelIds` rarely co-occur.
- The main export logic reflects these API constraints.

## ⚙️ Usage

### 1. Install dependencies
```bash
pip install -r requirements.txt
