## Little Lemon Restaurant Backend API

A fully functioning backend API for managing a restaurant system, including menu items, orders, and user roles (Manager, Delivery crew, and Customers). This API allows role-based access to ensure only authorized users can perform certain actions, like assigning delivery crew to orders or placing orders.

### Features

    - Role-based access control: Manager, Delivery crew, and Customer roles with different access levels.

    - Menu management: View and update menu items.

    - Order management: Customers can create orders, managers can assign delivery crew, and delivery crew can update order status.

    - JWT Authentication: Secure API endpoints using Djoser for authentication and role management.

    - Filtering and Pagination: Efficient data retrieval with filtering and pagination features.

    - Deployed on AWS EC2: The API is hosted on an AWS EC2 instance with Nginx and Gunicorn for production readiness.

### Technologies Used

    - Backend Framework: Django, Django REST Framework
    - Authentication: Djoser, JWT
    - Database: SQLite
    - Deployment: AWS EC2, Nginx, Gunicorn
    - Tools: Postman, pipenv, Git

### Installation and Setup

1. Installation and Setup

```bash
git clone https://github.com/LucaXYB/LittleLemonBackendAPI.git
```

2. Navigate to the project directory

```bash
cd LittleLemonBackendAPI
```

3. Install dependencies using pipenv:

```bash
pipenv install
```

4. Apply migrations to set up the database

```bash
python manage.py migrate
```

5. Create a superuser for accessing the Django admin panel

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

7. Access the API locally at http://127.0.0.1:8000.

### API Endpoints

Here are some of the key API endpoints:

    - User Registration: /api/users/
    - User Login: /api/token/login/
    - Menu Items:
        - GET /api/menu-items/: List all menu items (customers and managers).
        - POST /api/menu-items/: Create a new menu item (managers only).
    -Orders:
        - GET /api/orders/: List all orders for customers or managers.
        - POST /api/orders/: Create a new order (customers).
        - PATCH /api/orders/{order_id}/: Update order status (delivery crew or manager).
    - User Role Management (managers only):
        - GET /api/groups/manager/users/: List all managers.
        - POST /api/groups/manager/users/: Assign user to the manager group.

### Testing the API

You can test the API using Postman or Insomnia. Here’s an example of how to retrieve all menu items:

1. In Postman, make a GET request to: http://127.0.0.1:8000/api/menu-items/.
2. Use the token from the login endpoint to authorize the request.

