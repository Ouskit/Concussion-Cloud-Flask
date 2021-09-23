from api.models.VEPData import VepData, VepDataSchema
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
            if row_data['_dataType'] == 'GameData.GameFlowData':
                pass

            # Store VEP EEG Data
            elif row_data['_dataType'] == 'Data.EEGData':
                data['gameid'] = '0000'
                data['username'] = 'okt'
                data['sessionid'] = '20210915'
                data['eeg_value'] = row_data['Data']['rawVal']
                vep_schema = VepDataSchema()
                vep = vep_schema.load(data)
                vep.create()
            else:
                print(row_data['Data']['_dataType'])
            #data['gameid'] = row_data['Data']['projectId']
            #data['sessionid'] = row_data['Data']['_scopeId']

        return response_with(resp.SUCCESS_201)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

    #sql_query = text("INSERT INTO `VEPData` ( `gameid`, `sessionid`, `username`, `eeg_value` ) VALUES ( :gameid, :sessionid, :username, :eeg_value )")
    #query_data = db.engine.execute(sql_query, gameid=data['gameid'], sessionid=data['sessionid'], username=data['username'], eeg_value=data['eeg_value'])

