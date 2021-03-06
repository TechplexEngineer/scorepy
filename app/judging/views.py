from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask.ext.login import login_required
from app import db
from app.util import sortTeamsWithPlaceholder
from app.teams.models import Team
from models import Presentation, Technical, CoreValues
from forms import PresentationForm, TechnicalForm, CoreValuesForm

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_judging = Blueprint('judging', __name__, url_prefix='/judging')


# Restrict access to authorized users only
@mod_judging.before_request
@login_required
def before_request():
    pass


@mod_judging.route("/")
def index():
    teams = Team.query.all()
    return render_template("judging/judging_list.html",
                           teams=sorted(teams, key=by_team))


# Add a presentation judging entry
@mod_judging.route('/presentation/new', methods=['GET', 'POST'])
def add_presentation():
    teams = Team.query.all()

    if not teams:
        return render_template("no_teams.html")

    form = PresentationForm()
    form.team_id.choices = [(t.id, t.number) for t in
                            sortTeamsWithPlaceholder(teams)]

    # Gather and preset the team ID field if provided in URL
    preselected_team = request.args.get('team_id', default=None, type=int)
    if preselected_team is not None:
        form.team_id.data = preselected_team

    repeat = request.args.get('repeat', default=False, type=bool)

    if request.method == 'POST' and request.form['end'] == 'reset':
        return redirect(url_for(".add_presentation", repeat = True))
    elif request.method == 'POST' and request.form['end'] == 'submit' and form.validate_on_submit():
        presentation = Presentation()
        form.populate_obj(presentation)
        db.session.add(presentation)
        db.session.commit()
        if repeat:
            flash('Added presentation score for %s' % (presentation.team.number), 'success')
            return redirect(url_for(".add_presentation", repeat = True))
        else:
            return redirect(url_for("review"))
    elif request.method == 'POST':
        flash('Failed validation', 'danger alert-auto-dismiss')
    return render_template("judging/presentation_form.html", form=form, id=None, repeat=repeat)


# Edit a previously-entered presentation judging entry
@mod_judging.route("/presentation/<int:presentation_id>/edit",
                   methods=['GET', 'POST'])
def edit_presentation(presentation_id):
    presentation = Presentation.query.get(presentation_id)
    form = PresentationForm(obj=presentation)
    del form.team_id

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(presentation)
        db.session.commit()
        return redirect(url_for("review"))
    elif request.method == 'POST':
        flash('Failed validation', 'danger alert-auto-dismiss')
    return render_template("judging/presentation_form.html", form=form,
                           team_id=presentation.team.number, id=presentation.id)


# Delete a presentation judging entry
@mod_judging.route("/presentation/<int:presentation_id>/delete",
                   methods=['GET', 'POST'])
def delete_presentation(presentation_id):
    presentation = Presentation.query.get(presentation_id)
    if request.method == 'POST':
        db.session.delete(presentation)
        db.session.commit()
        return redirect(url_for("review"))
    return render_template("delete.html",
                           identifier="presentation evaluation for team %d"
                           % presentation.team.number)


# Add a technical judging entry
@mod_judging.route('/technical/new', methods=['GET', 'POST'])
def add_technical():
    teams = Team.query.all()

    if not teams:
        return render_template("no_teams.html")

    form = TechnicalForm()
    form.team_id.choices = [(t.id, t.number) for t in
                            sortTeamsWithPlaceholder(teams)]

    # Gather and preset the team ID field if provided in URL
    preselected_team = request.args.get('team_id', default=None, type=int)
    if preselected_team is not None:
        form.team_id.data = preselected_team

    repeat = request.args.get('repeat', default=False, type=bool)

    if request.method == 'POST' and request.form['end'] == 'reset':
        return redirect(url_for(".add_technical", repeat = True))
    elif request.method == 'POST' and request.form['end'] == 'submit' and form.validate_on_submit():
        technical = Technical()
        form.populate_obj(technical)
        db.session.add(technical)
        db.session.commit()
        if repeat:
            flash('Added technical score for %s' % (technical.team.number), 'success')
            return redirect(url_for(".add_technical", repeat = True))
        else:
            return redirect(url_for("review"))
    elif request.method == 'POST':
        flash('Failed validation', 'danger alert-auto-dismiss')
    return render_template("judging/technical_form.html", form=form, id=None, repeat=repeat)


# Edit a previously-entered technical judging entry
@mod_judging.route("/technical/<int:technical_id>/edit",
                   methods=['GET', 'POST'])
def edit_technical(technical_id):
    technical = Technical.query.get(technical_id)
    form = TechnicalForm(obj=technical)
    del form.team_id

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(technical)
        db.session.commit()
        return redirect(url_for("review"))
    elif request.method == 'POST':
        flash('Failed validation', 'danger alert-auto-dismiss')
    return render_template("judging/technical_form.html", form=form,
                           team_id=technical.team.number, id=technical.id)


# Delete a technical judging entry
@mod_judging.route("/technical/<int:technical_id>/delete",
                   methods=['GET', 'POST'])
def delete_technical(technical_id):
    technical = Technical.query.get(technical_id)
    if request.method == 'POST':
        db.session.delete(technical)
        db.session.commit()
        return redirect(url_for("review"))
    return render_template("delete.html",
                           identifier="technical evaluation for team %d"
                           % technical.team.number)


# Add a core values judging entry
@mod_judging.route('/core_values/new', methods=['GET', 'POST'])
def add_core_values():
    teams = Team.query.all()

    if not teams:
        return render_template("no_teams.html")

    form = CoreValuesForm()
    form.team_id.choices = [(t.id, t.number) for t in
                            sortTeamsWithPlaceholder(teams)]

    # Gather and preset the team ID field if provided in URL
    preselected_team = request.args.get('team_id', default=None, type=int)
    if preselected_team is not None:
        form.team_id.data = preselected_team

    repeat = request.args.get('repeat', default=False, type=bool)

    if request.method == 'POST' and request.form['end'] == 'reset':
        return redirect(url_for(".add_core_values", repeat = True))
    elif request.method == 'POST' and request.form['end'] == 'submit' and form.validate_on_submit():
        core_values = CoreValues()
        form.populate_obj(core_values)
        db.session.add(core_values)
        db.session.commit()
        if repeat:
            flash('Added core values score for %s' % (core_values.team.number), 'success')
            return redirect(url_for(".add_core_values", repeat = True))
        else:
            return redirect(url_for("review"))
    elif request.method == 'POST':
        flash('Failed validation', 'danger alert-auto-dismiss')
    return render_template("judging/core_values_form.html", form=form, id=None, repeat=repeat)


# Edit a previously-entered core values judging entry
@mod_judging.route("/core_values/<int:core_values_id>/edit",
                   methods=['GET', 'POST'])
def edit_core_values(core_values_id):
    core_values = CoreValues.query.get(core_values_id)
    form = CoreValuesForm(obj=core_values)
    del form.team_id

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(core_values)
        db.session.commit()
        return redirect(url_for("review"))
    elif request.method == 'POST':
        flash('Failed validation', 'danger alert-auto-dismiss')
    return render_template("judging/core_values_form.html", form=form,
                           team_id=core_values.team.number, id=core_values.id)


# Delete a core values judging entry
@mod_judging.route("/core_values/<int:core_values_id>/delete",
                   methods=['GET', 'POST'])
def delete_core_values(core_values_id):
    core_values = CoreValues.query.get(core_values_id)
    if request.method == 'POST':
        db.session.delete(core_values)
        db.session.commit()
        return redirect(url_for("review"))
    return render_template("delete.html",
                           identifier="core values evaluation for team %d"
                           % core_values.team.number)


# Sort teams by number
def by_team(team):
    return team.number
