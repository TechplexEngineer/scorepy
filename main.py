# Python library imports
import flask
from flask import flash, render_template, request, jsonify, redirect, url_for, make_response
from cStringIO import StringIO
from xhtml2pdf import pisa

# Imports from other parts of the app
from forms import ScoreForm, TeamForm
from models import RobotScore, Team, db

# setup application
app = flask.Flask(__name__)
app.config.from_object('config')

db.init_app(app)

# Main route
@app.route("/")
def index():
    scores = RobotScore.query.all()
    for score in scores:
        score.total=score.getScore()
    return render_template("index.html", scores=scores)

@app.route("/teams")
def team_list():
    teams = Team.query.all()
    return render_template("teams.html", teams=sorted(teams, key=by_team))

# Add a new robot score
@app.route("/new", methods=['GET', 'POST'])
def new_score():
    form = ScoreForm()
    form.team_id.choices = [(t.id, t.number) for t in sorted(Team.query.all(), key=by_team)]
    if request.method == 'POST' and form.validate_on_submit():
        score = RobotScore()
        form.populate_obj(score)
        db.session.add(score)
        db.session.commit()
        flash("Added score")
        return redirect(url_for("index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("score_form.html", form=form)

# add a new team
@app.route("/new_team", methods=['GET', 'POST'])
def new_team():
    form = TeamForm()
    if request.method == 'POST' and form.validate_on_submit():
        team = Team()
        form.populate_obj(team)
        db.session.add(team)
        db.session.commit()
        flash("Added team")
        return redirect(url_for("team_list"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("team_form.html", form=form)

# Edit a previously-entered score
# TODO can this be combined with the above method?
@app.route("/edit_score/<int:score_id>", methods=['GET', 'POST'])
def edit_score(score_id):
    score = RobotScore.query.get(score_id)
    form = ScoreForm(obj = score)
    form.team_id.choices = [(t.id, t.number) for t in sorted(Team.query.all(), key=by_team)]
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(score)
        db.session.commit()
        flash("Edited score")
        return redirect(url_for("index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("score_form.html", form=form)

# Return a list of scores, highest - lowest
@app.route("/ranks", methods=['GET'])
def ranks():
    scores = RobotScore.query.all()
    for score in scores:
        score.total=score.getScore()
    return render_template("ranks.html", scores=sorted(scores, key=by_score, reverse=True))

def create_pdf(pdf_data):
    pdf = StringIO()
    pisa.CreatePDF(StringIO(pdf_data.encode('utf-8')), pdf, encoding="utf-8")
    return pdf

@app.route('/ranks.pdf')
def rank_pdf():
    pdf = create_pdf(ranks())
    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'ranks.pdf'
    return response

def by_score(score):
    return score.total

def by_team(team):
    return team.number

# Utility method to get live score when score form is being filled out
@app.route('/_add_numbers')
def add_numbers():
    score = RobotScore(team = 0, tree_branch_is_closer = request.args.get('tree_branch_is_closer')=='true', tree_branch_is_intact = request.args.get('tree_branch_is_intact')=='true', cargo_plane_location = request.args.get('cargo_plane_location', 0, type=int))
    return jsonify(result=score.getScore())

if __name__ == "__main__":
    app.debug = True
    db.create_all(app=app)
    app.run(debug = True)
