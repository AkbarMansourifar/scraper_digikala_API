# Django Scraper API

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.3-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🔹 Project Overview
This project is a **Digikala web scraper** integrated into a **professional Django API**.  
With this API, you can easily search for products and retrieve detailed information including:
- Product title
- Product URL
- Category
- Main image URL
- Rating
- Price

Key features:
- Modern, scalable Django project structure
- Scraper logic separated in `utils.py`
- Export results to CSV and JSON
- API endpoints for easy data retrieval
- Optional proxy support

---

## 🔹 Requirements
- Python 3.11+
- Django 4.3+
- Dependencies listed in `requirements.txt`

---

## 🔹 Installation & Setup
1. Clone the repository:

```bash
git clone https://github.com/USERNAME/django_scraper_api.git
cd django_scraper_api
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run Django server:

```bash
python manage.py runserver
```

---

## 🔹 Using the API
### Main Endpoint:

```
GET /api/search/?q=<product_name>&items=<number_of_items>
```

**Parameters:**
- `q` : Product name (e.g., `mobile`)  
- `items` : Number of products to retrieve (e.g., `20`)  

**Example request with cURL:**

```bash
curl "http://127.0.0.1:8000/api/search/?q=mobile&items=10"
```

**Example JSON response:**

```json
[
  {
    "title": "XYZ Mobile Phone",
    "product_url": "https://www.digikala.com/product/...",
    "category": "Mobile Phones",
    "image_url": "https://www.digikala.com/product/xyz.jpg",
    "rating": 4.5,
    "price": 12300000
  }
]
```

---

## 🔹 Project Structure
```
django_scraper_api/
│
├─ scraper/             # Django app
│   ├─ utils.py         # Scraper logic
│   ├─ views.py         # API views
│   ├─ urls.py
│   └─ ...
│
├─ django_scraper_api/
│   └─ settings.py
│
├─ requirements.txt
├─ manage.py
└─ README.md
```

---

## 🔹 Professional Notes
- To use proxies, create a `proxy_list.txt` file with one proxy per line.  
- Scraper includes request throttling to reduce the risk of being blocked.  
- CSV and JSON outputs are available for offline analysis.  

---

## 🔹 License
This project is released under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.
