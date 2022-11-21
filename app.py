from flask import Flask, render_template, request, flash, redirect, session
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'surveysarecool'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

res_sessions = 'responses'

@app.route('/')
def instructions_page():
    title=satisfaction_survey.title
    instructions=satisfaction_survey.instructions
    return render_template('start.html',title=title,instructions=instructions)

@app.route('/startpage',methods=['POST'])
def start_survey():
    session[res_sessions] = []
    return redirect('/questions/0')

@app.route('/questions/<int:id>')
def questions_page(id):
    responses = session.get(res_sessions)
    if (len(responses) != id):
        flash('Error: Trying to access questions out of order')
        return redirect(f'questions/{len(responses)}')
    if (len(responses) == len(satisfaction_survey.questions)):
        flash('Error: survey already completed')
        return redirect('/end-survey')
    question = satisfaction_survey.questions[id]
    return render_template('questions.html', question=question, id=id)

@app.route('/answerpage',methods=['POST'])
def answers_page():
    ans = request.form['answer']
    responses = session[res_sessions]
    responses.append(ans)
    session[res_sessions] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/end-survey')
    else: 
        return redirect(f'/questions/{len(responses)}')

@app.route('/end-survey')
def end_survey():
    return render_template('end_survey.html')
    
    
