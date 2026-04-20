"""
CookMate – Flask application
No AI dependencies. Pure rule-based recipe matching.
"""

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = 'cookmate_secret_key'

# ---------------------------------------------------------------------------
# Recipe database
# Each cuisine holds a list of recipes.  Every recipe has:
#   triggers   – ingredient keywords used for matching (lowercase)
#   title      – real dish name shown to the user
#   base_steps – ordered cooking instructions
# ---------------------------------------------------------------------------

RECIPES = {
    "Indian": [
        {
            "triggers": ["paneer", "butter", "tomato"],
            "title": "Paneer Butter Masala",
            "base_steps": [
                "Heat butter in a pan and sauté finely chopped onions until golden.",
                "Add ginger-garlic paste and cook for 2 minutes until aromatic.",
                "Blend tomatoes into a smooth purée; add to the pan and cook until oil separates.",
                "Stir in red chilli powder, coriander powder, garam masala, and salt.",
                "Add cubed paneer and gently coat in the gravy.",
                "Pour in fresh cream and simmer on low heat for 5 minutes.",
                "Garnish with cream and chopped coriander. Serve with naan or rice.",
            ],
        },
        {
            "triggers": ["paneer", "onion", "tomato"],
            "title": "Paneer Masala",
            "base_steps": [
                "Heat oil; add a bay leaf and whole spices and let them splutter.",
                "Fry finely chopped onions to a deep golden brown.",
                "Add ginger-garlic paste and cook for 2 minutes.",
                "Add chopped tomatoes and cook until they break down.",
                "Stir in coriander powder, cumin powder, red chilli powder, and salt.",
                "Add cubed paneer; splash in water, cover, and simmer for 5 minutes.",
                "Finish with garam masala and fresh coriander. Serve with roti or rice.",
            ],
        },
        {
            "triggers": ["chicken", "tomato", "onion"],
            "title": "Chicken Curry",
            "base_steps": [
                "Heat oil; add whole spices and let them splutter.",
                "Fry finely chopped onions until deep golden brown.",
                "Add ginger-garlic paste and sauté for 2 minutes.",
                "Add chopped tomatoes and cook until completely broken down.",
                "Stir in turmeric, red chilli powder, coriander powder, and salt.",
                "Add chicken pieces, sear for 5 minutes, then add water.",
                "Cover and cook on medium heat for 20–25 minutes until tender.",
                "Finish with garam masala and fresh coriander. Serve with rice or roti.",
            ],
        },
        {
            "triggers": ["potato", "tomato", "onion"],
            "title": "Aloo Sabzi",
            "base_steps": [
                "Heat oil; add cumin seeds and let them splutter.",
                "Sauté chopped onions until translucent, then add ginger-garlic paste.",
                "Add chopped tomatoes and cook until mushy.",
                "Stir in turmeric, coriander powder, red chilli, and salt.",
                "Add diced potatoes with a splash of water; mix well.",
                "Cover and cook on medium-low for 15 minutes until potatoes are soft.",
                "Garnish with coriander and lemon juice. Serve with chapati.",
            ],
        },
        {
            "triggers": ["mushroom", "onion", "tomato"],
            "title": "Mushroom Masala",
            "base_steps": [
                "Heat oil and sauté onions until golden; add ginger-garlic paste.",
                "Add pureed tomatoes and cook until oil separates.",
                "Stir in cumin powder, coriander powder, red chilli powder, and salt.",
                "Add sliced mushrooms and toss to coat.",
                "Cook uncovered on medium heat for 8–10 minutes until tender.",
                "Stir in garam masala and cream. Serve with paratha or rice.",
            ],
        },
        {
            "triggers": ["carrot", "onion"],
            "title": "Gajar Ki Sabzi",
            "base_steps": [
                "Heat oil or ghee; add mustard seeds and curry leaves.",
                "Sauté finely chopped onions until soft.",
                "Add grated or diced carrots and stir well.",
                "Season with turmeric, red chilli powder, and salt.",
                "Cover and cook on low heat for 10 minutes until carrots are done.",
                "Finish with lemon juice and coriander. Serve with dal and rice.",
            ],
        },
    ],

    "Chinese": [
        {
            "triggers": ["chicken", "capsicum", "garlic"],
            "title": "Kung Pao Chicken",
            "base_steps": [
                "Marinate chicken in soy sauce, cornstarch, and rice vinegar for 15 minutes.",
                "Mix sauce: soy sauce, hoisin, sugar, vinegar, and cornstarch.",
                "Stir-fry dried chillies in a hot oiled wok for 30 seconds; add garlic and ginger.",
                "Add chicken and cook on high heat until golden, about 4–5 minutes.",
                "Add capsicum and toss for 2 minutes.",
                "Pour in the sauce and toss until thickened.",
                "Add peanuts and garnish with spring onions. Serve with steamed rice.",
            ],
        },
        {
            "triggers": ["tofu", "mushroom", "garlic"],
            "title": "Mapo Tofu",
            "base_steps": [
                "Blanch tofu cubes in salted boiling water for 2 minutes; drain gently.",
                "Fry minced garlic and ginger in a hot wok until fragrant.",
                "Add chilli bean paste and cook for 1 minute until oil turns red.",
                "Add mushrooms and stir-fry for 2 minutes; pour in vegetable stock.",
                "Slide in tofu and simmer for 5 minutes.",
                "Thicken with cornstarch slurry; finish with sesame oil and Sichuan pepper.",
                "Garnish with spring onions. Serve with steamed rice.",
            ],
        },
        {
            "triggers": ["carrot", "capsicum", "onion"],
            "title": "Chinese Vegetable Stir-Fry",
            "base_steps": [
                "Julienne carrots, slice capsicum, and cut onion into wedges.",
                "Mix sauce: soy sauce, oyster sauce, sesame oil, sugar, and cornstarch.",
                "Stir-fry onion in a smoking wok for 1 minute; add carrots for 2 minutes.",
                "Add capsicum and toss for 2 minutes more.",
                "Add garlic and ginger; stir for 30 seconds.",
                "Pour sauce over and toss until glossy.",
                "Serve immediately over rice or noodles.",
            ],
        },
        {
            "triggers": ["chicken", "onion", "garlic"],
            "title": "Chinese Garlic Chicken",
            "base_steps": [
                "Marinate sliced chicken in soy sauce, Shaoxing wine, and cornstarch for 10 minutes.",
                "Sear chicken in a very hot wok until cooked; set aside.",
                "Stir-fry garlic and ginger for 30 seconds; add sliced onion for 2 minutes.",
                "Return chicken; add oyster sauce, soy sauce, and a pinch of sugar.",
                "Toss on high heat for 1–2 minutes; finish with sesame oil.",
                "Serve with steamed rice.",
            ],
        },
    ],

    "Italian": [
        {
            "triggers": ["tomato", "garlic", "mushroom"],
            "title": "Penne Arrabbiata with Mushrooms",
            "base_steps": [
                "Cook penne in salted boiling water until al dente; reserve 1 cup pasta water.",
                "Sauté sliced mushrooms in olive oil on high heat until golden.",
                "Add minced garlic and chilli flakes; cook for 1 minute.",
                "Add crushed tomatoes and simmer for 10–12 minutes until thickened.",
                "Toss drained pasta in the sauce, loosening with pasta water as needed.",
                "Plate and finish with fresh basil and extra-virgin olive oil.",
            ],
        },
        {
            "triggers": ["chicken", "tomato", "garlic"],
            "title": "Chicken Cacciatore",
            "base_steps": [
                "Season chicken; brown on all sides in olive oil then set aside.",
                "Sauté diced onion and garlic in the same pan until soft.",
                "Add capsicum for 3 minutes, then deglaze with white wine.",
                "Add crushed tomatoes, oregano, and rosemary; return chicken.",
                "Cover and simmer on low heat for 35–40 minutes.",
                "Serve with crusty bread or polenta.",
            ],
        },
        {
            "triggers": ["mushroom", "garlic", "onion"],
            "title": "Mushroom Risotto",
            "base_steps": [
                "Keep vegetable stock warm in a separate pan.",
                "Sauté onion in butter and olive oil until translucent.",
                "Add mushrooms and cook until golden; add garlic for 1 minute.",
                "Toast Arborio rice for 2 minutes, then add stock one ladle at a time, stirring.",
                "Continue for 18–20 minutes until rice is creamy and al dente.",
                "Off heat, stir in cold butter and Parmesan. Season and serve immediately.",
            ],
        },
        {
            "triggers": ["tomato", "onion", "garlic"],
            "title": "Pasta Pomodoro",
            "base_steps": [
                "Cook spaghetti in salted boiling water until al dente; reserve pasta water.",
                "Gently cook sliced garlic in olive oil until golden.",
                "Add sliced onion until soft, then crushed tomatoes with salt and a pinch of sugar.",
                "Simmer for 15 minutes until thick and rich.",
                "Toss pasta in the sauce with pasta water to loosen.",
                "Finish with torn basil and good olive oil.",
            ],
        },
    ],

    "Japanese": [
        {
            "triggers": ["tofu", "mushroom", "onion"],
            "title": "Miso Soup with Tofu & Mushrooms",
            "base_steps": [
                "Simmer kombu in water for 10 minutes; remove, add bonito flakes, steep 5 minutes, then strain.",
                "Bring dashi to a gentle simmer; add sliced mushrooms for 3 minutes.",
                "Add silken tofu cubes.",
                "Dissolve miso in a ladleful of hot stock, then stir back — do not boil.",
                "Add sliced spring onions and serve immediately.",
            ],
        },
        {
            "triggers": ["chicken", "onion", "garlic"],
            "title": "Chicken Teriyaki",
            "base_steps": [
                "Mix teriyaki sauce: equal parts soy sauce, mirin, sake, and sugar.",
                "Marinate scored chicken thighs for 20 minutes.",
                "Cook skin-side down in a non-stick pan for 5–6 minutes until crispy.",
                "Flip for 4–5 minutes, then pour in remaining marinade and glaze.",
                "Slice and serve over steamed rice with pickled ginger.",
            ],
        },
        {
            "triggers": ["carrot", "mushroom", "onion"],
            "title": "Yasai Itame (Vegetable Stir-Fry)",
            "base_steps": [
                "Slice all vegetables thinly and uniformly.",
                "Stir-fry onion in sesame oil over high heat for 1 minute.",
                "Add carrots for 2 minutes, then mushrooms for 2 minutes more.",
                "Season with soy sauce, mirin, and a pinch of salt.",
                "Finish with a drizzle of sesame oil. Serve with rice and miso soup.",
            ],
        },
        {
            "triggers": ["potato", "onion", "carrot"],
            "title": "Nikujaga (Japanese Potato Stew)",
            "base_steps": [
                "Sauté thick-sliced onion in oil until slightly soft.",
                "Add potato wedges and carrot rounds; stir gently.",
                "Pour in dashi stock, soy sauce, mirin, and sugar to cover.",
                "Bring to a boil, skim foam, then simmer covered for 20 minutes.",
                "Serve in deep bowls with steamed rice.",
            ],
        },
    ],

    "Mexican": [
        {
            "triggers": ["tomato", "onion", "capsicum"],
            "title": "Veggie Tacos with Salsa Roja",
            "base_steps": [
                "Char tomatoes, onion, and capsicum over a flame until blistered.",
                "Blend with garlic, salt, and cumin into a chunky salsa.",
                "Warm corn tortillas on a dry griddle for 30 seconds per side.",
                "Sauté remaining capsicum and onion strips with cumin and paprika.",
                "Fill tortillas; top with salsa, avocado, lime juice, and coriander.",
            ],
        },
        {
            "triggers": ["chicken", "tomato", "onion"],
            "title": "Pollo a la Mexicana",
            "base_steps": [
                "Season chicken with cumin, chilli powder, paprika, salt, and pepper.",
                "Sear in hot oil until golden; remove and set aside.",
                "Sauté onion until soft; add garlic and jalapeño for 1 minute.",
                "Add diced tomatoes and cook down into a sauce.",
                "Return chicken; cover and simmer for 20–25 minutes.",
                "Serve with Mexican rice, refried beans, and warm tortillas.",
            ],
        },
        {
            "triggers": ["paneer", "capsicum", "onion"],
            "title": "Paneer Fajitas",
            "base_steps": [
                "Marinate paneer strips in lime juice, cumin, smoked paprika, and chilli powder.",
                "Sear paneer on a very hot cast-iron pan for 2 minutes per side; set aside.",
                "Stir-fry capsicum and onion strips until slightly charred.",
                "Return paneer and toss together.",
                "Serve in warm flour tortillas with sour cream, guacamole, and salsa.",
            ],
        },
        {
            "triggers": ["potato", "onion", "tomato"],
            "title": "Papas Guisadas (Mexican Potato Hash)",
            "base_steps": [
                "Par-boil diced potatoes for 5 minutes; drain.",
                "Fry onion in oil until golden; add diced tomatoes and cook 5 minutes.",
                "Add potatoes and press lightly to get crispy edges.",
                "Season with cumin, paprika, salt, and pepper.",
                "Cook undisturbed for 3–4 minutes to form a crust, then flip.",
                "Serve with coriander, lime, and hot sauce.",
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_db():
    """Return a database connection."""
    return sqlite3.connect('database.db')


def find_best_recipe(ingredients_list, cuisine):
    """Return the best-matching recipe for the given cuisine and ingredients."""
    ingredients_lower = {i.lower() for i in ingredients_list}
    best, best_score = None, -1
    for recipe in RECIPES.get(cuisine, []):
        score = sum(1 for t in recipe["triggers"] if t in ingredients_lower)
        if score > best_score:
            best_score, best = score, recipe
    return best


def build_recipe(ingredients_list, cuisine):
    """Build and return a recipe dict from matched or fallback logic."""
    matched = find_best_recipe(ingredients_list, cuisine)
    if matched:
        return {
            "title":       matched["title"],
            "ingredients": ", ".join(ingredients_list),
            "steps":       matched["base_steps"],
        }

    # Fallback: sort by cooking priority and construct a generic dish
    priority = {
        "Onion": 1, "Garlic": 1, "Ginger": 1,
        "Tomato": 2, "Capsicum": 2, "Carrot": 2, "Potato": 2,
        "Paneer": 3, "Tofu": 3, "Chicken": 3, "Mushroom": 3,
    }
    sorted_ing = sorted(ingredients_list, key=lambda x: priority.get(x, 4))
    suffix = {
        "Indian": "Masala", "Chinese": "Stir-Fry",
        "Italian": "al Forno", "Japanese": "Itame", "Mexican": "Guisado",
    }.get(cuisine, "Dish")
    title = f"{sorted_ing[-1]} & {sorted_ing[0]} {suffix}" if len(sorted_ing) > 1 else f"Mixed {suffix}"

    steps = ["Heat oil in a pan over medium heat."]
    steps += [f"Add {ing} and cook until done." for ing in sorted_ing]
    steps += [
        f"Season with {cuisine.lower()} spices and mix well.",
        "Add salt to taste; adjust consistency with water if needed.",
        "Simmer for a few more minutes and serve hot.",
    ]
    return {"title": title, "ingredients": ", ".join(sorted_ing), "steps": steps}

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route('/')
def home():
    return render_template(
        'home.html',
        logged_in='user_id' in session,
        username=session.get('username', ''),
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username'].strip()
        email    = request.form['email'].strip().lower()
        password = generate_password_hash(request.form['password'])
        db = get_db()
        try:
            db.execute(
                'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                (username, email, password),
            )
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            error = "An account with that email already exists."
        finally:
            db.close()
    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email    = request.form['email'].strip().lower()
        password = request.form['password']
        db     = get_db()
        user   = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        db.close()
        if user and check_password_hash(user[3], password):
            session['user_id']  = user[0]
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        error = "Invalid email or password."
    return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])


@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    ingredients_list = [
        i.strip().title()
        for i in request.form['ingredients'].split(',')
        if i.strip()
    ]
    cuisine = request.form['cuisine']
    recipe  = build_recipe(ingredients_list, cuisine)
    return render_template('dashboard.html', username=session['username'], recipe=recipe)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email    TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    db.commit()
    db.close()
    if __name__ == "__main__":
    app.run()
