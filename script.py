#!/home/a683040/domo-sweethawk-surveys/.venv/bin/python3
import pandas as pd
import numpy as np
from pydomo import Domo
from pydomo.datasets import DataSetRequest, Schema, Column, ColumnType
from io import StringIO
from os import getenv
import json

with open('conf.json') as f:
    CONF = json.loads(f.read())

domo = Domo(**CONF["creds"])

data = pd.read_csv('https://zendesk.sweethawk.co/app/survey/responses.csv?user_token=mmNzdrXqGuJR3VKAog39UCT8')
data['date'] = pd.to_datetime(data['date'])
data['reason'] = data['reason'].replace(np.nan, '')
data['nps_reason'] = data['nps_reason'].replace(np.nan,'')

csv = StringIO()

data.to_csv(csv, index=False)

if "dsid" in CONF.keys():
    pass
else:
    dsr = DataSetRequest()
    dsr.name = 'ZenDesk Sweethawk Surveys'
    dsr.description = 'Zendesk Surveys Exported from Sweethawk'
    dsr.schema = Schema([
        Column(ColumnType.LONG,'ticket'),
        Column(ColumnType.STRING, 'brand'),
        Column(ColumnType.LONG, 'score'),
        Column(ColumnType.STRING, 'reason'),
        Column(ColumnType.DECIMAL, 'nps'),
        Column(ColumnType.STRING, 'nps_reason'),
        Column(ColumnType.DATE, 'date')
    ])

    dataset = domo.datasets.create(dsr)
    CONF['dsid'] = dataset['id']
    with open('conf.json', 'w') as f:
        f.write(json.dumps(CONF))

domo.datasets.data_import(CONF['dsid'], csv.getvalue())
