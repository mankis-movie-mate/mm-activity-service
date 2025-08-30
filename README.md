# mm-activity-service
Tracks user interactions.

## ⚙️ Environment Variables

Environment variables are defined in `.env.example`.

- Copy `.env.example` to `.env`
- Fill in the required values for your local or production setup

## 📄 API Documentation

- **Swagger UI:** `${config.BASE_URL}/docs/swagger-ui`

_Replace `${config.BASE_URL}` with deployment context (e.g. `/api/user`)._

## 🚀 Running Locally
1. Install dependencies:
   ```bash
   poetry install
   ```
2. Run the application:
   ```bash
   poetry run start
   ```