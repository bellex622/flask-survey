from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


response = []
current_question_idx = 0

@app.get('/')
def show_homepage():
    """display the homepage to users"""
    global current_question_idx
    current_question_idx = 0
    response.clear()
    title = survey.title
    instructions = survey.instructions

    return render_template("survey_start.html",title=title, instructions=instructions)



@app.post('/begin')
def show_survey():
    """presee start button and begin the survey"""

    return redirect(f"/questions/{current_question_idx}")







@app.post('/answer')
def continue_question():
    """continue to next question after submitting answer"""
    answer = request.form["answer"]
    print("\n\n****", answer)
    response.append(answer)

    global current_question_idx
    current_question_idx += 1

    if current_question_idx >= len(survey.questions):
        return redirect ('/thanks')


    else:
        return redirect(f"/questions/{current_question_idx}")




@app.get('/questions/<int:question_idx>')
def show_question(question_idx):
    """display the question to user"""

    question = survey.questions[question_idx]
    return render_template("question.html",question=question)

@app.get('/thanks')
def thank_user():
    """display thanks msg to user after completion"""

    questions_list = []
    for question in survey.questions:
        questions_list.append(question.prompt)

    result_dict = dict(zip(questions_list, response))
    print("combined questions and answers", result_dict)



    return render_template("completion.html",result_dict=result_dict)












