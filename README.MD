# 🍽️ LeftoverLink

**LeftoverLink** is a community-driven platform to reduce food wastage by connecting individuals, restaurants, and events with surplus food to people or NGOs in need.  
This project is built with **Django**, **Bootstrap**, and **SQLite** (for development) and can be deployed to Render or any cloud provider.

---

## 📌 Features
- **Food Sharing Posts** – Share surplus food details with images, location, and expiry.
- **Google Maps Discovery** – Find nearby food posts easily.
- **Smart Notifications** – Notify NGOs or receivers about new food availability.
- **Role-Based Access** – Donors, NGOs, and Receivers get separate dashboards.
- **Waste Reduction Tracker** – Monitor saved food statistics.
- **Responsive UI** – Modern Bootstrap-based interface.

---

## 🛠️ Tech Stack
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Backend**: Django (Python)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Deployment**: Render / Heroku
- **Version Control**: Git & GitHub

---

## 📂 Project Structure


```

leftoverlink/
│
├── leftoverlink/               # Main project settings & config
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── render.yaml              # Render deployment configuration
│
├── leftoverlink\_app/            # Main Django app with core features
│
├── media/                       # Uploaded media files
├── static/                      # Static files (CSS, JS, images)
├── template/                    # HTML templates
│
├── db.sqlite3                   # SQLite database (for local dev)
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation

````


## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/LeftoverLink.git
cd LeftoverLink
````

### 2️⃣ Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run migrations

```bash
python manage.py migrate
```

### 5️⃣ Create superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 6️⃣ Run the development server

```bash
python manage.py runserver
```

The site will be available at: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🌐 Deployment (Render)

1. Push your project to GitHub (including `requirements.txt` and `render.yaml`).
2. Go to [Render](https://render.com/), create a new **Web Service**.
3. Connect your GitHub repo, select your branch.
4. Render will detect `render.yaml` and auto-configure the build & start commands.
5. Deploy and your site will be live! 🎉

---

## 📜 License

This project is licensed under the MIT License — feel free to use and adapt.

---

## 👥 Contributors

* **Shivam Pawar** —  Web Developer
* **Bhakti Waghmare** —  Web Developer
* **Gayatri Mule** —  Web Developer
* **Tech Trio** — Project Team

```

---

If you want, I can also **add a “Quick Deploy to Render” badge** in the README so anyone visiting your GitHub can deploy the site in one click.  
That would make it look very professional.
```
