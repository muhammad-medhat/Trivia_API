import os
from flask import Flask, request, abort, jsonify
from sqlalchemy.sql.expression import select
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    QUETSIONS_PER_PAGE = 10
    '''
    @TODO: #? Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    '''
    @TODO:#? Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    def get_categories_dict():
        selection = Category.query.order_by(Category.id).all()
        return {cat.id: cat.type for cat in selection}
    
    def paginate(req, selection):
        """ 
        Paginate the obtained results 

        Args:
            req ([request]): [name of the sent request]
            selection ([dictionary]): [the whole results ]

        Returns:
            [dictionary]: [a slice from the whole results]
        """
        page=req.args.get('page', 1, type=int )
        start=(page-1)*QUETSIONS_PER_PAGE
        end = start+QUETSIONS_PER_PAGE
        return selection[start:end]
    '''
    @TODO: 
    #? Create an endpoint to handle GET requests 
    #? for all available categories.
    '''

        
    @app.route('/categories', methods=['GET'])
    def get_request_categories():
        categories_count = Category.query.order_by(Category.id).count()
        if categories_count == 0:
            abort(404)
        return jsonify({
            'categories':get_categories_dict()
        })

    '''
    @TODO: 
    #? Create an endpoint to handle GET requests for questions, 
    #? including pagination (every 10 questions). 
    #? This endpoint should return a list of questions, 
    #? number of total questions, current category, categories. 

    TEST: 
    #? At this point, when you start the application
    #? you should see questions and categories generated,
    #? ten questions per page and pagination at the bottom of the screen for three pages.
    #? Clicking on the page numbers should update the questions. 
    '''
    @app.route('/questions', methods=['GET'])
    def get_paginated_questions():
        categories = Category.query.all()
        questions = Question.query.all()
        
        formated_categories = get_categories_dict()
        formated_questions = [q.format() for q in questions]   
        display = paginate(request, formated_questions)
        
        if len(display) == 0:
            abort(404)
        else:
            current_category='## IMPLEMENT CRRENT CATEGORY ##'
            return jsonify({
                "questions": display,                
                "total_questions": len(questions),
                "categories": formated_categories,
                "current_category": current_category
            })
    '''
    @TODO: 
    #? Create an endpoint to DELETE question using a question ID. 

    TEST: 
    #? When you click the trash icon next to a question, the question will be removed.
    #? This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])        
    def delete_question(question_id):

        try:
            q = Question.query.filter(Question.id==question_id).one_or_none()
            if q is None:
                abort(404)
            else:
                q.delete()
                return jsonify({
                    'success':True
                })
                
        except:
            abort(404)

    '''
    @TODO: 
    #? Create an endpoint to POST a new question, 
    #? which will require the question and answer text, 
    #? category, and difficulty score.

    #? TEST: When you submit a question on the "Add" tab, 
    #? the form will clear and the question will appear at the end of the last page
    #? of the questions list in the "List" tab.  
    '''
    @app.route('/questions', methods = ['POST'])
    def create_question():
        body = request.get_json()
        if body:      
            id          = body.get('id', None)
            question    = body.get('question', None)
            answer      = body.get('answer', None)
            category    = body.get('category', None)
            difficulty  = body.get('difficulty', None)
            
            search      = body.get('search', None)        
            try:
                if search:
                    return post_search_questions(search)
                else:
                    b = Question( id, question, answer, category, difficulty)                
                    b.insert()
                    return jsonify({
                        'success':True, 
                        'total_questions':len(Question.query.all()),
                        'body':b.format()
                    })        
            except:
                abort(404)
        else:
            abort(400)

    '''
    @TODO: 
    #! Create a POST endpoint to get questions based on a search term. 
    #! It should return any questions for whom the search term 
    #! is a substring of the question. 

    #! TEST: Search by any phrase. The questions list will update to include 
    #! only question that include that string within their question. 
    #! Try using the word "title" to start. 
    '''
    def post_search_questions(search):
        """
        Function for searching a question

        Returns:
            json object with the format {
            "success": True, 
            "questions": array of questions to display, 
            "total_results": integer number of results
        }
        """

        selection = Question.query.filter(Question.question.ilike(f'%{search}%'))                
        formated_selections = [q.format() for q in selection]   
        display = paginate(request, formated_selections)
        return jsonify({
            "success": True, 
            "questions": display, 
            "total_results":len(display)
        })

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):   
        if Category.category_exists(category_id):
            qtns = Question.query.filter(Question.category==category_id).all()
            formated = [q.format() for q in qtns]  
            display = paginate(request, formated)
            
            return jsonify({
                "success": True, 
                "questions": display, 
                "total_results":len(qtns)
            })
        else:
            abort(404)


    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.route('/quizzes', methods=['POST'])
    def start_quiz():
        body = request.get_json()            

        if body:
            category           = body.get('category', None)
            previous_questions = body.get('previous_questions', None)
            if category:
                # if category is set, filter questions by category
                # and not in tee previouis_questions list
                category_questions = Question.query.filter(Question.category==category,Question.id.notin_(previous_questions)).all()
            else:
                # just filter by questions not in the previous_questions list
                category_questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            
            # return a random question from the selected list of questions
            random_question = random.choice(category_questions)
            return jsonify({
                    "success":True, 
                    "question":random_question.format()
                })
        else:
            abort(404)









    '''
    @TODO: 
    #? Create error handlers for all expected errors 
    #? including 404 and 422. 
    #* 400 and 405 added
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False, 
            'message':'Bad Request'
        }), 400
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False, 
            'message':'Not Found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False, 
            'message':'Method not allowed'
        }), 405
        
    @app.errorhandler(422)
    def unprocssable(error):
        return jsonify({
            'success': False, 
            'message':'Unprocessable Entity'
        }), 422
    
    return app

    