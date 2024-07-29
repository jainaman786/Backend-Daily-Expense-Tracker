# Daily Expenses Sharing Application

## Overview

This project is a backend service for a daily expenses sharing application. It allows users to add expenses and split them based on three different methods: exact amounts, percentages, and equal splits. The application manages user details, validates inputs, and generates downloadable balance sheets.

## Features

- User Management: Each user has an email, name, and mobile number.
- Expense Management:
  - Add expenses.
  - Split expenses using three methods:
    1. **Equal**: Split equally among all participants.
    2. **Exact**: Specify the exact amount each participant owes.
    3. **Percentage**: Specify the percentage each participant owes (ensure percentages add up to 100%).
- Balance Sheet:
  - Show individual expenses.
  - Show overall expenses for all users.
  - Download balance sheet as an Excel file.

## API Endpoints

### User Endpoints
- **Create user**: `POST /api/users`
- **Retrieve user details**: `GET /api/users/{user_id}`

### Expense Endpoints
- **Add expense**: `POST /api/expenses`
- **Retrieve individual user expenses**: `GET /api/expenses/user/{user_id}`
- **Retrieve overall expenses**: `GET /api/expenses`
- **Download balance sheet**: `GET /api/balance-sheet/download`

## Setup and Installation

### Installation

1. Clone the repository
   git clone https://github.com/jainaman786/Backend-Daily-Expense-Tracker.git
   
   cd expense-tracker-app

3. Create and activate a virtual environment
   python -m venv venv
  # On Windows: venv\Scripts\activate
  # On Mac : source venv/bin/activate

3. Install the dependencies
   pip install -r requirements.txt

4. Running the project
    uvicorn main:app --host 127.0.0.1 --port 8000 --reload

## Documentation and Running the Application

1. Start the fast api server
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload

2. Access the API documentation
Open your browser and navigate to http://127.0.0.1:8000/docs to view the interactive API documentation


#Usage
##Adding a User
-To add a user, make a POST request to /api/users with the following JSON body:
{
  "email": "user@example.com",
  "name": "John Doe",
  "mobile_number": "1234567890"
}

##Adding an Expense
To add an expense, make a POST request to /api/expenses with the following JSON body:
{
  "amount": 100,
  "description": "Dinner",
  "date": "2023-07-28T19:30:00",
  "split_method": "equal",
  "participants": [
    {"user_id": 1},
    {"user_id": 2}
  ]
}

##Downloading the Balance Sheet
To download the balance sheet, make a GET request to /api/balance-sheet/download. This will return an Excel file with the balance sheet.


## To explore the api end points run the projects and enjoy the docs here http://127.0.0.1:8000/docs  after setting up project locally

  

   
