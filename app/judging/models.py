from app import db


class Presentation(db.Model):
    __tablename__ = 'presentation'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    # Research
    problem_identification = db.Column(db.Integer)
    sources_of_information = db.Column(db.Integer)
    problem_analysis = db.Column(db.Integer)
    existing_solutions = db.Column(db.Integer)

    # Innovative Solution
    team_solution = db.Column(db.Integer)
    innovation = db.Column(db.Integer)
    implementation = db.Column(db.Integer)

    # Presentation
    sharing = db.Column(db.Integer)
    creativity = db.Column(db.Integer)
    effectiveness = db.Column(db.Integer)

    @property
    def research_score(self):
        total = self.problem_identification + self.sources_of_information \
            + self.problem_analysis + self.existing_solutions
        return total/4.0

    @property
    def innovative_solution_score(self):
        total = self.team_solution + self.innovation + self.implementation
        return total/3.0

    @property
    def presentation_score(self):
        total = self.sharing + self.creativity + self.effectiveness
        return total/3.0

    @property
    def breakdown_string(self):
        return "%0.1f | %0.1f | %0.1f" % (self.research_score, self.innovative_solution_score, self.presentation_score)

    @property
    def overall_score(self):
        total = self.research_score \
            + self.innovative_solution_score \
            + self.presentation_score
        return total/3.0


class CoreValues(db.Model):
    __tablename__ = 'corevalues'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    # Teamwork
    effectiveness = db.Column(db.Integer)
    efficiency = db.Column(db.Integer)
    kids_do_the_work = db.Column(db.Integer)

    # GP
    inclusion = db.Column(db.Integer)
    respect = db.Column(db.Integer)
    coopertition = db.Column(db.Integer)

    # Inspiration
    discovery = db.Column(db.Integer)
    team_spirit = db.Column(db.Integer)
    integration = db.Column(db.Integer)

    @property
    def teamwork_score(self):
        total = self.effectiveness + self.efficiency + self.kids_do_the_work
        return total/3.0

    @property
    def gp_score(self):
        total = self.inclusion + self.respect + self.coopertition
        return total/3.0

    @property
    def inspiration_score(self):
        total = self.discovery + self.team_spirit + self.integration
        return total/3.0

    @property
    def breakdown_string(self):
        return "%0.1f | %0.1f | %0.1f" % (self.teamwork_score, self.gp_score, self.inspiration_score)

    @property
    def overall_score(self):
        total = self.teamwork_score + self.gp_score + self.inspiration_score
        return total/3.0


class Technical(db.Model):
    __tablename__ = 'technical'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    # Mechanical Design
    mechanical_durability = db.Column(db.Integer)
    mechanical_efficiency = db.Column(db.Integer)
    mechanization = db.Column(db.Integer)

    # Programming
    programming_quality = db.Column(db.Integer)
    programming_efficiency = db.Column(db.Integer)
    autonomous_navigation = db.Column(db.Integer)

    # Strategy and Innovation
    design_process = db.Column(db.Integer)
    mission_strategy = db.Column(db.Integer)
    innovation = db.Column(db.Integer)

    @property
    def mechanical_score(self):
        total = self.mechanical_durability + self.mechanical_efficiency \
            + self.mechanization
        return total/3.0

    @property
    def programming_score(self):
        total = self.programming_quality + self.programming_efficiency \
            + self.autonomous_navigation
        return total/3.0

    @property
    def strategy_innovation_score(self):
        total = self.design_process + self.mission_strategy + self.innovation
        return total/3.0

    @property
    def breakdown_string(self):
        return "%0.1f | %0.1f | %0.1f" % (self.mechanical_score, self.programming_score, self.strategy_innovation_score)

    @property
    def overall_score(self):
        total = self.mechanical_score + self.programming_score \
            + self.strategy_innovation_score
        return total/3.0
