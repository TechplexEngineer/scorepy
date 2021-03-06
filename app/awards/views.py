from flask import Blueprint, render_template, flash, request, redirect, \
    url_for
from flask.ext.login import login_required
from app import db
from app.util import create_pdf, sortTeamsWithPlaceholder
from app.teams.models import Team
from models import AwardWinner, AwardCategory
from forms import AwardWinnerForm
from app.models import EventSettings

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_awards = Blueprint('awards', __name__, url_prefix='/awards')


# Restrict access to authorized users only
@mod_awards.before_request
@login_required
def before_request():
    pass


# Awards page
@mod_awards.route("/", methods=['GET'])
def index():
    teams = Team.query.all()

    if not teams:
        return render_template("no_teams.html")

    award_winners = AwardWinner.query.all()

    award_winners = sorted(award_winners, key=lambda x: x.friendly_award_name)
    for winner in award_winners:
        winner.category_name = AwardCategory(winner.category_id).friendly_name
    return render_template("awards/awards.html", award_winners=award_winners)


# Award winner report
@mod_awards.route("/awards_report.pdf")
def awards_pdf():
    award_winners = AwardWinner.query.all()
    title = EventSettings.query.first().name

    award_winners = sorted(award_winners, key=lambda x: x.friendly_award_name)
    for winner in award_winners:
        winner.category_name = AwardCategory(winner.category_id).friendly_name

    awards = render_template("awards/awards_report.html",
                             award_winners=award_winners,
                             title="Award Winners Report: %s" % title)

    pdf = create_pdf(awards, 'awards_report.pdf')
    return pdf


# Edit a previously-entered award winner
@mod_awards.route("/<int:award_winner_id>/assign", methods=['GET', 'POST'])
def assign_award_winner(award_winner_id):
    teams = Team.query.all()

    if not teams:
        return render_template("no_teams.html")

    award_winner = AwardWinner.query.get(award_winner_id)
    form = AwardWinnerForm(obj=award_winner)
    form.team_id.choices = [(t.id, t.number) for t in
                            sortTeamsWithPlaceholder(teams)]

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(award_winner)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation', 'danger alert-auto-dismiss')
    return render_template("awards/award_winner_form.html", form=form, award=award_winner.friendly_award_name)


# Delete an award winner
@mod_awards.route("/<int:award_winner_id>/delete", methods=['GET', 'POST'])
def clear_award_winner(award_winner_id):
    award_winner = AwardWinner.query.get(award_winner_id)
    if request.method == 'POST':
        award_winner.team_id = None
        db.session.add(award_winner)
        db.session.commit()
        return redirect(url_for(".index"))
    return render_template("delete.html", identifier="award winner for %s"
                                                     % award_winner.friendly_award_name)


@mod_awards.route("/populate_slots", methods=['GET', 'POST'])
def populate_slots():
    if request.method == 'POST':
        # Remove any existing winners
        for existing_winner in AwardWinner.query.all():
            db.session.delete(existing_winner)
        db.session.commit()

        # Seed new slots
        slots = []
        is_championship = EventSettings.query.first().is_championship

        for category in AwardCategory:
            if is_championship or category == AwardCategory.Champions or category == AwardCategory.Robot_Performance:
                for i in range(0, 2):
                    slots.append(AwardWinner(category_id=category.value, place=i))
            else:
                slots.append(AwardWinner(category_id=category.value, place=0))

        for slot in slots:
            db.session.add(slot)
        db.session.commit()
        flash("Populated slots", 'success')
        return redirect(url_for(".index"))
    return render_template("awards/populate_slots.html")


# Sort teams by number
def by_team(team):
    return team.number
