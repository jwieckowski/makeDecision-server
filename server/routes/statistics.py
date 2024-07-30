# Copyright (c) 2024 Jakub Więckowski

from flask_restx import Resource
from werkzeug.exceptions import BadRequest
import datetime as dt
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd

# NAMESPACE
from .namespaces import v1 as api
path = '../logs'

@api.route('/stats/logs')
class StatisticsLogs(Resource):
    def get(self):    
        try:
            logs = {}
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and 'error' not in f]
            today = dt.datetime.today()
            today_str = today.strftime('%Y-%m-%d')
            today_str = '2023-12-21'
            week = today - dt.timedelta(days=7)
            week_str = week.strftime('%Y-%m-%d')
            month = today - dt.timedelta(days=30)
            month_str = month.strftime('%Y-%m-%d')

            for filename in onlyfiles:
                with open(f'{path}/{filename}', 'r') as f:
                    log_date = filename[-14:-4]

                    logs[log_date] = []
                    for line in f:
                        items = line.split(' -')
                        if items[0] not in logs[log_date]:
                            logs[log_date].append(items[0])

            if today_str not in list(logs.keys()):
                logs[today_str] = []

            week_logs, month_logs = [], []
            for key, val in logs.items():
                log_datetime = dt.datetime.strptime(key, '%Y-%m-%d')
                if log_datetime >= week:
                    week_logs.append(len(val))
                if log_datetime >= month:
                    month_logs.append(len(val))

            datelist = pd.date_range(dt.datetime.today() - dt.timedelta(days=7), periods=7).tolist()
            return {
                "response": {
                    "today": len(logs[today_str]),
                    "7": np.sum(week_logs).tolist(),
                    "30": np.sum(month_logs).tolist()
                }
            }
        except Exception as err:
            api.logger.info(str(err))
            e = BadRequest(str(err))
            raise e