def check_endpoint_info(sent_data, expected_data):
    for data in expected_data:
        if(sent_data.get(data) == None):
            return f"the {data} parameter is required"

def fill_optional_data(sent_data, original_data, expected_data):
    for data in expected_data:
        if(sent_data.get(data) != None):
            original_data[data] = sent_data[data]
    return original_data