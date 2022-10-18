import json


def process(parsed_object):
    """
    This function accepts a nested dictionary as argument
    and iterate over all values of nested dictionaries.
    :param parsed_object: Json object to process
    :return: Tuple
    """
    # Iterate over all key-value pairs of dict argument
    for key, value in parsed_object.items():
        # Check if value is of dict type
        if isinstance(value, dict):
            # If value is dict then iterate over all its values
            for pair in process(value):
                yield key, *pair
        else:
            # If value is not dict type then yield the value
            yield key, value


def replace_camel_case(s):
    """
    This function check if string contains a camel case character and
    add comma before camel case character
    :param s: String
    :return: Modified string
    """
    # For camel case
    for index, ch in enumerate(s):
        # Check for uppercase character
        if ch.isupper():
            return False, s[0:index] + ',' + s[index].lower() + s[index + 1:]
        else:
            continue

    return True, s


def convert_to_property(processed_objects):
    """
    This function convert objects to a property.
    Customize it according to your needs.
    :param processed_objects: Processed json object
    :return: Object
    """
    # Creates temporary property
    temp_object = []

    # Iterate over all objects
    for object in processed_objects:
        s = str(object[1:-1]).replace('(', '').replace(')', '').replace(' ', '').replace("'", '')

        while True:
            (done, s) = replace_camel_case(s)

            if done:
                break

        s2 = str(object[:-1]).replace('(', '').replace(')', '').replace(' ', '').replace("'", '')
        s_property = s.replace(',', '_').upper()
        s_value = s2.replace(',', '.')
        s_full = s_property + f": computed(() => i18n.global.t('{s_value}')),"
        temp_object.append(s_full)

    # Return array of created properties
    return temp_object


def export_to_file(processed_objects):
    """
    This function export properties to file.
    Customize it according to your needs.
    :param processed_objects: Processed json objects to export
    :return: File
    """
    with open("output.txt", "w") as txt_file:
        for object in processed_objects:
            txt_file.write(''.join(object) + "\n")


if __name__ == "__main__":
    with open('object.json') as f:
        parsed_object = json.load(f)
        
    processed_objects = []

    for pair in process(parsed_object):
        processed_objects.append(pair)

    processed_objects = convert_to_property(processed_objects)
    export_to_file(processed_objects)
