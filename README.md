# FastAPI Customer Support Ticketing System (Dockerized)

This project is a **Support Ticketing System** built using **FastAPI** and **PostgreSQL**, fully containerized with **Docker Compose**. It includes database migrations using Alembic.

## Prerequisites

Ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Project Structure

```
.
├── app/                   # FastAPI application
├── alembic/               # Alembic migration files
│   ├── versions/          # Migration history
├── database.py            # Database configuration
├── main.py                # FastAPI application entry point
├── Dockerfile             # Defines the FastAPI app container
├── docker-compose.yml     # Docker Compose configuration
├── alembic.ini            # Alembic configuration
├── .env                   # Environment variables
└── README.md              # Documentation
```

## Environment Variables

Create a `.env` file in the root directory with the following content:

```
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=password
MAIL_FROM=your_email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_STARTTLS=False
MAIL_SSL_TLS=True
DATABASE_URL=postgresql://postgres:password@postgres_container:5432/database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=database
```

## Running the Project

1. **Clone the repository:**

   ```sh
   git clone git@github.com:Ayalwm/customer_ticket.git
   cd customer_ticket
   ```

2. **Start the containers:**

   ```sh
   docker compose up --build -d
   ```

   This will:

   - Start a PostgreSQL container (`postgres_container`)
   - Start the FastAPI application (`fastapi_app`)
   - Apply database migrations automatically

3. **Check logs (optional):**

   ```sh
   docker compose logs -f
   ```

4. **Access the API:**
   The FastAPI app will be running at: [http://localhost:8000](http://localhost:8000)

5. **API Documentation:**
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Database Migrations

To manage database migrations inside the FastAPI container:

- **Create a new migration:**

  ```sh
  docker compose exec fastapi_app alembic revision --autogenerate -m "migration_message"
  ```

- **Apply migrations:**

  ```sh
  docker compose exec fastapi_app alembic upgrade head
  ```

- **Downgrade migrations (rollback):**
  ```sh
  docker compose exec fastapi_app alembic downgrade -1
  ```

## Stopping & Removing Containers

To stop and remove all containers, volumes, and networks:

```sh
docker compose down -v
```

## Notes

- If you face migration issues, you can reset the migration history by deleting the `versions/` folder inside `alembic/` and dropping the `alembic_version` table in PostgreSQL:
  ```sh
  docker compose exec db psql -U postgres -d ticket_db -c "DROP TABLE IF EXISTS alembic_version;"
  ```
  Then, re-run migrations.

## License

This project is open-source and available under the MIT License.
