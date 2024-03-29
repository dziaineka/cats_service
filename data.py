import json
import psycopg2
import re


class Data:
    def __init__(self):
        self.db_connection = psycopg2.connect(host="postgreDB",
                                              database="wg_forge_db",
                                              user="wg_forge",
                                              password="42a")

        self.cur = self.db_connection.cursor()

        self.SELECT_PARAMS = {
            'attribute': self.__check_attribute,
            'order': self.__check_order,
            'offset': self.__check_number,
            'limit': self.__check_number,
        }

        self.INSERT_PARAMS = {
            'name': self.__check_dummy,
            'color': self.__check_dummy,
            'tail_length': self.__check_number,
            'whiskers_length': self.__check_number,
        }

    def __del__(self):
        self.db_connection.commit()

        self.cur.close()
        self.db_connection.close()

    @staticmethod
    def __check_dummy(value):
        return True

    @staticmethod
    def __check_attribute(value):
        return value in ['name', 'color', 'tail_length', 'whiskers_length']

    @staticmethod
    def __check_order(value):
        return value in ['asc', 'desc']

    @staticmethod
    def __check_number(value):
        if re.match(r"^[0-9]*$", value):
            return True
        else:
            return False

    @staticmethod
    def __param_exist(parameter, validator):
        return parameter in validator

    @staticmethod
    def __param_valid(parameter, value, validator):
        value_lowered = str(value).lower()
        return validator[parameter](value_lowered)

    def __get_parameters(self, gross_params, validator):
        parameters = {}
        errors = []

        if not gross_params:
            return parameters, errors

        for parameter in gross_params:
            param_lower = parameter.lower()

            if self.__param_exist(param_lower, validator):
                if self.__param_valid(param_lower,
                                      gross_params[parameter],
                                      validator):
                    parameters[param_lower] = str(gross_params[parameter])
                else:
                    errors.append(f'Parameter \'{parameter}\' has invalid ' +
                                  f'value: \'{gross_params[parameter]}\'')
            else:
                errors.append(f'Invalid parameter: \'{parameter}\'.')

        return parameters, errors

    @staticmethod
    def __get_select_sql_request(parameters):
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

    @staticmethod
    def __get_insert_sql_request(parameters):
        sql = 'INSERT INTO cats ('

        fields = ''

        for field in parameters.keys():
            fields += field + ', '

        sql += fields[:-2] + ') '

        values = ''

        for value in parameters.values():
            values += '\'' + value + '\', '

        sql += 'VALUES (' + values[:-2] + ')'

        return sql + ';'

    @staticmethod
    def __get_insert_parameters(gross_params):
        parameters = {}
        errors = []

        if not gross_params:
            errors.append('Please, provide cat to save in DB.')

        return parameters, errors

    def get_cats(self, gross_params=None):
        parameters = {}
        errors = []
        parameters, errors = self.__get_parameters(gross_params,
                                                   self.SELECT_PARAMS)

        if errors:
            return json.dumps(errors, ensure_ascii=False, indent=2)

        sql_request = self.__get_select_sql_request(parameters)

        try:
            self.cur.execute(sql_request)
        except psycopg2.InternalError as exc:
            self.cur.execute("ROLLBACK")
            errors.append(str(exc))
            return json.dumps(errors, ensure_ascii=False,  indent=2)

        columns = ('name', 'color', 'tail_length', 'whiskers_length')
        results = []

        for row in self.cur.fetchall():
            results.append(dict(zip(columns, row)))

        return json.dumps(results, indent=2)

    def add_cat(self, gross_params):
        parameters = {}
        errors = []

        try:
            params_json = json.loads(gross_params)
        except (json.decoder.JSONDecodeError, TypeError) as exc:
            errors.append(str(exc))
            return json.dumps(errors, ensure_ascii=False, indent=2)

        parameters, errors = self.__get_parameters(params_json,
                                                   self.INSERT_PARAMS)

        if not parameters:
            errors.append('Provide cat parameters, please.')

        if errors:
            return json.dumps(errors, ensure_ascii=False, indent=2)

        sql_request = self.__get_insert_sql_request(parameters)

        try:
            self.cur.execute(sql_request)
        except psycopg2.IntegrityError as exc:
            self.cur.execute("ROLLBACK")
            errors.append(str(exc))
            return json.dumps(errors, ensure_ascii=False,  indent=2)

        self.db_connection.commit()

        return json.dumps(['Inserted successfully'], indent=2)
