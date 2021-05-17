from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from datetime import timedelta

from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "hello"
DebugToolbarExtension(app)

sur = satisfaction_survey

'''activate and setup session for one year'''
@app.before_request
def set_session_timeout():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days = 365)

'''send to home page'''
@app.route('/')
def home():

    '''check if user already took servey'''
    if session.get('responses'):
        responses = session.get('responses')
        if len(responses) == len(sur.questions):
            flash('You already completed survey, thank you', 'error')

    title = sur.title
    instruct = sur.instructions

    return render_template('home.html', title = title, instruct = instruct)

'''send to quastion page with number of question'''
@app.route('/questions/<int:num>')
def questions(num):

    '''check if session responses exists if not setup session'''
    if session.get('responses'):
        responses = session.get('responses')
    else:
        responses = []
        session['responses'] = responses

    '''check if user requests the correct number of the question if not change to correct number'''
    if num != len(responses)+1:

        msg = f'You are trying to get the invalid number {num} of the question. Your question number is {len(responses)+1}'
        flash(msg, 'error')

        num = len(responses)+1

    '''check if user already finished servey and tries to get question page'''
    if len(responses) == len(sur.questions):
        return redirect('/finished')

    question_number = num
    title = f'Question # {question_number}'

    question = sur.questions[num-1].question
    choices = sur.questions[num-1].choices

    return render_template('question.html', title = title, question = question, choices = choices, question_number = question_number)

'''process user's answers with POST request'''
@app.route('/answer', methods=["POST"])
def answer():

    answer = request.form['answer']
    num = int(request.form['question'])+1

    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    '''check if user finished servey if not rederect to the correct question'''
    if len(responses) < len(sur.questions):
        url = f'/questions/{num}'
    else:
        url = '/finished'

    return redirect(url)

'''send user to finished page'''
@app.route('/finished')
def finished():
    return render_template('endservey.html')
