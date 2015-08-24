# Python library imports
import flask
from flask import flash, render_template, request, jsonify, redirect, url_for

# Imports from other parts of the app
from forms import ScoreForm
from models import RobotScore, db

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

# Add a new robot score
@app.route("/new", methods=['GET', 'POST'])
def new_score():
    form = ScoreForm()
    if form.validate_on_submit():
        score = RobotScore()
        form.populate_obj(score)
        db.session.add(score)
        db.session.commit()
        flash("Added score")
        return redirect(url_for("index"))
    return render_template("form.html", form=form)

@app.route("/edit_score/<int:score_id>", methods=['GET', 'POST'])
def edit_score(score_id):
    score = RobotScore.query.get(score_id)
    form = ScoreForm(obj = score)
    if form.validate_on_submit():
        form.populate_obj(score)
        db.session.commit()
        flash("Added score")
        return redirect(url_for("index"))
    return render_template("form.html", form=form)

# Utility method to get live score when score form is being filled out
@app.route('/_add_numbers')
def add_numbers():
    score = RobotScore(tree_branch_is_closer = request.args.get('tree_branch_is_closer')=='true', tree_branch_is_intact = request.args.get('tree_branch_is_intact')=='true', cargo_plane_location = request.args.get('cargo_plane_location', 0, type=int))
    return jsonify(result=score.getScore())

if __name__ == "__main__":
    app.debug = True
    db.create_all(app=app)
    app.run(debug = True)
