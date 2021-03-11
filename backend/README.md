# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python Version
Python 3.8.5 for the python version 
#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

to install the packages required to run the application simply run the following command in a bash shell
```bash
pip install -r requirements.txt
```

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
### API Endpoints
- GET     '/categories'
- GET     '/categories/<int:category_id>/questions'
- GET     '/questions'
- POST    '/questions'
- POST    '/quizzes'
- DELETE  '/questions'

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. {'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

### GET '/categories/<int:category_id>/questions'
- Fetches an array of questions of a certain category
- Request Arguments: None
- Returns: A key for questions objects and ket for success value and another key for total results. 

#### Example 
http://127.0.0.1:5000/categories/2/questions.

{
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which..."
        },....
    ],
    "success": true,
    "total_results": 4
}

### GET  '/questions'
- Fetches paginated questions
- Request Arguments: page
- Returns: A json object with the following keys:
    - categories
    - current_category
    - questions
    - total_questions

#### Example 
{
    "categories": {
        "1": "Science",
        ...
    },
    "current_category": "## IMPLEMENT CRRENT CATEGORY ##",
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "....."
        },
        ...
        
    ],
    "total_questions": 22
}