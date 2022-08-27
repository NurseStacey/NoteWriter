import copy

def get_fields_for_record_name_formula(record_name_formula):

    return_values = []

    while not record_name_formula.find('<!-')==-1:
        start_value = record_name_formula.find('<!-') + 3
        end_value = record_name_formula.find('-!>')
        return_values.append(record_name_formula[start_value:end_value])

        record_name_formula = record_name_formula[end_value+3:]

    return return_values


def get_names(record_values, record_name_formula):
    return_values = []

    for one_record in record_values:
        one_name={}
        this_name=copy.deepcopy(record_name_formula)
        while not this_name.find('<!-') == -1:
            start_value = this_name.find('<!-') + 3
            end_value = this_name.find('-!>')
            this_field_name = this_name[start_value:end_value]
            this_name = this_name[:start_value-3] + \
                str(one_record[this_field_name]) + this_name[3+end_value:]

        one_name['Name']=this_name
        one_name['Record_ID']=one_record['Record_ID']
        return_values.append(one_name)

    return return_values