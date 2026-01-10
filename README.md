# PhiMart - E-commerce REST API (Django REST Framework)

PhiMart is a fully functional e-commerce backend built using **Django REST Framework (DRF)**. It includes product management, categories, cart system, ordering, authentication using **JWT with Djoser**, and a complete API documentation generated using **drf_yasg (Swagger UI)**.

---

##  Features

### 🛒 **E-commerce Modules**

* **Products** CRUD
* **Categories** with product relationship
* **Product Images**
* **Cart system** (Add/Remove/Update cart items)
* **Orders** with status update

###  **Authentication**

* JWT Authentication using **Djoser**
* Register, Login, Logout, Password Reset endpoints

###  **API Documentation**

* Fully auto-generated API docs using **drf_yasg (Swagger & Redoc)**

###  **Other Features**

* Permissions and role-based access
* Serializers and Model ViewSets
* Nested routing for better API design

---

##  Project Structure (Highlights)

```
phimart/
├── products/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
├── orders/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
├── carts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│
├── settings.py
└── urls.py
```

---

##  Installation & Setup

### 1️ Clone the repository

```
git clone https://github.com/yourusername/phimart.git
cd phimart
```

### 2️ Create & activate virtual environment

```
python -m venv env
source env/bin/activate      # Linux/Mac
env\Scripts\activate         # Windows
```

### 3️ Install dependencies

```
pip install -r requirements.txt
```

### 4️ Apply migrations

```
python manage.py migrate
```

### 5️ Create superuser

```
python manage.py createsuperuser
```

### 6️ Run the server

```
python manage.py runserver
```

---

##  Authentication (JWT + Djoser)

Djoser provides the following routes:

* `/auth/jwt/create/` – Login
* `/auth/jwt/refresh/` – Refresh token
* `/auth/users/` – Register
* `/auth/users/me/` – Get logged-in user

Example login request:

```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

---

##  API Endpoints

###  **Products**

* `GET /api/products/`
* `POST /api/products/`
* `GET /api/products/{id}/`
* `PUT /api/products/{id}/`
* `DELETE /api/products/{id}/`

###  **Categories**

* `GET /api/categories/`
* `POST /api/categories/`

###  **Cart**

* `GET /api/carts/{cart_id}/items/`
* `POST /api/carts/{cart_id}/items/`
* `PATCH /api/carts/{cart_id}/items/{item_id}/`
* `DELETE /api/carts/{cart_id}/items/{item_id}/`

###  **Orders**

* `GET /api/orders/`
* `POST /api/orders/`
* `PATCH /api/orders/{id}/` – Update order status

---

##  Swagger Documentation

After running the server:

* Swagger UI → `/swagger/`
* Redoc UI → `/redoc/`

---

##  Technologies Used

* Python
* Django
* Django REST Framework
* Djoser (JWT Authentication)
* drf_yasg (API docs)
* PostgreSQL / SQLite

---

##  Contribution

Feel free to fork the project and improve features.
Pull requests are welcome!

---

##  License

This project is under the **MIT License**.

---

##  Support

If you like this project, give it a star ⭐ on GitHub!

