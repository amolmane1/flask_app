from datetime import datetime, timedelta
import dateutil.parser as parser
from itertools import chain
import pandas as pd

import logging

logger = logging.getLogger(__name__)


class Transformer:
    def __init__(self, incoming_data, feature_names, predictor):
        self.incoming_data = incoming_data
        self.feature_names_by_dtype = feature_names
        self.feature_names = list(chain.from_iterable(self.feature_names_by_dtype))
        self.predictor = predictor
        self.calculated_fields = self.predictor['data_set_details']['calculated_fields']
        self.calculated_fields_to_include = None
        self.prediction_date = None
        self.x = None
        # self.date_field = self.predictor['event_Date_Field']
        self.date_field = 'date'

    def run(self):
        if self.get_prediction_date():
            if self.convert_incoming_data_to_dataframe():
                if self.set_datatypes():
                    if self.compute_calculated_fields():
                        return self.x, self.prediction_date

    def get_prediction_date(self):
        date_format = self.predictor['data_set_details']['date_format']
        try:
            incoming_data_date = self.incoming_data[self.date_field]
        except KeyError:
            logging.error("Date field: {0} is required".format(self.date_field))
            return False

        try:
            self.prediction_date = datetime.strptime(incoming_data_date, date_format)
        except ValueError:
            self.prediction_date = parser.parse(incoming_data_date)
        except TypeError:
            logging.error("Incoming date: {0} is not in expected date format: {1}".format(incoming_data_date, date_format))
            return False

        if self.predictor['model_type_full'] == 'Future Values':
            self.prediction_date = (self.prediction_date + timedelta(minutes=self.predictor['fv_Prediction_Horizon'])).strftime(date_format)

        return True

    def convert_incoming_data_to_dataframe(self):
        self.calculated_fields_to_include = []
        if self.predictor:
            for calculated_field in self.calculated_fields:
                if calculated_field['include_In_Predictions']:
                    self.calculated_fields_to_include.append(calculated_field['name'])
        missing_features = list(set(self.feature_names) - set(self.incoming_data.keys()) - set(self.calculated_fields_to_include))
        if missing_features:
            logging.error('Missing fields: {0}'.format(missing_features))
            return False
        else:
            self.x = pd.DataFrame(self.incoming_data, index=[0])
            self.x = self.x[self.feature_names]
        return True

    def set_datatypes(self):
        try:
            for col in self.feature_names_by_dtype[2]:
                self.x[col] = pd.to_datetime(self.x[col], errors='coerce')
            for col in self.feature_names_by_dtype[0]:
                self.x[col] = pd.to_numeric(self.x[col], errors='coerce')
            for col in self.feature_names_by_dtype[1]:
                self.x[col] = self.x[col].astype(str)
        except:
            logging.error('Error setting datatypes')
            return False
        return True

    def compute_calculated_fields(self):
        for calculated_field in self.calculated_fields:
            if calculated_field.get('include_In_Predictions'):
                try:
                    self.x.eval(calculated_field['name'] + ' = ' + calculated_field['formula'], inplace=True)
                except:
                    logging.error("Failed to compute calculated field: {0} with formula: {1}".format(calculated_field['name'],
                                                                                                     calculated_field['formula']))
                    return False
        return True
