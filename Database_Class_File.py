import mysql.connector

class MyDatabaseClass():

    def __init__(self):

        self.the_db = mysql.connector.connect(
            host='localhost', user='root', password='B@rton', database='EHR')

    def get_cursor(self):
        return self.the_db.cursor()

    def get_list_current_tables(self):
        _SQL = "SHOW TABLES"

        mycursor = self.get_cursor()
        mycursor.execute(_SQL)
        results = mycursor.fetchall()
        return [item[0] for item in results]

    def get_column_info(self, table):

        _SQL = "SHOW COLUMNS FROM " + table

        mycursor = self.get_cursor()
        mycursor.execute(_SQL)
        return mycursor.fetchall()

    def change_table_name(self, old_name, new_name):

        _SQL = "ALTER TABLE  " + old_name + " RENAME TO " + new_name
        mycursor = self.get_cursor()
        mycursor.execute(_SQL)

    def add_new_table(self, table_name, all_fields):

        query_string = 'CREATE TABLE ' + table_name + ' ('       

        for one_field in all_fields:
            query_string += self.one_new_field_query_string(one_field)

        query_string = query_string[0:len(query_string)-2]
        query_string += ')'
        mycursor = self.get_cursor()
        mycursor.execute(query_string)

    def one_new_field_query_string(self, one_field):

        query_string = ''
        if one_field.type == 'string':
            query_string += one_field.name
            query_string += ' VARCHAR('
            query_string += str(one_field.length)
            query_string += '), '
        elif one_field.type == 'text':
            query_string += one_field.name
            query_string += ' MEDIUMTEXT, '
        elif one_field.type == 'integer':
            query_string += one_field.name
            query_string += ' SMALLINT, '
        elif one_field.type == 'double':
            query_string += one_field.name
            query_string += ' FLOAT(10,4), '
        elif one_field.type == 'date':
            query_string += one_field.name
            query_string += ' DATETIME, '

        return query_string

    def add_new_fields(self, table_name, new_fields):

        query_string = 'ALTER TABLE ' + table_name + ' ADD ('

        for one_field in new_fields:
            query_string += self.one_new_field_query_string(one_field)

        query_string = query_string[0:len(query_string)-2]
        query_string += ')'
        mycursor = self.get_cursor()
        mycursor.execute(query_string)

    def removed_fields(self, table_name, fields_to_remove):
        query_string = 'ALTER TABLE ' + table_name + ' '

        for one_field in fields_to_remove:
            query_string += "DROP COLUMN "
            query_string += one_field.name
            query_string += ", "

        query_string = query_string[0:len(query_string)-2]
        query_string += ';'
        mycursor = self.get_cursor()
        mycursor.execute(query_string)
