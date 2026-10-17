# EchoRoute · Backend

REST API for EchoRoute, a field operations platform for delivery and sales teams. Drivers check in at each client by scanning a QR code, the API records the visit with GPS coordinates and validates the distance to the client, and admins get dashboards, maps and Excel reports. It is used in production by a distribution company.

The web app lives in [EchoRoute_FrontEnd](https://github.com/ErickMontesDK/EchoRoute_FrontEnd). **Live demo:** [echoroute-wine.vercel.app](https://echoroute-wine.vercel.app/) (read-only, `admin` / `echo1234`).

## Features

- **JWT authentication** (SimpleJWT) with login, refresh and logout
- **Roles and permissions:** Admin, Operator and Delivery users
- **Clients, routes and visits** with soft delete and restore
- **Visit validation:** the distance between the recorded GPS point and the client is computed with the haversine formula and checked against a configurable maximum
- **Business settings:** max valid distance, units and branding, configurable per deployment
- **Dashboard stats and Excel exports** (openpyxl)
- **Demo mode:** a middleware that makes the whole API read-only for public demos

## Stack

Python 3.11 · Django 5 · Django REST Framework · PostgreSQL · Gunicorn · WhiteNoise · Docker · deployed on Render

## Data model

```
User (Admin / Operator / Delivery)
 └─ Route (deliverer, day of week)
     └─ Client (code, type, address, lat/lng)
         └─ Visit (deliverer, time, recorded lat/lng, distance, valid?, productive?)
```

## Main endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/api/auth/login/` | Get access and refresh tokens |
| GET | `/api/users/me/dashboard/` | Current user's dashboard |
| GET | `/api/users/dashboard/stats/` | Admin stats |
| GET/POST | `/api/clients/` | List or create clients |
| GET | `/api/clients/code/<code>/` | Look up a client by its QR code |
| GET | `/api/clients/map/` | Clients for the map view |
| GET/POST | `/api/visits/` | List or register visits |
| GET | `/api/visits/export/` | Export visits to Excel |

## Running locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Without `DATABASE_URL` it uses SQLite. With Docker:

```bash
docker build -t echoroute-api .
docker run -p 8000:8000 -e PORT=8000 -e DATABASE_URL=... -e SECRET_KEY=... echoroute-api
```

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for local development |
| `DATABASE_URL` | PostgreSQL connection string (SQLite if empty) |
| `FRONTEND_URL` / `BACKEND_URL` | Allowed origins and hosts |
| `DEMO_MODE` | `True` blocks every write except auth |
