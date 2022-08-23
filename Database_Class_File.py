import mysql.connector

class MyDatabaseClass():

    def __init__(self):

        self.the_db = mysql.connector.connect(
            host='localhost', user='root', password='B@rton', database='EHR')

    def get_cursor(self):
        return self.the_db.cursor()

    def get_interface_names(self):
        _SQL = "SELECT DISTINCT Interface_Name from interfaces"

        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        results = mycursor.fetchall()
        return [item[0] for item in results]
        
    def get_list_current_tables(self):
        _SQL = "SHOW TABLES"

        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        results = mycursor.fetchall()
        return [item[0] for item in results]

    def get_column_info(self, table):

        _SQL = "SHOW COLUMNS FROM " + table

        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        return mycursor.fetchall()

    def change_interface_name(self, old_name, new_name):

        if new_name in self.get_interface_names():
            return('Duplicate')

        _SQL = "UPDATE interfaces SET Interface_Name =" + chr(34) + \
             new_name + chr(34) +" WHERE Interface_Name = " + chr(34) + old_name + chr(34) 
        
        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        _SQL = "UPDATE interface_fields SET Interface_Name =" + chr(34) + \
             new_name + chr(34) +" WHERE Interface_Name = " + chr(34) + old_name + chr(34) 
        
        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'
            
        return 'No_Error'

    # def change_table_name_interface(self,interface, old_name, new_name):

    #     if self.change_table_name(old_name, new_name)=='Error':
    #         return 'Error'

    #     _SQL = "UPDATE interfaces SET Table_Name ="  + chr(34) + \
    #          new_name + chr(34) + " WHERE  = Table_Name" + chr(34) + old_name + chr(34) + " AND WHERE Interface_Name = "  + chr(34) + interface  + chr(34)
        
    #     try:
    #         mycursor = self.get_cursor()
    #         mycursor.execute(_SQL)
    #     except mysql.connector.Error as err:
    #         print("Something went wrong: {}".format(err))
    #         return 'Error'

    #     return 'No_Error'

    def change_table_name(self, old_name, new_name):

        _SQL = "ALTER TABLE  " + old_name + " RENAME TO " + new_name
        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'
        
        return 'No_Error'


    def add_record(self, table, all_data):

        _SQL = "INSERT INTO "
        _SQL += table
        _SQL += " ("

        field_data = []
        field_type = []

        for one_field in all_data:
            _SQL += one_field['column']
            _SQL += ", "

            field_data.append(one_field['value'])
            field_type.append(one_field['type'])

        _SQL = _SQL[:len(_SQL)-2]
        _SQL += ") VALUES ("  

        for index in range(len(field_type)):
            if field_type[index] == 'string':
                _SQL += chr(34)
                _SQL +=field_data[index]
                _SQL += chr(34)
            elif field_type[index] in ['double','integer']:
                _SQL += str(field_data[index])
            _SQL += ", "

        _SQL = _SQL[:len(_SQL)-2]
        _SQL += ") "
        
        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
            self.the_db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'
        
        return 'No_Error'

    def add_new_interface(self,interface_name, table_name, record_name_formula, all_fields):

        field_data = []
        for one_field in all_fields:
                
            field_data.append((interface_name, 
                            one_field.name,
                            one_field.label,
                            int(one_field.order),
                            one_field.type,
                            one_field.linked_table,
                           one_field.immutable=='Yes'))
        
        _SQL = "INSERT INTO interface_fields (Interface_Name, Field_Name, Field_Lable, Field_Order, Field_Type, Linked_Table, Immutable) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        try:
            mycursor = self.get_cursor()
            mycursor.executemany(_SQL, field_data)
            self.the_db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'
        
        _SQL = "INSERT INTO interfaces (Interface_Name, Record_Name_Formula, Interface_Table) VALUES ("
        #%s, %s, %s)"
        _SQL += chr(34)
        _SQL += interface_name
        _SQL += chr(34)
        _SQL += ", "
        _SQL += chr(34)
        _SQL += record_name_formula
        _SQL += chr(34)
        _SQL += ", "
        _SQL += chr(34)
        _SQL += table_name
        _SQL += chr(34)
        _SQL += ")"

        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
            self.the_db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        return 'No_Error'
 

    def add_new_table(self, table_name, all_fields):

        _SQL = 'CREATE TABLE ' + table_name + ' (Record_ID int NOT NULL AUTO_INCREMENT, '       

        for one_field in all_fields:
            _SQL += self.one_new_field_query_string(one_field)

        #_SQL = _SQL[0:len(_SQL)-2]
        _SQL += 'PRIMARY KEY (Record_ID))'
        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        return 'No_Error'

    def one_new_field_query_string(self, one_field):

        _SQL = ''
        if one_field.type == 'string':
            _SQL += one_field.name
            _SQL += ' VARCHAR(255)'
            # _SQL += str(one_field.length)
            _SQL += ', '
        elif one_field.type == 'text':
            _SQL += one_field.name
            _SQL += ' MEDIUMTEXT, '
        elif one_field.type == 'integer':
            _SQL += one_field.name
            _SQL += ' SMALLINT, '
        elif one_field.type == 'double':
            _SQL += one_field.name
            _SQL += ' FLOAT(10,4), '
        elif one_field.type == 'date':
            _SQL += one_field.name
            _SQL += ' DATETIME, '
        elif one_field.type == 'bool':
            _SQL += one_field.name
            _SQL += ' BOOL, '

        return _SQL

    def add_new_fields(self, table_name, new_fields):

        _SQL = 'ALTER TABLE ' + table_name + ' ADD ('

        for one_field in new_fields:
            _SQL += self.one_new_field_query_string(one_field)

        _SQL = _SQL[0:len(_SQL)-2]
        _SQL += ')'

        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        return 'No_Error'

    def update_one_record(self, table_name, record_ID, columns_to_update):

        _SQL = 'UPDATE '
        _SQL += table_name
        _SQL += ' SET '

        for one_column in columns_to_update:
            _SQL +=one_column['column_name'] 
            _SQL += ' = '
            
            if one_column['type']=='string':
                _SQL += chr(34)
                _SQL +=one_column['value']
                _SQL += chr(34)
            else:
                _SQL +=one_column['value']
            _SQL += ', '
  
        
        _SQL = _SQL[:len(_SQL)-2]
        _SQL += ' WHERE '
        _SQL += record_ID['column_name']
        _SQL += ' = '
        if record_ID['type'] == 'string':
            _SQL += chr(34)
            _SQL += record_ID['value']
            _SQL += chr(34)
        else:
            _SQL += record_ID['value']
            _SQL += ', '

        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
            self.the_db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        return 'No_Error'

    def update_interface(self, old_interface_name, interface_name, table_name, record_name_formula):

        _SQL = 'DELETE FROM interfaces WHERE Interface_Name= '



        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
            self.the_db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        _SQL = "INSERT INTO interfaces (Interface_Name, Record_Name_Formula, Interface_Table) VALUES"
        
        _SQL += '('
        _SQL += chr(34)
        _SQL += interface_name
        _SQL += chr(34)
        _SQL += ', '
        _SQL += chr(34)
        _SQL += record_name_formula
        _SQL += chr(34)
        _SQL += ', '
        _SQL += chr(34)
        _SQL += table_name
        _SQL += chr(34)
        _SQL += ')'
        

        try:
            mycursor = self.get_cursor()
            mycursor.executemany(_SQL, field_data)
            self.the_db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        return 'No_Error'

    def add_new_fields_interface(self, interface_name, table_name, new_fields):

        if self.add_new_fields(table_name, new_fields) == 'Error':
            return 'Error'

        field_data=[]
        for one_field in new_fields:
                
            field_data.append((interface_name, 
                            one_field.name,
                            one_field.label,
                            int(one_field.order),
                            one_field.type,
                            one_field.linked_table,
                           one_field.immutable=='Yes'))
        
        _SQL = "INSERT INTO interface_fields (Interface_Name, Field_Name, Field_Lable, Field_Order, Field_Type, Linked_Table, Immutable) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        try:
            mycursor = self.get_cursor()
            mycursor.executemany(_SQL, field_data)
            self.the_db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        # if self.add_new_interface(interface_name, table_name, interface_name_formula, new_fields) == 'Error':
        #     return 'Error'

        return 'No_Error'

    def remove_fields(self, table_name, fields_to_remove):
        _SQL = 'ALTER TABLE ' + table_name + ' '

        for one_field in fields_to_remove:
            _SQL += "DROP COLUMN "
            _SQL += one_field
            _SQL += ", "

        _SQL = _SQL[0:len(_SQL)-2]
        _SQL += ';'
        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        return 'No_Error'

    def remove_fields_interface(self, interface, table_name, fields_to_remove):

        if self.remove_fields(table_name, fields_to_remove)=='Error':
            return 'Error'

        for one_field in fields_to_remove:
            _SQL = 'DELETE FROM interface_fields WHERE field_Name= '
            _SQL += chr(34)
            _SQL += one_field
            _SQL += chr(34)
            try:
                mycursor = self.get_cursor()
                mycursor.execute(_SQL)
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))
                return 'Error'

        return 'No_Error'

    # def get_list_current_interfaces(self):
    #     _SQL = "SELECT Interface_Name from interfaces GROUP BY Interface_Name"
    #     mycursor = self.get_cursor()
    #     mycursor.execute(_SQL)
    #     results = [x[0] for x in mycursor.fetchall()]

    #     return results

    def delete_table(self, which_table):

        _SQL = 'DROP TABLE ' + which_table
        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        return 'No_Error'
        
    def delete_interface(self, which_interface):
        _SQL = "SELECT Interface_Table from interfaces WHERE Interface_Name="
        _SQL += chr(34)
        _SQL += which_interface
        _SQL += chr(34)
        _SQL += " GROUP BY Interface_Table"

        mycursor = self.get_cursor()
        mycursor.execute(_SQL)
        tables = [x[0] for x in mycursor.fetchall()]

        for one_table in tables:
            if self.delete_table(one_table)=='Error':
                return 'Error'

        _SQL = 'DELETE FROM interface_fields WHERE Interface_Name= '
        _SQL += chr(34)
        _SQL += which_interface
        _SQL += chr(34)

        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        return 'No_Error'

    def get_interface_info(self, which_interface):

        _SQL = "SELECT * from interfaces WHERE Interface_Name="
        _SQL += chr(34)
        _SQL += which_interface
        _SQL += chr(34)
 

        mycursor = self.get_cursor()
        mycursor.execute(_SQL)

        records = mycursor.fetchall()
        columnNames = [column[0] for column in mycursor.description]

        return (dict(zip(columnNames, records[0])))

    def get_interface_records(self, which_interface):

        _SQL = "SELECT * from interface_fields WHERE Interface_Name="
        _SQL += chr(34)
        _SQL += which_interface
        _SQL += chr(34)
        _SQL += ' ORDER BY Field_Order'

        mycursor = self.get_cursor()
        #mycursor = self.get_cursor(dictionary=True)
        # mycursor = self.cursor(dictionary=True)
        # mycursor = self.MySQLCursorDict()
        mycursor.execute(_SQL)

        records = mycursor.fetchall()
        columnNames = [column[0] for column in mycursor.description]

        return_value = []

        for one_record in records:
            return_value.append(dict(zip(columnNames, one_record)))

        return return_value
