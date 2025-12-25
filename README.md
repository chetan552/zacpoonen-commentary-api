# Zac Poonen Commentary API

A Django REST API for accessing Zac Poonen Bible Commentary data.

## Description

This project provides a RESTful API to access Bible commentaries by Zac Poonen. The API allows retrieving commentaries by book and chapter, and includes an admin interface for importing commentary data.

## Tech Stack

- **Python**: 3.12+
- **Django**: 5.0+
- **Django REST Framework**: 3.16+

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/zac-poonen-commentary-api.git
   cd zac-poonen-commentary-api
   ```

2. **Install dependencies**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Populate books data**:
   ```bash
   python manage.py populate_books
   ```

5. **Import commentary data (optional, if you have a JSON file)**:
   ```bash
   python manage.py import_commentaries path/to/commentaries.json
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`.

## Docker Usage

Container images make it easy to run the API without installing Python locally.

### Build

```bash
docker build -t zacpoonen-commentary-api .
```

### Run with Docker Compose

```bash
docker compose up --build
```

The compose file now bootstraps only the Django API container. Provide your Supabase (or other external) Postgres connection string via `DATABASE_URL` in `.env`—the container automatically loads that file for all environment variables, so you can also place values such as `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` there. Because the container runs migrations before starting Gunicorn, the API is available at `http://127.0.0.1:8000/` as soon as the remote database is reachable.

## API Endpoints

### Get Commentaries
Retrieve commentaries for a specific book and chapter.

- **Endpoint**: `GET /api/commentaries/{book}/{chapter}/`
- **Parameters**:
  - `book`: Book name (e.g., "Genesis") or abbreviation (e.g., "GEN")
  - `chapter`: Chapter number (integer)
- **Example**: `GET /api/commentaries/Genesis/1/`

Response example:
```json
[
  {
    "id": 1,
    "book": "Genesis",
    "chapter": 1,
    "verse": 1,
    "text": "In the beginning..."
  },
  ...
]
```

### Search Commentaries
Search commentary text (plus book name, abbreviation, and verse) with keyword + topical helpers.

- **Endpoint**: `GET /api/search/`
- **Parameters**:
  - `keyword`: Main search terms (space-separated); numeric values also match chapter numbers
  - `match`: `or` (default) or `and` to control whether all terms must match
  - `topics`: Comma-separated topic names to expand (built-in map: grace, faith, love, repentance, forgiveness)
  - `expand_topics`: `true|false` (default `true`) to expand `keyword` tokens that match topic names into their synonyms
- **Examples**:
  - `GET /api/search/?keyword=grace`
  - `GET /api/search/?keyword=faith love&match=and`
  - `GET /api/search/?topics=grace,faith`

### Import Commentaries
Import commentary data via JSON payload.

- **Endpoint**: `POST /api/import/`
- **Content-Type**: `application/json`
- **Body**: Array of commentary objects

Example payload:
```json
[
  {
    "book": "Genesis",
    "chapter": 1,
    "verse": 1,
    "text": "In the beginning God created the heaven and the earth."
  }
]
```

## Admin Interface

The Django admin interface is available at `/admin/`. You can use it to:

- Import commentaries via file upload (JSON files)
- Manage books and commentaries

Navigate to `/admin/` and log in with appropriate credentials.

## Data Models

### Book
- `name`: Full book name (e.g., "Genesis")
- `abbreviation`: Short form (e.g., "GEN")

### Commentary
- `book`: Foreign key to Book
- `chapter`: Chapter number
- `verse`: Verse number
- `text`: Commentary text

## Usage Examples

Using `curl` to fetch commentaries:

```bash
# Get Genesis chapter 1 commentaries
curl http://127.0.0.1:8000/api/commentaries/Genesis/1/

# Using abbreviation
curl http://127.0.0.1:8000/api/commentaries/GEN/1/
```

Using Python requests:
```python
import requests

response = requests.get('http://127.0.0.1:8000/api/commentaries/Genesis/1/')
data = response.json()
print(data)
```

## License

This project is open source. See LICENSE file for details.

## Deployment to Vercel

1. **Connect to Vercel**: Import your GitHub repository to Vercel
2. **Environment Variables**: Set the following in Vercel's environment variables:
   - `DJANGO_SECRET_KEY`: Generate a new secret key for production
   - `DJANGO_DEBUG`: Set to `false` for production
3. **Deploy**: Vercel will automatically detect the `vercel.json` configuration and deploy the Django app
4. **Database**: SQLite database is included in the deployment. For larger datasets, consider using Vercel Postgres or another database service.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
