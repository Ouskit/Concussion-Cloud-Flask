from api.models.VEPData import VepData, VepDataSchema
from api.utils.responses import response_with
from api.utils import responses as resp
from flask import Blueprint, request, url_for, current_app
from sqlalchemy.sql import text

vep_routes = Blueprint("vep_routes", __name__)


@vep_routes.route('/send', methods=['POST'])
def create_vep():
    data = request.get_json()
    #sql_query = text("INSERT INTO `VEPData` ( `gameid`, `sessionid`, `username`, `eeg_value` ) VALUES ( :gameid, :sessionid, :username, :eeg_value )")
    #query_data = db.engine.execute(sql_query, gameid=data['gameid'], sessionid=data['sessionid'], username=data['username'], eeg_value=data['eeg_value'])

    try:
        vep_schema = VepDataSchema()
        vep = vep_schema.load(data)
        vep.create()
        return response_with(resp.SUCCESS_201)
    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)

