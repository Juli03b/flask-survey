from flask import Flask, request, session , render_template, redirect, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys, Question, Survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "hiih"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)



@app.route('/')
def start_page():
    """Load user's surveys, then render page"""
    load_usr_surveys()
    survey = surveys[session.get("current_survey", "personality")]

    return render_template('start-page.html', survey=survey, surveys=surveys)

@app.route('/start', methods=["POST"])
def start_handle():
    """Check if user has ansered the survey"""
    [[element_name, val]] = list(request.form.items())
    session["current_survey"] = val
    load_usr_surveys()
    survey = surveys[session.get("current_survey", "personality")]
    if not session.get(f"done_{survey.title}", None): 
        session["responses"] = []
        return redirect('/question/0') 
    else:
        flash('NOT AGAIN!', 'error')
        return redirect('/')

@app.route('/question/<int:q_num>')
def question_handling(q_num):
    """
    if #1: Check if question number is less or equal to questions list. 
    Then check if the previous questions have been answered.

    if #2: check if user is at the last question

    if #3: redirect user to home page if question is out of range
    """
    load_usr_surveys()
    survey = surveys[session.get("current_survey", "personality")]
    if q_num <= len(survey.questions) - 1:
        if validate_prev_qs(q_num - 1):
            question = survey.questions[q_num]
            q_num += 1
            return render_template('question.html', q_num=q_num, survey=survey, question=question) 
        else:
            q_num = len(session["responses"]) 
            question = survey.questions[q_num]
            flash('No skipping!!')
            return redirect(f'/question/{q_num}')
    elif q_num == len(survey.questions):
        return redirect('/thanks')
    elif q_num > len(survey.questions):
        return redirect('/')
    
@app.route('/answer', methods=['POST'])
def question_post():
    [[q_num, val]] = list(request.form.items())
    res = session["responses"]
    res.append({q_num: val})
    session["responses"] = res
    
    return redirect(f'question/{q_num}')

@app.route('/thanks')
def thank_you():
    survey = surveys[session.get("current_survey", "personality")]
    if len(session["responses"]) >= len(survey.questions):
        session[f"done_{survey.title}"] = True
        flash('Click header to go home', 'success')
        return render_template('thank-you.html', survey=survey, int=int)
    else:
        flash('NO', 'error')
        return redirect('/')

def validate_prev_qs(q_num):
    """ returns user's answer to question passed,
    or else it returns false"""
    if q_num < 1:
        return True
    for response in session["responses"]:
        if response.get(str(q_num)):
            return response.get(str(q_num))
    return False

@app.route('/create-survey')
def create_story():
    return render_template('create-survey.html')

@app.route('/submit-survey', methods=["POST"])
def sub_survey():
    if not session.get("surveys"):
        session["surveys"] = []
        surveys = session["surveys"]
        surveys.append(request.form)
        session["surveys"] = surveys

        return redirect('/')
    else:

        surveys = session["surveys"]
        surveys.append(request.form)
        session["surveys"] = surveys

        return redirect('/')

def load_usr_surveys():
    if session.get("surveys", None):
        for sur in session["surveys"]:
            surveys[sur["title"]] = Survey(sur["title"], sur["instructions"], [Question(sur[q]) for q in sur ] )
