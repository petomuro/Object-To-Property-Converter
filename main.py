import json


def process(parsed_object):
    ''' This function accepts a nested dictionary as argument
        and iterate over all values of nested dictionaries.
    '''
    # Iterate over all key-value pairs of dict argument
    for key, value in parsed_object.items():
        # Check if value is of dict type
        if isinstance(value, dict):
            # If value is dict then iterate over all its values
            for pair in process(value):
                yield (key, *pair)
        else:
            # If value is not dict type then yield the value
            yield (key, value)


def convert_to_property(processed_objects):
    ''' This function convert objects to a property.
        Customize it according to your needs.
    '''
    # Creates temporary property
    temp_object = []

    # Iterate over all objects
    for object in processed_objects:
        s = str(object[:-1]).replace('(', '').replace(')', '').replace(' ', '').replace("'", '')
        s_property = s.replace(',', '_').upper()
        s_value = s.replace(',', '.')
        s_full = s_property + ': computed(() => i18n.global.t(' + s_value + ')),'
        temp_object.append(s_full)

    # Return array of created properties
    return temp_object


def export_to_file(processed_objects):
    ''' This function export properties to file.
        Customize it according to your needs.
    '''
    with open("output.txt", "w") as txt_file:
        for object in processed_objects:
            txt_file.write(''.join(object) + "\n")


if __name__ == "__main__":
    raw_object = '''
    {
        "productDialog": {
            "header": {
                "title": "Product details"
            }
        },
        "product": {
            "header": {
                "title": "Manage products"
            },
            "main": {
                "id": {
                    "title": "Id"
                },
                "textField": {
                    "title": "Text field",
                    "error": "Text field is required."
                },
                "booleanField": {
                    "title": "Boolean field"
                },
                "bigDecimalField": {
                    "title": "Big decimal field"
                },
                "dateField": {
                    "title": "Date field"
                },
                "datetimeField": {
                    "title": "Datetime field"
                },
                "enumField": {
                    "title": "Enum field"
                },
                "countryField": {
                    "title": "Country field"
                }
            },
            "footer": {
                "title": "Showing {first} to {last} of {totalRecords} products"
            }
        },
        "deleteProductDialog": {
            "main": {
                "title": "Are you sure you want to delete {productName}?"
            }
        },
        "deleteProductsDialog": {
            "main": {
                "title": "Are you sure you want to delete the selected products?"
            }
        }
    }
    '''

    parsed_object = json.loads(raw_object)
    processed_objects = []

    for pair in process(parsed_object):
        processed_objects.append(pair)

    processed_objects = convert_to_property(processed_objects)
    export_to_file(processed_objects)
