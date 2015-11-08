from flask.ext.wtf import Form
from wtforms import SelectField, RadioField
from models import RobotScore


class ScoreForm(Form):
    team_id = SelectField(u'Team', coerce=int)
    round_number = SelectField(u'Round',
                               choices=[(1, '1'), (2, '2'), (3, '3')],
                               coerce=int)
    tree_branch_is_closer = RadioField(u'Is tree branch closer to mat than \
                                       power lines',
                                       choices=[(False, 'No'), (True, 'Yes')],
                                       coerce=bool,
                                       default=False)
    tree_branch_is_intact = RadioField(u'Is tree branch model intact',
                                       choices=[(False, 'No'), (True, 'Yes')],
                                       coerce=bool,
                                       default=False)
    cargo_plane_location = RadioField(u'Cargo plane location',
                                      choices=[('0', 'None'),
                                               ('1', 'Yellow only'),
                                               ('2', 'Light blue')],
                                      default=0)

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.score = None

    def validate(self):
        # Base validation
        rv = Form.validate(self)
        if not rv:
            return False

        # Team-ID and round-number fields don't exist on an 'edit' form
        if not self.team_id or not self.round_number:
            return True

        # New score being entered, check if one already exists for team/ round
        score = RobotScore.query.filter_by(round_number=self.round_number.data,
                                           team_id=self.team_id.data).first()
        if score is not None:
            self.round_number.errors.append("Score already exists for this \
                                            round")
            return False

        self.score = score
        return True
