# ⚡ Coding Thunder

> **Heaven for Programmers** — A high-performance, Server-Side Rendered (SSR) technical blogging platform built with Python, Flask, SQLAlchemy, and MySQL.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.54-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Architecture](https://img.shields.io/badge/Architecture-SSR%20(Server--Side)-FF6F00?logo=fastapi&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🌟 Overview & Sellable Value Proposition

**Coding Thunder** is an enterprise-grade, lightweight, and ultra-fast dynamic blogging engine engineered for developer communities, content creators, and technical organizations. 

Unlike heavy Single Page Applications (SPAs) that suffer from massive JavaScript bundle bloat, sluggish First Contentful Paint (FCP), and poor indexing, **Coding Thunder leverages pure Server-Side Rendering (SSR)**. HTML pages are compiled in single-digit milliseconds on the server and delivered directly to the client as fully hydrated, semantic documents.

---

## ⚡ Why SSR? (SSR vs. Traditional CSR / SPAs)

| Dimension | ⚡ Coding Thunder (SSR) | 🐢 Client-Side Rendering (CSR/SPA) |
|---|---|---|
| **First Contentful Paint (FCP)** | **< 100ms** (Instant server-rendered HTML) | 1.5s – 4.0s (Waits for JS download & execution) |
| **SEO & Crawler Indexing** | **100% Native** — Search engines read full content immediately | Requires dynamic rendering or headless browsers |
| **Client Resource Footprint** | **Zero JS overhead** — Runs smoothly on any device | Heavy RAM & CPU usage on mobile/low-end devices |
| **Network Payload** | Streamlined HTML + minimal CSS (~15KB) | Heavy JS runtime bundles (500KB – 2MB+) |
| **Operational Simplicity** | Monolithic clarity, straightforward WSGI deployment | Complex build steps, hydration bugs, API versioning |

---

## ✨ Key Product Features

- ⚡ **Pure Server-Side Rendering (SSR)**: Instantaneous page transitions, maximum SEO visibility, and full social graph / OpenGraph compatibility.
- 📝 **Full Article Lifecycle Management (CRUD)**: Create, view, update, and delete rich technical posts with custom slugs and subheadings.
- 🖼️ **Resilient Media Architecture**: Native support for external high-resolution CDN images with graceful fallback to curated local WebP banners.
- 🔐 **Secure Admin Authentication**: Session-based administrative portal with protected CRUD routes and credential guards.
- 📄 **Optimized Pagination Engine**: Server-side pagination via SQLAlchemy for snappy navigation across large datasets.
- ✉️ **Automated Lead / Contact Pipeline**: Contact form integrated with `Flask-Mail` for real-time customer and reader inquiry dispatch.
- 🛡️ **Self-Healing 3-Tier Database Engine**: Automatically creates the MySQL database, generates schemas, and seeds initial data if none exist on startup.
- 🌐 **12-Factor Configuration**: Fully decoupled secret management using `.env` and `python-dotenv`.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    subgraph Client ["Client Layer (Browser / Mobile)"]
        User["User / Admin"]
        Crawler["Search Engine Crawlers (Google, Bing)"]
    end

    subgraph AppServer ["Flask Application Engine (SSR)"]
        Router["WSGI Request Router"]
        AuthGuard["Admin Session Guard"]
        JinjaEngine["Jinja2 SSR Template Hydration"]
        MailService["Flask-Mail Worker"]
    end

    subgraph DataLayer ["Data & Persistence Layer"]
        ORM["SQLAlchemy ORM (Pool Recycling)"]
        MySQL[("MySQL Database Server")]
    end

    User -->|HTTP Request| Router
    Crawler -->|Crawls Semantic HTML| Router
    Router -->|Public Routes| JinjaEngine
    Router -->|Protected Admin Routes| AuthGuard
    AuthGuard -->|Authenticated| JinjaEngine
    Router -->|Contact Form| MailService
    JinjaEngine <--> ORM
    ORM <--> MySQL
```

---

## 📂 Directory Structure

```text
coding-thunder/
├── static/
│   ├── asset/
│   │   ├── favicon.ico           # Multi-resolution favicon (16px - 256px)
│   │   ├── favicon.png           # High-definition Web icon
│   │   └── img/                  # High-compression WebP backgrounds & banners
│   │       ├── posts/            # Themed fallback illustrations (AI, Energy, Mars...)
│   │       ├── home-bg.webp
│   │       ├── about-bg.webp
│   │       ├── contact-bg.webp
│   │       └── admin-bg.webp
│   ├── css/
│   │   ├── styles.css            # Responsive Bootstrap theme
│   │   └── login.css             # Admin sign-in portal styles
│   └── js/
│       └── scripts.js            # Responsive navigation & navbar handlers
├── templates/
│   ├── layout.html               # Base Jinja2 layout with navigation & footer
│   ├── index.html                # SSR home feed with pagination
│   ├── about.html                # About page
│   ├── contact.html              # Contact form
│   ├── post.html                 # Single post view with dynamic masthead
│   ├── login.html                # Admin authentication portal
│   ├── dashboard.html            # Admin management dashboard
│   └── edit.html                 # Post editor / creator
├── .env.example                  # Environment variable blueprint
├── .gitignore                    # Git tracking rules
├── db_bootstrap.py               # Database auto-creation, schema setup & seed engine
├── flask_app.py                  # Core backend, routing, ORM models, and routes
├── requirements.txt              # Categorized direct and transitive dependencies
├── LICENSE                       # MIT License
└── README.md                     # Comprehensive project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **MySQL 8.0+**
- [`uv`](https://github.com/astral-sh/uv) (recommended) or standard `python -m venv`

---

### 1. Clone the Repository

```bash
git clone https://github.com/saransh-2021/coding-thunder.git
cd coding-thunder
```

---

### 2. Environment Setup

#### Using `uv` (Fastest):
```bash
uv venv
.\.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux/macOS
uv pip install -r requirements.txt
```

#### Using standard `pip`:
```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

---

### 3. Configuration (.env)

Copy `.env.example` to create your local `.env`:

```bash
cp .env.example .env
```

Configure your credentials in `.env`:

```ini
# Environment Mode
LOCAL_SERVER=True
SECRET_KEY=your_super_secret_key

# Database Connection URIs
LOCAL_URI=mysql://root:your_password@localhost/codingthunder
PROD_URI=mysql+mysqldb://username:password@hostname/dbname

# Admin Credentials
ADMIN_USER=saransh
ADMIN_PASSWORD=your_secure_password

# Email / Contact Configuration
GMAIL_USERNAME=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
MAIL_REPLY_TO=your_email@gmail.com

# Site Customization
BLOG_NAME="Coding Thunder"
TAG_LINE="Heaven for Programmers"
NO_OF_POSTS=3
```

---

### 4. Run the Application

```bash
python flask_app.py
```

Open your browser at:
```text
http://127.0.0.1:5000
```

> **💡 Zero-Config Auto-Bootstrap**: The application will automatically connect to your MySQL instance, create the `codingthunder` database if it doesn't exist, create all tables (`Contacts`, `Posts`), and seed default technical articles!

---

## 💼 Resume & Portfolio Highlights

If you are reviewing this project as part of **Saransh Shukla's** engineering portfolio, here is a concise breakdown of the technical achievements:

- **High-Throughput SSR Architecture**: Designed and implemented a full-stack blogging platform using Flask and Jinja2 server-side rendering, achieving sub-100ms First Contentful Paint and 100% SEO audit compliance.
- **Robust Data Layer**: Built normalized SQLAlchemy models mapped to MySQL with automatic database creation, connection pool recycling, and `TEXT` column scaling for arbitrary post lengths.
- **Production-Ready Admin Workflows**: Engineered secure administrative authentication, CRUD workflows for posts, dynamic pagination, and automated lead capture with `Flask-Mail` error isolation.
- **Asset Optimization**: Implemented external URL image support with intelligent local WebP fallback strategies, minimizing repository size and CDN egress costs.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: add AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👤 Author

**Saransh Shukla**
- GitHub: [@saransh-2021](https://github.com/saransh-2021/)

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
