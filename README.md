
# **Soul Bank App**

## **Overview**

Soul Bank App is a web application designed to help evangelists and churches efficiently record and track souls saved during evangelism outreaches. The app provides an organized system for documenting new believers, capturing important details about each soul saved, and offering insightful reports to monitor progress over time.

## **Prerequisites**

- `Python 3.11.3`
- `Django 5.1.1`
- `Django Rest Framework (DRF) 3.15.2`
- `SQLite or any other preferred database`


## **Installation**
Clone the Repository


git clone https://github.com/GbolahanAlaba/soul-bank-app

cd soul-bank-app


## **Create Virtual Environment**

It's recommended to use a virtual environment to manage dependencies:


`python -m venv venv`

## **Activate Virtual Environment**

MAC `source venv/bin/activate`

Windows `venv/Scripts/activate`

## **Install Dependencies**

Install the required dependencies using pip:

`pip install -r requirements.txt`


## **Run Migrations**

Apply the migrations to set up your database schema:

`python manage.py makemigrations`

`python manage.py migrate`


## **Run the Development Server**
Start the development server to verify everything is set up correctly:

`python manage.py runserver`
You should now be able to access the application at http://127.0.0.1:8000/api

## **API Endpoints**
Base URL - `http://127.0.0.1:8000`

- `POST /auth/signin/`: Signin as a user or admin.
- `POST /auth/signup/`: Signup an account.


## **API Implementation**

#### POST /auth/signin/

- **Request Body**:

  ```json
  {
    "email_or_phone": "admin@gmail.com or 09073832843",
    "password": "pass"
  }

- **Response**:

  ```json
  {
    "status": "success",
    "message": "Signed successfully",
    "data": {
        "user_id": "1fd51c63-d29c-4450-b978-d32ca913ec53",
        "first_name": "HOF",
        "last_name": "Admin",
        "email": "admin@gmail.com",
        "phone": "090",
        "team": "Admin",
        "role": "Sector Leader",
        "sector": "Headquaters"
    },
    "token": "ef739f7d96ce5381f3785fd3680171eaa03ee604078763e91ac47770a315a98f"
  }

`200 OK` on success.

`404 Not Found` on not found error.

`403 Forbidden` on unverified account error.

`509 Internal Server Error` on server error.


## **Testing**
Run a tests to ensure the API endpoints work as expected.

`py manage.py test`