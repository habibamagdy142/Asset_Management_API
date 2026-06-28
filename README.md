# Asset Management API

Backend API for managing and tracking digital assets.

Built using:

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy


## Features

- Asset CRUD operations
- Asset filtering and pagination
- API key authentication for write operations
- Input validation using Pydantic schemas
- Directed asset relationship management
- Bulk asset import
- Deduplication during import
- Automated tests

## Project Structure
```text

├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── dependencies.py
│   │
│   ├── routers/
│   │   ├── assets.py
│   │   ├── relationships.py
│   │   └── import_data.py
│   │
│   └── tests/
│       └── test_assets.py
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── sample_assets.json
└── requirements.txt 

```
## Design Decisions & Assumptions

- Deduplication key: assets are matched by `(type, value)`. If a re-imported
  asset has a different `id` than the stored one, the stored `id` is kept
  (the original record is preserved; only `last_seen`, `tags`, `metadata`,
  and `status` are merged).
- Stale assets: marked manually via `PATCH /assets/{id}/mark-stale`, or
  automatically reset to `active` whenever the same asset re-appears in an
  import.
- Tag merge strategy on conflict: union of existing + incoming tags.
  Metadata merge strategy: incoming metadata overwrites matching keys,
  other existing keys are preserved (shallow merge).
- Relationships are directional (source → target) and deduplicated.
- Database schema is initialized using SQLAlchemy metadata creation.
  For this internship task, this approach is sufficient. Alembic migrations
  can be added for production schema evolution.
## Setup



### 1. Create virtual environment

```bash
python -m venv .venv
```


### 2. Activate environment

Windows:

```bash
.venv\Scripts\activate
```


### 3. Install dependencies

```bash
pip install -r requirements.txt
```


### 4. Configure database

Create PostgreSQL database:


asset_db


Update database URL in environment variables.


Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/asset_db
```
### Configure Environment Variables

Create a `.env` file based on `.env.example`:

```env
API_KEY=your-secret-key
DATABASE_URL=postgresql://username:password@localhost:5432/asset_db
```
The `.env` file contains local secrets and should not be committed to version control.
## Run Application
### Local Development

```bash
uvicorn app.main:app --reload
```
### Docker

Run the application using:

```bash
docker compose up --build
```
Docker Compose starts both the FastAPI application and PostgreSQL database service.



### API documentation:

```text
http://127.0.0.1:8000/docs
```

## Authentication

Write operations require an API key.

Header:

```text
x-api-key: <API_KEY_VALUE_FROM_ENV>
```
The API key is loaded from environment variables and should not be stored in source code.
## Error Handling

The API uses standard HTTP status codes:

- 200: Successful request
- 401: Invalid or missing API key
- 404: Resource not found
- 422: Validation error
## API Endpoints

### Assets

- POST `/assets/` - Create asset
- GET `/assets/` - List assets
- GET `/assets/{id}` - Get asset
- PUT `/assets/{id}` - Update asset
- DELETE `/assets/{id}` - Delete asset
- PATCH `/assets/{id}/mark-stale` - Mark asset as stale

### Relationships

- POST `/relationships/` - Create asset relationship
- GET `/relationships/{asset_id}` - Get related assets

### Import

- POST `/import/` - Import assets from JSON file (requires API key)

## Import Assets

Example JSON:

```json
[
  {
    "type": "domain",
    "value": "example.com",
    "status": "active",
    "source": "scan",
    "tags": [
      "external"
    ],
    "metadata": {}
  }
]
```
Upload the JSON file using:

```text
POST /import/
```
The endpoint accepts a JSON file containing a list of assets.
## Testing

Run tests using:

```bash
pytest
```
The test suite covers:

- Asset creation and retrieval
- Asset update and deletion
- API key authentication
- Asset filtering
- Bulk import
- Deduplication logic
- Relationship creation and import relationships