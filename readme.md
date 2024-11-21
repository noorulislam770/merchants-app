
# Merchant Accounting Application

A simple application to help local merchants transition from traditional pen-and-paper accounting to a digital system. The app allows users to manage transactions, track credits, and generate transaction summaries with a user-friendly interface.

---

## Features

- **Transaction Management**
  - Add, edit, and delete transactions.
  - Filter and search by transaction type, customer, salesperson, and date.

- **Credit Management**
  - Track credit transactions.
  - Mark credits as paid or pending.
  - Filter credits by status and salesperson.

- **Analytics**
  - Summarize daily transactions.
  - Exclude paid credits from summaries.

- **User Management**
  - Quick login functionality for salespeople through a dropdown in the navbar.

- **Error Handling**
  - Custom 404 error page for undefined routes.

- **Responsive Design**
  - Designed with Bootstrap for a seamless user experience across devices.

---

## Installation

### Prerequisites
- Python 3.x
- Django
- PostgreSQL (or any other database supported by Django) / I Use Sqlite
- Git

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/noorulislam770/merchants-app.git
   cd merchants-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Update the `DATABASES` section in `settings.py` with your database credentials.
   - Apply migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

---

## Usage

1. Navigate to the home page of the application.
2. Log in as a salesperson or administrator.
3. Access features such as adding/editing transactions, managing credits, and viewing analytics.
4. Use the dropdown in the navigation bar for quick salesperson login.

---

## Contribution Guidelines

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push to your fork.
4. Create a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact

For any questions or support, contact:
- **Developer Name:** Noor ul Islam
- **Email:** noorulislam770@gmail.com
