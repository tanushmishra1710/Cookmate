# 🍳 CookMate

A lightweight, full-stack recipe generator web application built with **Python Flask**. Users register, log in, enter the ingredients they have on hand, pick a cuisine style, and instantly receive a real, properly named recipe with step-by-step cooking instructions — no API keys or internet connection required.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
- [How It Works](#how-it-works)
- [Supported Cuisines & Dishes](#supported-cuisines--dishes)
- [Routes Reference](#routes-reference)
- [Database Schema](#database-schema)
- [Theme System](#theme-system)
- [Customisation](#customisation)
- [Known Limitations](#known-limitations)

---

## Features

- **User authentication** — secure registration and login with hashed passwords
- **Ingredient tag input** — interactive tag-based ingredient entry (press Enter or comma to add, × to remove)
- **Visual cuisine selector** — clickable emoji cards for 5 cuisine styles
- **Rule-based recipe matching** — matches ingredients to real dish names using a scored trigger system
- **Graceful fallback** — generates a sensibly named generic dish when no exact match is found
- **Three-mode theme system** — Light, Dark, and System (follows OS preference), persisted in `localStorage`
- **Responsive design** — works on desktop and mobile
- **No external API dependencies** — fully self-contained, runs offline

---

## Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | Python 3, Flask                   |
| Auth      | Werkzeug (`generate/check_password_hash`) |
| Database  | SQLite 3 (file-based, zero config)|
| Frontend  | Jinja2 templates, Vanilla JS      |
| Styling   | Custom CSS with CSS variables     |
| Fonts     | Google Fonts (Cormorant Garamond + Outfit) |

---

## Project Structure

```
cookmate/
│
├── app.py                  # Flask application — routes, recipe logic, DB helpers
├── database.db             # SQLite database (auto-created on first run)
│
├── templates/
│   ├── base.html           # Shared navbar, theme toggle (extended by dashboard pages)
│   ├── home.html           # Public landing page
│   ├── login.html          # Login page (split-screen layout)
│   ├── register.html       # Registration page (split-screen layout)
│   └── dashboard.html      # Main recipe generator (requires login)
│
└── static/
    └── css/
        └── style.css       # All styles — theme variables, components, animations
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- `pip` package manager

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/cookmate.git
cd cookmate
```

**2. Create and activate a virtual environment** *(recommended)*

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install flask werkzeug
```

> No other packages are required. There are no AI or third-party API dependencies.

### Running the App

```bash
python app.py
```

The database (`database.db`) and the `users` table are created automatically on first run.

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

## How It Works

### Recipe Matching

Every recipe in the built-in database has a list of **trigger ingredients** (lowercase keywords). When a user submits their ingredients and cuisine, the app:

1. Converts all user ingredients to lowercase.
2. Scores every recipe in the chosen cuisine by counting how many of its triggers appear in the user's ingredient list.
3. Returns the recipe with the highest score.

**Example:**
- User enters: `paneer, butter, tomato` → cuisine: `Indian`
- Best match: **Paneer Butter Masala** (all 3 triggers match)

### Fallback Logic

If no recipe scores above zero (i.e. none of the triggers match), a generic dish is constructed on the fly:

- Ingredients are sorted by cooking priority (aromatics → vegetables → proteins).
- A sensible name is assembled: `{main ingredient} & {base ingredient} {cuisine suffix}` — e.g. *Paneer & Onion Masala*.
- Generic step-by-step instructions are generated from the sorted ingredient list.

### Password Security

Passwords are never stored in plain text. `werkzeug.security.generate_password_hash` applies PBKDF2-HMAC-SHA256 hashing before saving to the database.

---

## Supported Cuisines & Dishes

| Cuisine  | Sample Dishes                                            |
|----------|----------------------------------------------------------|
| 🍛 Indian  | Paneer Butter Masala, Chicken Curry, Aloo Sabzi, Mushroom Masala, Gajar Ki Sabzi |
| 🥢 Chinese | Kung Pao Chicken, Mapo Tofu, Chinese Vegetable Stir-Fry, Chinese Garlic Chicken |
| 🍝 Italian | Penne Arrabbiata with Mushrooms, Chicken Cacciatore, Mushroom Risotto, Pasta Pomodoro |
| 🍜 Japanese| Miso Soup with Tofu & Mushrooms, Chicken Teriyaki, Yasai Itame, Nikujaga |
| 🌮 Mexican | Veggie Tacos with Salsa Roja, Pollo a la Mexicana, Paneer Fajitas, Papas Guisadas |

Each cuisine has 4–6 recipes. New dishes can be added to the `RECIPES` dictionary in `app.py` without changing any other code — see [Customisation](#customisation).

---

## Routes Reference

| Method | Route              | Auth Required | Description                                  |
|--------|--------------------|---------------|----------------------------------------------|
| GET    | `/`                | No            | Landing page (adapts for logged-in users)    |
| GET    | `/register`        | No            | Registration form                            |
| POST   | `/register`        | No            | Create new user account                      |
| GET    | `/login`           | No            | Login form                                   |
| POST   | `/login`           | No            | Authenticate and start session               |
| GET    | `/dashboard`       | Yes           | Recipe generator dashboard                   |
| POST   | `/generate-recipe` | Yes           | Submit ingredients and receive recipe        |
| GET    | `/logout`          | Yes           | Clear session and redirect to login          |

---

## Database Schema

A single table, automatically created on startup:

```sql
CREATE TABLE IF NOT EXISTS users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email    TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL        -- bcrypt/PBKDF2 hash, never plain text
);
```

The database file `database.db` is created in the project root directory on first run.

---

## Theme System

CookMate supports three colour modes, toggled by clicking the **🌙 / ☀️ / 💻** button in the top-right navbar:

| Mode   | Icon | Behaviour                                    |
|--------|------|----------------------------------------------|
| Light  | 🌙   | Pale mint greens and whites                  |
| Dark   | ☀️   | Deep forest greens and dark surfaces         |
| System | 💻   | Automatically follows your OS preference     |

The selected mode is stored in `localStorage` under the key `cm-theme` and applied immediately on page load to prevent any flash of unstyled content. Cycling order: **Light → Dark → System → Light…**

---

## Customisation

### Adding a new recipe

Open `app.py` and add an entry to the `RECIPES` dictionary under the relevant cuisine:

```python
{
    "triggers": ["keyword1", "keyword2", "keyword3"],  # lowercase
    "title": "Real Dish Name",
    "base_steps": [
        "Step one instructions.",
        "Step two instructions.",
        # ...
    ],
},
```

The trigger keywords should be lowercase versions of the main ingredients. The more triggers that overlap with the user's input, the higher the match score.

### Adding a new cuisine

1. Add a new key to the `RECIPES` dict in `app.py` with its list of recipe entries.
2. Add a button for it in `dashboard.html` inside the `.cuisine-grid` loop:
   ```html
   ('🥗', 'NewCuisine')
   ```
3. Add the cuisine suffix to the fallback `suffix` dict in `build_recipe()`:
   ```python
   "NewCuisine": "Dish Suffix",
   ```

### Changing the secret key

Replace the hardcoded value in `app.py` with an environment variable for production:

```python
import os
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-dev-key')
```

---

## Known Limitations

- **Single-file SQLite database** — suitable for development and small personal deployments. For production use, consider migrating to PostgreSQL or MySQL with connection pooling.
- **Session-based auth only** — there is no "remember me", password reset, or email verification flow.
- **No pagination** — all recipe steps are rendered in a single page response.
- **Recipe database is hardcoded** — recipes live in `app.py`. A future improvement would be to move them into the SQLite database for easier management.
- **Debug mode is on by default** — set `debug=False` or use a proper WSGI server (e.g. Gunicorn) before deploying to production.

---

## License

This project is open source and available under the [MIT License](LICENSE).
