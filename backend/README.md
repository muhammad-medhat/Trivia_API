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

#### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

#### Running the server

- From within the `backend` directory first ensure you are working using your created virtual environment.
- ****IMP*:*** to avoid the error 
 ```AttributeError: module 'time' has no attribute 'clock'```
Edit line ***331*** in file **backend/venv/Lib/site-packages/sqlalchemy/util/compat.py**
``` 
    From: time_func = time.clock
    To:   time_func = time.perf_counter()
```

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
## API Endpoints
- GET     '/categories'
- GET     '/categories/<int:category_id>/questions'
- GET     '/questions'
- POST    '/questions'
- POST    '/quizzes'
- DELETE  '/questions'
- PATCH   '/questions/<int:question_id>'
- PUT     '/questions/<int:question_id>'

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
    {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography", 
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
    }
```

### GET '/categories/<int:category_id>/questions'
- Fetches an array of questions of a certain category
- Request Arguments: category_id
- Returns: A key for questions objects and ket for success value and another key for total results. 

##### Example output

http://127.0.0.1:5000/categories/2/questions.
```
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
```

### GET  '/questions'
- Fetches paginated questions
- Request Arguments: page
- Returns: A json object with the following keys:
    - categories
    - current_category
    - questions
    - total_questions

##### Example output

```{
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
```

### POST '/questions'

- This endpoint will be responsible for adding a new question, and searching for a question.
- it depends on the input request body
#### Adding a new question
- Require  a request body that contains
    - The question text
    - An answer text.
    - Category
    - Difficulty score.
- Request Arguments: None
- Returns: A json object with the following keys:
    - body
    - success
    - total_questions

##### Example output
 

```
{
    "body": {
        "answer": "The Pythoneer!",
        "category": 1,
        "difficulty": 1,
        "id": 28,
        "question": "What is your nickname? "
    },
    "success": true,
    "total_questions": 23
}
```
#### Search for question
- This endpoint get questions based on a search term. 
- Require  a request body that contains the searchterm as follows
```
{'search':'the'}
```
- Returns: It should return any questions(paginated) for whom the search term is a substring of the question.:
    - questions
    - success
    - total_questions

##### Example output

```
{
    "questions": [
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "..."
        }, 
        ...
    ],
    "success": true,
    "total_results": 10

```

### POST '/quizzes'
- Retrieve questions to play the quiz. 
- This endpoint take category and previous question parameters.
- Request body example
```
    {
        "category": "2",
        "previous_questions": ["16", "17"]
    }
```
- Return: a random questions within the given category, if provided, and that is not one of the previous questions

##### Example output
```
{
    "question": {
        "answer": "One",
        "category": 2,
        "difficulty": 4,
        "id": 18,
        "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    "success": true
}
```

### DELETE '/questions/<int:question_id>'
- An endpoint to DELETE question using a question ID.
- __Request Argement__ question_id

### PATCH/PUT '/questions/<int:question_id>'
- An endpoint to update or modify answer for a question using a question ID.
- __Request Argement__ question_id
##### Example output
- The updated question with the status of request
- the next output is the result of sending a patch request for a question with id 11
```
{
    "question": {
        "answer": "new updated answer",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    "success": true
}
```

## Error handlers

The following are the list of errors handld in this api, for a full list of errors can be found in this [MDN article](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- 400 -- Bad request
- 404 -- Not found
- 422 -- Not processable
- 500 -- Internal Server Error
    _Each error returns a json responce with its message_
     **For 500 response output**

```
{
    'success': False,
    'message': 'Internal Server Error'
}
```
