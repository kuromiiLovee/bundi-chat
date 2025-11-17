# **🔐 BundiChat Backend**

## **📌 Overview**

BundiChat backend is a fast, scalable, and privacy-focused chat server built with **FastAPI**, **Tortoise ORM**, **Docker**, and **uv** for dependency management.
It powers a real-time messaging platform with secure authentication, encrypted communication workflows, user avatars, and async performance optimized for production.

---

### **📂 Project Structure**

```
.
├── app/
│   ├── core/
|   ├── middleware/
│   ├── models/
|   ├── routers/
|   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── __init__.py
│
├── migrations/
├── .dockerignore
├── .env.example
├── .gitignore
├── .python-version
├── Dockerfile
├── README.md
├── docker-compose.yml
├── pyproject.toml
└── uv.lock
```

## **🛠️ Developer Instructions**
### **Prerequisites**
* 🐍 Python - v3.9+
* 🗃️ uv
* 🐋 Docker

### **🔧 Tech Stack**

* **FastAPI** — async high-performance API framework
*  **Tortoise ORM** — expressive async ORM
* **Docker & Docker Compose** — containerization and running multi-container Docker app, and deployment
* **uv** — dependency & environment manager
* **WebSockets** — real-time communication
* **PostgreSQL** — storage backend

---
**NOTE**

- Make sure you have installed Docker on your machine. Refer to [Docker's installation guide]() and follow a step-by-step guide on how you can install Docker on your OS. If you don't wish to use Docker, check `**NOTE**` section below.
- Make sure you have installed `uv` package manager. Refer to [uv's documentation]() for more info.

### Docker installation guide
- [Install Docker on Windows](https://docs.docker.com/desktop/setup/install/windows-install)
- Linux:
  - [Install Docker on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
  - [Install Docker on Debian](https://docs.docker.com/engine/install/debian/)
  - [Install Docker on Fedora](https://docs.docker.com/engine/install/fedora/)

- [Install Docker on macOS](https://docs.docker.com/desktop/setup/install/mac-install)

Once installed, check version using the following commands:

```bash
docker --version
docker compose version
```

---

Follow these steps to run the app successfully:

1. Clone the Project

```bash
git clone https://github.com/morikeli/bundi-chat.git
cd bundi-chat
```

2. Using uv
Install dependencies from pyproject.toml:

```bash
uv sync
```
If you wish to install new dependencies run this command:

```bash
uv add <package-name>
```

---

**NOTE**: You can also install multiple packages separated by spaces. For example:

```bash
uv add <package-1> <package-2> <package-3> <package-4>
```

If you don't wish to use Docker to run the app, you can use the following commands:

Run server:

```bash
uv run fastapi dev
```
You can also use this command to run the development server

```bash
uvicorn app:app --reload
```

API documentation is available at:

* Swagger UI → `http://localhost:8000/api/v1/docs`
* ReDoc → `http://localhost:8000/api/v1/redoc`

---

3. Run Using Docker Compose (Recommended)

Make sure Docker is installed in your local machine.

Build and start the container. In Linux, it requires sudo privileges to use docker commands. Therefore use `sudo` before each command:

```bash
docker compose up --build

# If you want to run the container in the background, use:
# docker compose up -d
```

To stop containers run this command:

```bash
docker compose down
```

To view logs, run this command:

```bash
docker compose logs -f
```

---
**Miscellaneous**

If you wish to apply linting or script formatting using uv, run the following commands:

#### **🧹 Linting & Formatting**

```bash
uv run ruff check .
uv run ruff format .
```

---

## **🤝 Contributions**

Contributions are welcome! 🎉

### How to contribute:

1. **Fork** the repo
2. **Create a feature branch**
3. Commit changes with clear messages
4. Submit a **pull request**
5. Follow existing code style & project structure

Open issues anytime for bugs, feature suggestions, or discussions.

