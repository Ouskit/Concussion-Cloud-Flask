from api.models.VEPData import VepData, VepDataSchema
from api.models.PlayHistory import PlayHistorySchema
from api.utils.responses import response_with
from api.utils import responses as resp
from flask import Blueprint, request, url_for, current_app
from sqlalchemy.sql import text
import gzip
import json

vep_routes = Blueprint("vep_routes", __name__)


@vep_routes.route('/receive', methods=['POST'])
def create_vep():
    file = request.data

    try:
        aa = gzip.decompress(file).decode()
        tt = aa.split('\n');
        for i in tt:
            row_data = json.loads(i)
            data = {}
            # Create Play History
            if row_data['_dataType'] == 'DataSync.Entity.ScopeStartEntity':
                data['username'] = row_data['_userId']
                data['sessionid'] = row_data['_scopeId']
                data['gameid'] = row_data['projectId']
                play_history_schema = PlayHistorySchema()
                play_history = play_history_schema.load(data)
                play_history.create()

            # Store VEP EEG Data
            elif row_data['_dataType'] == 'Data.EEGData':
                data['gameid'] = row_data['projectId']
                data['username'] = row_data['_userId']
                data['sessionid'] = row_data['_scopeId']
                data['eeg_value'] = row_data['Data']['rawVal']
                vep_schema = VepDataSchema()
                vep = vep_schema.load(data)
                vep.create()

        return response_with(resp.SUCCESS_201)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

    #sql_query = text("INSERT INTO `VEPData` ( `gameid`, `sessionid`, `username`, `eeg_value` ) VALUES ( :gameid, :sessionid, :username, :eeg_value )")
    #query_data = db.engine.execute(sql_query, gameid=data['gameid'], sessionid=data['sessionid'], username=data['username'], eeg_value=data['eeg_value'])

