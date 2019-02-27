import json
import psycopg2
from psycopg2.extras import RealDictCursor


class Data:
    def __init__(self):
        # self.db_connection = psycopg2.connect(host="postgreDB",
        self.db_connection = psycopg2.connect(host="localhost",
                                              database="wg_forge_db",
                                              user="wg_forge",
                                              password="42a")

        self.cur = self.db_connection.cursor()

        self.VALID_VALUES = {
            'attribute': ['name', 'color', 'tail_length', 'whiskers_length'],
            'order': ['asc', 'desc'],
        }

        self.PARAMS_TYPE = {
            'attribute': 'name',
            'order': 'asc',
            'offset': 1,
            'limit': 1,
        }

    def __del__(self):
        self.db_connection.commit()

        self.cur.close()
        self.db_connection.close()

    def param_exist(self, parameter):
        return parameter in self.PARAMS_TYPE

    def param_valid(self, parameter, value):
        value_lowered = value

        if isinstance(value, str):
            value_lowered = value.lower()

        if not isinstance(value_lowered, type(self.PARAMS_TYPE[parameter])):
            return False

        if parameter not in self.VALID_VALUES:
            return True

        if value_lowered in self.VALID_VALUES[parameter]:
            return True
        else:
            return False

    def select_parameters(self, gross_params):
        parameters = {}
        errors = []

        for parameter in gross_params:
            param_lower = parameter.lower()

            if self.param_exist(param_lower):
                if self.param_valid(param_lower, gross_params[parameter]):
                    parameters[param_lower] = gross_params[parameter]
                else:
                    errors.append(f'Parameter \'{parameter}\' has invalid ' +
                                  f'value: \'{gross_params[parameter]}\'')
            else:
                errors.append(f'Invalid parameter: \'{parameter}\'.')

        return parameters, errors

    def get_sql_request(self, parameters):
        sql = 'SELECT * ' +\
            'FROM cats '

        if 'attribute' in parameters:
            if 'order' in parameters:
                sql = sql + 'ORDER BY {} '.format(parameters['attribute']) +\
                    '{} '.format(parameters['order'])

        if 'limit' in parameters:
            sql += 'LIMIT {} '.format(parameters['limit'])

        if 'offset' in parameters:
            sql += 'OFFSET {} '.format(parameters['offset'])

        return sql + ';'

    def get_cats(self, gross_params=None):
        parameters, errors = self.select_parameters(gross_params)

        if errors:
            return json.dumps(errors, ensure_ascii=False, indent=2)

        print(json.dumps(parameters, ensure_ascii=False, indent=2))

        sql_request = self.get_sql_request(parameters)

        return sql_request
