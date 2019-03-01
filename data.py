import json
import psycopg2
import re
from psycopg2.extras import RealDictCursor


class Data:
    def __init__(self):
        # self.db_connection = psycopg2.connect(host="postgreDB",
        self.db_connection = psycopg2.connect(host="localhost",
                                              database="wg_forge_db",
                                              user="wg_forge",
                                              password="42a")

        self.cur = self.db_connection.cursor()

        self.VALIDITY_CHECKER = {
            'attribute': self.__check_attribute,
            'order': self.__check_order,
            'offset': self.__check_number,
            'limit': self.__check_number,
        }

    def __del__(self):
        self.db_connection.commit()

        self.cur.close()
        self.db_connection.close()

    def __check_attribute(self, value):
        return value in ['name', 'color', 'tail_length', 'whiskers_length']

    def __check_order(self, value):
        return value in ['asc', 'desc']

    def __check_number(self, value):
        if re.match(r"^[0-9]*$", value):
            return True
        else:
            return False

    def __param_exist(self, parameter):
        return parameter in self.VALIDITY_CHECKER

    def __param_valid(self, parameter, value):
        value_lowered = value.lower()
        return self.VALIDITY_CHECKER[parameter](value_lowered)

    def __select_parameters(self, gross_params):
        parameters = {}
        errors = []

        if not gross_params:
            return parameters, errors

        for parameter in gross_params:
            param_lower = parameter.lower()

            if self.__param_exist(param_lower):
                if self.__param_valid(param_lower, gross_params[parameter]):
                    parameters[param_lower] = gross_params[parameter]
                else:
                    errors.append(f'Parameter \'{parameter}\' has invalid ' +
                                  f'value: \'{gross_params[parameter]}\'')
            else:
                errors.append(f'Invalid parameter: \'{parameter}\'.')

        return parameters, errors

    def __get_sql_request(self, parameters):
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
        parameters = {}
        errors = []
        parameters, errors = self.__select_parameters(gross_params)

        if errors:
            return json.dumps(errors, ensure_ascii=False, indent=2)

        sql_request = self.__get_sql_request(parameters)
        self.cur.execute(sql_request)

        columns = ('name', 'color', 'tail_length', 'whiskers_length')
        results = []

        for row in self.cur.fetchall():
            results.append(dict(zip(columns, row)))

        return json.dumps(results, indent=2)
