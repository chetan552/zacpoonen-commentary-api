# Zac Poonen Commentary API

A Django REST API for accessing Zac Poonen Bible Commentary data.

## Description

This project provides a RESTful API to access Bible commentaries by Zac Poonen. The API allows retrieving commentaries by book and chapter, and includes an admin interface for importing commentary data.

## Tech Stack

- **Python**: 3.12+
- **Django**: 5.0+
- **Django REST Framework**: 3.16+
- **Poetry**: For dependency management

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/zac-poonen-commentary-api.git
   cd zac-poonen-commentary-api
   ```

2. **Install dependencies using Poetry**:
   ```bash
   poetry install
   ```

3. **Activate the virtual environment**:
   ```bash
   poetry shell
   ```

4. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Populate books data**:
   ```bash
   python manage.py populate_books
   ```

6. **Import commentary data (optional, if you have a JSON file)**:
   ```bash
   python manage.py import_commentaries path/to/commentaries.json
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`.

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
