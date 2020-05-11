#!/usr/bin/env python3
import os
from flask import Flask, request, abort, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
from flask_migrate import Migrate
from auth.auth import AuthError, requires_auth
from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv, find_dotenv
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from flask_cors import cross_origin




def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.secret_key = 'mysecret'
  setup_db(app)
  CORS(app)

  return app

APP = create_app()


oauth = OAuth(APP)

auth0 = oauth.register(
    'auth0',
    client_id='0fi6Tzl1S7GYMks7a3bCXVosXu49V1N8',
    client_secret='cC-Ta5v-SdfyJezX6qNQBxNeFtltvqsnjKiDZWGV1r1EGlwz5uRMVN-sjK2eTHbK',
    api_base_url='https://dev-mee40p9i.eu.auth0.com',
    access_token_url='https://dev-mee40p9i.eu.auth0.com/oauth/token',
    authorize_url='https://dev-mee40p9i.eu.auth0.com/authorize',
    token_placement='headers',
    client_kwargs={
        'scope': 'openid profile email',
    },
)





@APP.after_request
def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,PUT,POST,DELETE,OPTIONS')
        return response
'''
<----------FrontEnd---------------------------->
'''

@APP.route('/', methods=['GET'])
def index():
	return render_template('home.html')

@APP.route('/create', methods=['GET'])
def create_actor_profile():
	
	return render_template('index.html')

@APP.route('/create-movie', methods=['GET'])
def create_movie_profile():
	
	return render_template('create_movie.html')

@APP.route('/profile/<int:actor_id>', methods=['GET'])
def get_actor_profile(actor_id):
	return render_template('profile.html')

@APP.route('/profile-movie/<int:movie_id>', methods=['GET'])
def get_movie_profile(movie_id):
	return render_template('film_profile.html')

@APP.route('/dashboard')
def dashboard():	
    return render_template('dashboard.html')

@APP.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    return redirect('/dashboard')

@APP.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://localhost:8080/callback')


                           

@APP.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('index', _external=True), 'client_id': '0fi6Tzl1S7GYMks7a3bCXVosXu49V1N8'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

'''
<-------------API EndPoints------------------------->
'''


@APP.route('/actors/<int:actor_id>', methods=['GET'])
@requires_auth('get:actor-detail')
def get_actor(payload,actor_id):
	
	actor = Actor.query.get(actor_id)
	return jsonify({'first_name': actor.first_name,
                        'last_name': actor.last_name,
                        'age':actor.age,
                        'gender':actor.gender,
			'image_link':actor.image_link
})

@APP.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actor')
def delete_actor(payload,actor_id):
	
	actor = Actor.query.get(actor_id)
	actor.delete()
	return jsonify({'success': True,
                        'deleted': actor.id
})


@APP.route('/actors', methods=['GET'])
@requires_auth('get:actor')
def get_actors(payload):
	print(request.headers)

	actors = Actor.query.all()
	data=[]	
	for actor in actors:
		temp={  'id':actor.id,
		        'first_name':actor.first_name,
			'last_name':actor.last_name,
			'age':actor.age,
			'gender':actor.gender,
			'image_link':actor.image_link
			}
		data.append(temp)
	print(data)
	return jsonify({
			'success': True,
			'actors':data
			})
	

@APP.route('/actors', methods=['POST'])
@requires_auth('post:actor')
def create_actor(payload):
	req =request.get_json()
	
	
	try:
		first_name = req['first_name']
		last_name = req['last_name']
		age = int(req['age'])
		gender = req['gender']
		image_link = req['image_link']
		if first_name == None or last_name == None:
			abort(400)
		new_actor = Actor(first_name = first_name, last_name = last_name, age = age, gender = gender, image_link=image_link)
		Actor.insert(new_actor)
		new_id = new_actor.id
		return jsonify({
			'success': True,
			'actors':new_id
			})
	except:
		abort(422)




@APP.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actor')
def edit_actor(payload,actor_id):
	req =request.get_json()
	actor =Actor.query.get(actor_id)
	
	try:
		

		req_first_name = req['first_name']
		if req_first_name!=None:
			
			actor.first_name= req_first_name
		req_last_name =req['last_name']
		if req_last_name!=None:
			actor.last_name= req_last_name
		req_age = req['age']
		if req_age!=None:
			actor.age = int(req_age)
		req_gender = req['gender']
		if req_gender!=None:
			actor.gender = req_gender
		req_link = req['image_link']
		if req_link!=None:
			actor.image_link = req_link 
		actor.update()
		
		
	except BaseException:
		abort(400)
	return jsonify({
			'success': True,
			'actors':actor.id
			})


@APP.route('/movies', methods=['GET'])
@requires_auth('get:movie')
def get_movies(payload):
	

	movies = Movie.query.all()
	data=[]	
	for movie in movies:
		temp={  'id':movie.id,
		        'title':movie.title,
			'release_date':movie.release_date
			}
		data.append(temp)
	print(data)
	return jsonify({
			'success': True,
			'movies':data
			})



@APP.route('/movies', methods=['POST'])
@requires_auth('post:movie')
def create_movie(payload):
	req =request.get_json()
	print(req)
	
	try:
		title = req['title']
		release_date = req['release_date']
		image_link = req['image_link']
		if title == None or release_date == None or image_link==None:
			abort(400)
		new_movie = Movie(title = title, release_date = release_date,image_link = image_link)
		Movie.insert(new_movie)
		new_id = new_movie.id
		return jsonify({
			'success': True,
			'actors':new_id
			})
	except:
		abort(422)




@APP.route('/movies/<int:movie_id>', methods=['GET'])
@requires_auth('get:movie-detail')
def get_movie(payload,movie_id):
	
	movie = Movie.query.get(movie_id)
	return jsonify({'title': movie.title,
                        'release_date': movie.release_date,
			'image_link': movie.image_link
})


@APP.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movie')
def delete_movie(payload,movie_id):
	
	movie = Movie.query.get(movie_id)
	movie.delete()
	return jsonify({'success': True,
                        'deleted': movie.id
})


@APP.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movie')
def edit_movie(payload,movie_id):
	req =request.get_json()
	movie =Movie.query.get(movie_id)
	print(req)
	try:
		

		req_title = req['title']
		if req_title!=None:
			
			movie.title= req_title
		req_date =req['release_date']
		if req_date!=None:
			movie.release_date= req_date
		req_link = req['image_link']
		if req_link!=None:
			movie.image_link = req_link
		 
		movie.update()
		
		
	except BaseException:
		abort(400)
	return jsonify({
			'success': True,
			'actors':movie.id
			})

                        
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
