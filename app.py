from flask import Flask, request, jsonify, make_response
from api.utils.database import db
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from api.routes.VEPData import vep_routes

app = Flask(__name__)

# TODO python decouple
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:wmlab57997@140.115.54.9:4000/game"

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(vep_routes, url_prefix='/api/v1/vep')


@app.route("/api/v1/test", methods=['GET', 'POST'])
def submit():
    content = request.json
    print(content)
    sql_cmd = """
        INSERT INTO `VEP Data` ( `gameid`, `sessionid`, `username`, `eeg value` )
                       VALUES
                       ( '0000', '20210915','okt', 55 );
        """

    query_data = db.engine.execute(sql_cmd)
    print(query_data)

    return 'OK'


if __name__ == '__main__':
    app.run()
