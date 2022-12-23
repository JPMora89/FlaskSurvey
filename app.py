from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = 'manchesterunited'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses_given = 'responses'

@app.route("/")
def homepage():
    """Homepage where the user chooses a survey"""
    return render_template("home.html", survey=survey)

@app.route("/start", methods=["POST"])
def show_start_page():
    session[responses_given] = []
    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    choice = request.form['answer']
    
    responses = session[responses_given]
    responses.append(choice)
    session[responses_given] = responses
    

    if (len(responses) == len(survey.questions)):
        return redirect("/finished")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:questionID>")
def show_question(questionID):
    responses = session.get(responses_given)
    

    if (responses is None):
        return redirect("/")
    elif (len(responses) == len(survey.questions)):
        return redirect("/Finished")
    elif (len(responses) != questionID):
        flash(f"Invalid questionID!")
        return redirect(f"questions/{len(responses)}")
    question = survey.questions[questionID]
    return render_template("question.html", question_number=questionID, question=question)


@app.route("/finished")
def finished():
    return render_template("finished.html")