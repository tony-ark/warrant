# 🛒 GadgetHub: E-commerce Platform for Gadgets

[![Django](https://img.shields.io/badge/Django-4.x-green?logo=django)](https://www.djangoproject.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.x-blue?logo=mysql)](https://www.mysql.com/)
[![CatBoost](https://img.shields.io/badge/CatBoost-ML-yellow?logo=catboost)](https://catboost.ai/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

---

Welcome to **GadgetHub**, an all-in-one Django-powered gadget e-commerce platform!  
With built-in warranty claim prediction powered by CatBoost and a robust MySQL backend, GadgetHub is the perfect launchpad for your next online gadget store.

---

## ✨ Features

- 🏪 **Modern E-commerce Storefront**  
  Browse, search, and purchase the latest gadgets with ease.

- 🔐 **User Authentication & Profiles**  
  Secure registration, login, and profile management.

- 🛍️ **Product Management**  
  Add, edit, and organize gadget listings with sleek admin controls.

- 💳 **Order Processing**  
  Smooth cart, checkout, and order tracking experience.

- 🤖 **Warranty Claim Prediction**  
  Leverage CatBoost ML to predict the outcome of warranty claims and streamline after-sales support.

- 📊 **Analytics Dashboard**  
  View sales, user, and warranty claim statistics.

- 💾 **MySQL Database Integration**  
  Reliable and scalable data storage.

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/tony-ark/warrant.git
cd warrant
```

### 2. Set Up MySQL Database

- Create a MySQL database (e.g., `gadgethub_db`)
- Update your `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gadgethub_db',
        'USER': '<your-mysql-username>',
        'PASSWORD': '<your-mysql-password>',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Apply Migrations & Create Superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Start the Server

```bash
python manage.py runserver
```
Visit [http://localhost:8000/](http://localhost:8000/) to see GadgetHub in action!

---

## 🤖 Warranty Claim Prediction (CatBoost)

- Make sure CatBoost is installed:  
  `pip install catboost`
- The CatBoost model is trained on historical warranty claims and predicts the probability of successful claims.
- To retrain the model, use the provided scripts in `/ml/` (see [ml/README.md](ml/README.md) for details).

---

## 🛠️ Tech Stack

- **Backend:** Django 4.x
- **Database:** MySQL 8.x
- **Machine Learning:** CatBoost
- **Frontend:** Django Templates + Bootstrap (customizable)

---

## 📂 Project Structure

```
warrant/
├── manage.py
├── warrant/             # Django project settings
├── shop/                # E-commerce app
├── warranty/            # Warranty claim logic & ML integration
├── ml/                  # CatBoost models & scripts
├── static/
├── templates/
└── requirements.txt
```

---

## 🖼️ Screenshots

> _Add screenshots of your storefront, admin dashboard, and warranty claim interface here!_

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -am 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 💡 Inspiration

GadgetHub is designed to blend robust e-commerce with intelligent after-sales support.  
Enjoy building your next-gen gadget store!

---
