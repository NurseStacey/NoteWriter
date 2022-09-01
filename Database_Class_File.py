import mysql.connector
from template import *
from tkinter import messagebox
class MyDatabaseClass():

    def __init__(self):

        try:
            self.the_db = mysql.connector.connect(
                host='localhost', user='root', password='B@rton', database='EHR')
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              password="B@rton"
            )

            mycursor = mydb.cursor()

            mycursor.execute("CREATE DATABASE EHR")
            self.the_db = mysql.connector.connect(
                host='localhost', user='root', password='B@rton', database='EHR')

        self.check_needed_tables_interfaces()

    def check_needed_tables_interfaces(self):
        #check if required tables are present
        table_names = self.get_table_names()

        #get needed tables
        self.needed_tables = []

        try:
            this_file = open('required_tables.txt', 'r')
        except FileNotFoundError:
            messagebox.showerror('Error', 'Error - Required Tables File is Missing')
            return

        for one_line in this_file.readlines():
            one_table={}
            one_table['name'] = one_line.partition('-')[0]
            one_table['sql'] = one_line.partition('-')[2]
            self.needed_tables.append(one_table)

        this_file.close()

        for one_needed_table in self.needed_tables:
            if not one_needed_table['name'] in table_names:
                if self.preform_SQL_statement(one_needed_table['sql'])=='Error':
                    messagebox.showerror('Error', 'Error Creating Needed Tables')
                    return('Error')

        #get needed interfaces
        self.needed_interfaces = []
        try:
            this_file = open('required_interfaces.txt', 'r')
        except FileNotFoundError:
            return            
        
        for one_line in this_file.readlines():
            one_line=one_line.replace('\n','')
            if one_line=='':
                break
            
            one_interface = {}
            interface_data = one_line.split(',')

            one_interface['interface_name'] = interface_data[0]
            one_interface['record_name_formula'] =interface_data[1]
            one_interface['table_name'] =interface_data[2]
            self.needed_interfaces.append(one_interface)

        this_file.close()



        interface_names = self.get_interface_names()

        for one_interface in self.needed_interfaces:
            if not one_interface['interface_name'] in interface_names:
                the_fields = self.get_required_interface_fields(
                    one_interface['interface_name'])
                if self.add_new_interface(one_interface['interface_name'], one_interface['table_name'], one_interface['record_name_formula'], the_fields, True) == 'Error':
                    messagebox.showerror(
                        'Error', 'Error Creating Needed Interfaces')
                    return('Error')

    def Is_Table_Required(self, table_name):
        if [x for x in self.needed_tables if x['name']==table_name] == []:
            return False
        else: return True

    def Is_Interface_Required(self, interface_name):
        if [x for x in self.needed_interfaces if x['interface_name'] == interface_name] == []:
            return False
        else: return True

    def get_required_interface_fields(self, interface_name):
        this_file = open(interface_name+'.txt', 'r')

        return_values = []
        for one_line in this_file.readlines():
            this_field = {}
            one_line_data = one_line.split(',')
            this_field['field_name'] = one_line_data[0]
            this_field['field_label'] = one_line_data[1]
            this_field['field_order'] = int(one_line_data[2])
            this_field['field_type'] = one_line_data[3]
            this_field['linked_table'] = one_line_data[4]
            return_values.append(this_field)
        
        return return_values


    def preform_SQL_statement(self, _SQL):

        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        return 'No Error'

    def get_cursor(self):
        return self.the_db.cursor()

    def get_table_names(self):

        _SQL = "SELECT table_name FROM information_schema.tables"
        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        results = mycursor.fetchall()
        return [item[0] for item in results]

    def get_interface_names(self):
        _SQL = "SELECT DISTINCT interface_name from interfaces"

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

        _SQL = "UPDATE interfaces SET interface_name =" + chr(34) + \
             new_name + chr(34) +" WHERE interface_name = " + chr(34) + old_name + chr(34) 
        
        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        _SQL = "UPDATE interface_fields SET interface_name =" + chr(34) + \
             new_name + chr(34) +" WHERE interface_name = " + chr(34) + old_name + chr(34) 
        
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
            if field_type[index] in [ 'string', 'text']:
                _SQL += chr(34)
                _SQL +=field_data[index]
                _SQL += chr(34)
            elif field_type[index] in ['date']:
                _SQL += chr(34)
                _SQL += field_data[index].strftime('%Y-%m-%d %H:%M:%S')
                _SQL += chr(34)
            elif field_type[index] in ['double','integer', 'bool', 'linked_table']:
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

    def add_new_interface(self, interface_name, table_name, record_name_formula, all_fields, required_table):
        this_file=None
        if required_table:
            file_name=interface_name + '.txt'
            this_file = open(file_name,'w')

        field_data = []

        for one_field in all_fields:

            field_data.append((interface_name, 
                            one_field['field_name'],
                               one_field['field_label'],
                              one_field['field_order'],
                               one_field['field_type'],
                               one_field['linked_table']))

            if required_table:
                this_file.write(one_field['field_name'])
                this_file.write(',')
                this_file.write(one_field['field_label'])
                this_file.write(',')
                this_file.write(str(one_field['field_order']))
                this_file.write(',')
                this_file.write(one_field['field_type'])
                this_file.write(',')
                this_file.write(one_field['linked_table'])
                this_file.write('\n')
        
        if required_table:
            this_file.close()

        _SQL = "INSERT INTO interface_fields (interface_name, field_name, field_label, field_order, field_type, linked_table) VALUES (%s, %s, %s, %s, %s, %s)"


        try:
            mycursor = self.get_cursor()
            mycursor.executemany(_SQL, field_data)
            self.the_db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'
        
        _SQL = "INSERT INTO interfaces (interface_name, record_name_formula, Interface_Table) VALUES ("
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

        if not required_table:
            return 'No_Error'

        try:
            this_file = open('required_interfaces.txt', 'r')
            all_lines = this_file.readlines()
            this_file.close()
        except IOError:
            all_lines = []

        this_file = open('required_interfaces.txt', 'w')
        need_to_add = True

        for one_line in all_lines:
            if interface_name == one_line.partition(',')[0]:
                this_file.write(interface_name)
                this_file.write(',')
                this_file.write(record_name_formula)
                this_file.write(',')
                this_file.write(table_name)
                this_file.write('\n')
                need_to_add = False
            else:
                this_file.write(one_line)

        if need_to_add:
            this_file.write(interface_name)
            this_file.write(',')
            this_file.write(record_name_formula)
            this_file.write(',')
            this_file.write(table_name)
            this_file.write('\n')            


        this_file.close()

        return 'No_Error'
 

    def add_new_table(self, table_name, all_fields, required_table):

        linked_fields=[]

        _SQL = 'CREATE TABLE ' + table_name + ' (Record_ID int NOT NULL AUTO_INCREMENT, '       

        for one_field in all_fields:
            
            if one_field['field_type']=='linked_table':
                linked_fields.append(one_field)            
            
            _SQL += self.one_new_field_query_string(one_field)


        _SQL += 'PRIMARY KEY (Record_ID)'

        for one_linked_table in linked_fields:
            this_interface_info = self.get_interface_info(one_linked_table['linked_table'])

            _SQL += ', FOREIGN KEY ('
            _SQL +=one_linked_table['field_name']
            _SQL +=')  REFERENCES '
            _SQL += this_interface_info['interface_table']
            _SQL +='(Record_ID)'
        
        _SQL += ')'

        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        if not required_table:
            return 'No_Error'

        try:
            this_file = open('required_tables.txt','r')
            all_lines = this_file.readlines()
            this_file.close()
        except IOError:
            all_lines=[]

        this_file = open('required_tables.txt','w')
        need_to_add = True

        for one_line in all_lines:
            if table_name == one_line.partition('-')[0]:
                this_file.write(table_name + '-' + _SQL + '\n')
                need_to_add = False
            else:
                this_file.write(one_line)

        if need_to_add:
            this_file.write(table_name + '-' + _SQL + '\n')

        this_file.close()

        return 'No_Error'

    def one_new_field_query_string(self, one_field):

        _SQL = ''
        if one_field['field_type'] == 'string':
            _SQL += one_field['field_name']
            _SQL += ' VARCHAR(255)'
            # _SQL += str(one_field.length)
            _SQL += ', '
        elif one_field['field_type'] == 'text':
            _SQL += one_field['field_name']
            _SQL += ' MEDIUMTEXT, '
        elif one_field['field_type'] == 'integer':
            _SQL += one_field['field_name']
            _SQL += ' SMALLINT, '
        elif one_field['field_type'] == 'double':
            _SQL += one_field['field_name']
            _SQL += ' FLOAT(10,4), '
        elif one_field['field_type'] == 'date':
            _SQL += one_field['field_name']
            _SQL += ' DATETIME, '
        elif one_field['field_type'] == 'bool':
            _SQL += one_field['field_name']
            _SQL += ' BOOL, '
        elif one_field['field_type'] in ['multi_linked_table','linked_table']:
            _SQL += one_field['field_name']
            _SQL += ' int, '
        return _SQL

    # def one_new_field_query_string(self, one_field):

    #     _SQL = ''
    #     if one_field.type == 'string':
    #         _SQL += one_field.name
    #         _SQL += ' VARCHAR(255)'
    #         # _SQL += str(one_field.length)
    #         _SQL += ', '
    #     elif one_field.type == 'text':
    #         _SQL += one_field.name
    #         _SQL += ' MEDIUMTEXT, '
    #     elif one_field.type == 'integer':
    #         _SQL += one_field.name
    #         _SQL += ' SMALLINT, '
    #     elif one_field.type == 'double':
    #         _SQL += one_field.name
    #         _SQL += ' FLOAT(10,4), '
    #     elif one_field.type == 'date':
    #         _SQL += one_field.name
    #         _SQL += ' DATETIME, '
    #     elif one_field.type == 'bool':
    #         _SQL += one_field.name
    #         _SQL += ' BOOL, '
    #     elif one_field.type == 'linked_table':
    #         _SQL += one_field.name
    #         _SQL += ' int, '
    #     return _SQL

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

        _SQL = 'DELETE FROM interfaces WHERE interface_name= '



        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
            self.the_db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        _SQL = "INSERT INTO interfaces (interface_name, record_name_formula, interface_table) VALUES"
        
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
            mycursor.execute(_SQL)
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
                            one_field['field_name'],
                               one_field['field_label'],
                               int(one_field['field_order']),
                            one_field['field_type'],
                            one_field['linked_table']))
        
        _SQL = "INSERT INTO interface_fields (interface_name, field_name, field_label, field_order, field_type, linked_table) VALUES (%s, %s, %s, %s, %s, %s)"

        try:
            mycursor = self.get_cursor()
            mycursor.executemany(_SQL, field_data)
            self.the_db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

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
            _SQL = 'DELETE FROM interface_fields WHERE field_name= '
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

        if self.Is_Table_Required(which_table):
            messagebox.showerror('Error','Table is required.  Cannot be deleted')
            return 'Error'

        _SQL = 'DROP TABLE ' + which_table
        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        return 'No_Error'
        
    def delete_interface(self, which_interface):

        if self.Is_Interface_Required(which_interface):
            messagebox.showerror('Error','Interface is required.  Cannot be deleted')
            return 'Error'

        _SQL = "SELECT interface_table from interfaces WHERE interface_name="
        _SQL += chr(34)
        _SQL += which_interface
        _SQL += chr(34)
        _SQL += " GROUP BY interface_table"

        mycursor = self.get_cursor()
        mycursor.execute(_SQL)
        tables = [x[0] for x in mycursor.fetchall()]

        for one_table in tables:
            if self.delete_table(one_table)=='Error':
                return 'Error'

        _SQL = 'DELETE FROM interface_fields WHERE interface_name= '
        _SQL += chr(34)
        _SQL += which_interface
        _SQL += chr(34)

        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
            self.the_db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        _SQL = 'DELETE FROM interfaces WHERE interface_name= '
        _SQL += chr(34)
        _SQL += which_interface
        _SQL += chr(34)

        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
            self.the_db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        return 'No_Error'

    def get_record_names(self, which_interface, record_name_formula):

        record_values = []
        fields_needed = get_fields_for_record_name_formula(record_name_formula)

        _SQL = "SELECT Record_ID, "
        for one_field in fields_needed:
            _SQL += one_field
            _SQL += ','

        _SQL = _SQL[0:len(_SQL)-1]

        _SQL += ' from '
        _SQL += which_interface

        try:
            mycursor = self.get_cursor()
            mycursor.execute(_SQL)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 'Error'

        records = mycursor.fetchall()
        columnNames = [column[0] for column in mycursor.description]

        for one_record in records:
            record_values.append(dict(zip(columnNames, one_record)))

        return get_names(record_values, record_name_formula)

    def get_interface_info(self, which_interface):

        _SQL = "SELECT * from interfaces WHERE interface_name="
        _SQL += chr(34)
        _SQL += which_interface
        _SQL += chr(34)
 

        mycursor = self.get_cursor()
        mycursor.execute(_SQL)

        records = mycursor.fetchall()
        columnNames = [column[0] for column in mycursor.description]

        return (dict(zip(columnNames, records[0])))

    def get_interface_records(self, which_interface):

        _SQL = "SELECT * from interface_fields WHERE interface_name="
        _SQL += chr(34)
        _SQL += which_interface
        _SQL += chr(34)
        _SQL += ' ORDER BY field_order'

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
