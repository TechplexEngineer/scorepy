from app import db
from app.scoring.models import RobotScore
from app.judging.models import Presentation, Technical, Teamwork, TeamSpirit
from app.awards.models import AwardWinner


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(50))
    affiliation = db.Column(db.String(200))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    is_rookie = db.Column(db.Boolean)
    scores = db.relationship('RobotScore', backref='team')
    presentation = db.relationship('Presentation', uselist=False,
                                   backref='team')
    technical = db.relationship('Technical', uselist=False, backref='team')
    teamwork = db.relationship('Teamwork', uselist=False, backref='team')
    team_spirit = db.relationship('TeamSpirit', uselist=False, backref='team')
    awards = db.relationship('AwardWinner', backref='team')

    def __init(self, number, name, affiliation, city, state, is_rookie):
        self.number = number
        self.name = name
        self.affiliation = affiliation
        self.city = city
        self.state = state
        self.is_rookie = is_rookie
