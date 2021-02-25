from flask import Flask, request, render_template, redirect, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "hiih"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
survey = surveys["satisfaction"]

@app.route('/')
def start_page():
    return render_template('start-page.html', survey=survey)

@app.route('/question/<int:q_num>')
def question_handling(q_num):
    if q_num <= len(survey.questions) - 1:
        if validate_prev_qs(q_num - 1):
            question = survey.questions[q_num]
            q_num += 1
            return render_template('question.html', q_num=q_num, survey=survey, question=question) 
        else:
            q_num = len(responses) 
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
    responses.append({q_num: val})

    return redirect(f'question/{q_num}')

@app.route('/thanks')
def thank_you():
    if len(responses) >= len(survey.questions):
        #user might answer two questions twice, add limit
        flash('Click header to go home', 'success')
        return render_template('thank-you.html')
        print(responses)
    else:
        print(responses)
        flash('NO', 'error')
        return redirect('/')

def validate_prev_qs(q_num):
    if q_num < 1:
        return True
    for response in responses:
        if response.get(str(q_num)):
            return response.get(str(q_num))
    return False