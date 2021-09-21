from api.utils.database import db, ma

class VepData(db.Model):
    __tablename__ = 'VEPData'
    uid = db.Column(db.BIGINT, primary_key=True, nullable=False)
    gameid = db.Column(db.String(100), nullable=False)
    sessionid = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    eeg_value = db.Column(db.Integer, nullable=False)

    def __init__(self, gameid, sessionid, username, eeg_value):
        self.gameid = gameid
        self.sessionid = sessionid
        self.username = username
        self.eeg_value = eeg_value

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<Post %r data>' % self.username


class VepDataSchema(ma.SQLAlchemyAutoSchema):
    """
    SQLAlchemySchema automatically generates fields
    """

    class Meta:
        model = VepData
        sqla_session = db.session
        load_instance = True
