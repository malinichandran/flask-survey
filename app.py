from flask import Flask, request, render_template,redirect,flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses=[]

@app.route('/')
def show_start_survey_form():
    # prompts = story.prompts
    
    return render_template("survey_form.html",survey = survey)

@app.route('/start',methods=["POST"])
def start_survey():
    return redirect("/questions/0")


@app.route("/questions/<int:qid>")
def show_question(qid):
    question = survey.questions[qid]
    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    return render_template("question.html", question_num=qid, question=question)

@app.route("/answer",methods=["POST"])
def handle_question():
    choice = request.form['answer']
    responses.append(choice)
    
    if (len(responses)==len(survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/complete")
def complete():
    return render_template("completion.html",responses=responses)
    

