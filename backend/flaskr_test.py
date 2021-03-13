import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from subprocess import call


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:1111@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        self.new_question = {
            'id':'1', 
            'question': "What is your nickname? ",
            'answer': "The Pythoneer!",
            'category': '1',
            'difficulty': '1' 
        } 
        
        
    def tearDown(self):
        """
        Executed after reach test
        Run this script after each test
        """


        pass
    
# @TODO: Write at least two tests for each endpoint - one each for success and error behavior.
#        You can feel free to write additional tests for nuanced functionality,
#        Such as adding a question without a rating, etc. 
#        Since there are four routes currently, you should have at least eight tests. 
# Optional: Update the question information in setUp to make the test database your own! 
    
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)        
        self.assertEqual(res.status_code, 200)   
        self.assertTrue(len(data['questions']), 10)   
        self.assertTrue(data['categories'], True)   
        self.assertTrue(data['total_questions'], True)   
        
    def test_get_questions_404(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)        
        self.assertEqual(res.status_code, 404)   
        self.assertEqual(data['success'], False)   
        self.assertEqual(data['message'], 'Not Found')   
    
    def test_post_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)  
        self.assertEqual(res.status_code, 200)   
        self.assertEqual(data['success'], True)   

    def test_post_create_question_400(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)  
        self.assertEqual(res.status_code, 400)   
        self.assertEqual(data['success'], False)   

    def test_delete_questions(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)   

    def test_delete_questions_404(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)   
    
    def test_post_search_questions_with_results(self):
        res = self.client().post('/questions', json={'search':'known'})
        data = json.loads(res.data)
        
        # self.assertEqual(res.status_code, 200)   
        self.assertEqual(data['success'], True)   
        
        self.assertTrue(len(data['questions']), 0) 
        
        self.assertTrue(data['total_results'], 0)   

    def test_post_search_questions_without_results(self):
        res = self.client().post('/questions', json={'search':'batman'})
        data = json.loads(res.data)
        
        # self.assertEqual(res.status_code, 200)   
        self.assertEqual(data['success'], True)   
        self.assertEqual(len(data['questions']), 0)   
        self.assertEqual(data['total_results'], 0)   
    
    def test_get_questions_by_category_with_results(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)   
        self.assertTrue(len(data['questions']), 4)   
        self.assertTrue(data['questions'])   
        self.assertEqual(data['total_results'], 4)   

    def test_get_questions_by_category_without_results(self):
        res = self.client().get('/categories/7/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)   
        self.assertEqual(len(data['questions']), 0)   
        self.assertEqual(data['total_results'], 0)   
        
    def test_post_quiz_with_category(self):
        res = self.client().post('/quizzes', json={ "category": "2", "previous_questions": ["16", "17"]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)   
        self.assertTrue(data['question'])
        self.assertTrue(data['success'])   

    def test_post_quiz_with_no_category(self):
        res = self.client().post('/quizzes', json={ "previous_questions": ["16", "17"]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)   
        self.assertTrue(data['question'])
        self.assertTrue(data['success'])   
        
    def test_put_patch_question(self):
        res = self.client().put('/questions/12', json={"answer": "Updated New Answer"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) 
        self.assertTrue(data['question'])
        self.assertEqual(data['success'], True)
    
    def test_put_question_with_error_404(self):
        res = self.client().put('/questions/2', json={"answer": "Updated New Answer"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404) 
        self.assertEqual(data['success'], False)

    def test_put_question_with_error_400(self):
        res = self.client().put('/questions/12', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400) 
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()