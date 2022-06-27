import pandas as pd
import numpy as np
from pydomo import Domo
from pydomo.datasets import DataSetRequest, Schema, Column, ColumnType
from io import StringIO
from os import getenv
import json

# load current config from the conf.json file in the project directory
with open('conf.json') as f:
    CONF = json.loads(f.read())

# initialize domo client with domo API credentials
domo = Domo(**CONF["creds"])

# download the data from sweethawk and normalize
data = pd.read_csv(CONF["csv_url"])
data['date'] = pd.to_datetime(data['date'])
data['reason'] = data['reason'].replace(np.nan, '')
data['nps_reason'] = data['nps_reason'].replace(np.nan,'')

# export to csv held in StringIO 
csv = StringIO()
data.to_csv(csv, index=False)


if "dsid" in CONF.keys():
    # skip this if the dataset id is already defined in conf.json
    pass
else:
    # create a new dataset if dsid is not defined and save the dsid to conf.json
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

# push the data to the domo dataset
domo.datasets.data_import(CONF['dsid'], csv.getvalue())
