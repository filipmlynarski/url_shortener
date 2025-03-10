# URL Shortener Service

A URL shortening service built with Django and Django REST Framework.

## Features

- Shorten long URLs to short links
- Track visit analytics for each shortened URL

## Tech Stack

- **Backend**: Django 5.1, Django REST Framework
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **Testing**: pytest, Django Test Framework
- **Code Quality**: ruff

### Running the Application

1. Clone the repository:
   ```bash
   git clone git@github.com:filipmlynarski/url_shortener.git
   ```

2. Start the application with Docker Compose:
   ```bash
   docker compose up
   ```

3. The application will be available at http://localhost:8000

### API Endpoints

#### URL Shortener

- `POST /shortener/`: Create a new shortened URL
  ```json
  {
    "original_url": "https://example.com/very/long/url/that/needs/shortening"
  }
  ```

- `GET /shortener/`: List all shortened URLs
- `GET /shortener/{short_code}/`: Get details for a specific shortened URL
- `PUT /shortener/{short_code}/`: Update a shortened URL
- `DELETE /shortener/{short_code}/`: Delete a shortened URL

#### URL Redirection

- `GET /{short_code}/`: Redirects to the original URL and records the visit

#### Analytics

- `GET /analytics/{short_code}/`: Get visit statistics for a shortened URL

## Development

### Running Tests

```bash
docker compose run web pytest src/tests/
```

### Code Quality

```bash
docker compose run web ruff check . --config pyproject.toml
```

### Formatting

```bash
docker compose run web ruff check . --config pyproject.toml --fix
```

## Project Configuration

Additional configuration options can be found in `src/url_shortener/settings.py`:

- `URL_SHORTENER_LENGTH`: Length of generated short codes (default: `6`)

