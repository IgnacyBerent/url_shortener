<h1>URL Shortener</h1>

## Overview
The URL Shortener is a web application that allows users to shorten long URLs into more manageable links. It provides both a frontend interface and a RESTful API for creating and managing shortened URLs.

## Installation
To set up the project locally, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/urlshortener.git
    cd urlshortener
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```

3. **Add .env file**:
    Create a `.env` file in the urlshortener/urlshortener directory of the project and add the following environment variables:
    ```sh
    DJANGO_SECRET=django_secret
    DEBUG=1
    POSTGRES_DB=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    PORT=5432
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations**:
    ```sh
    python manage.py migrate
    ```

5. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

## Usage
To use the URL Shortener, navigate to `http://127.0.0.1:8000/` in your web browser. You can create a new shortened URL by entering the long URL in the provided form. You can also see swaggers documentation by navigating to /swagger

## API Endpoints
The application provides the following API endpoints:

- **Create Shortened URL**: `POST /api/shorten/`
- **Retrieve Shortened URL**: `GET /api/shorten/<short_code>/`
- **List All Shortened URLs**: `GET /api/shorten/`

## Testing
To run the tests, use the following command:
```sh
python manage.py test