import re
import json
from argparse import ArgumentParser
from os.path import exists


def scrub_field(val: str | int | float | bool | None) -> str:
    val_type = type(val)
    if val_type == str:
        return re.sub('\w', "*", val)
    elif val_type == int or val_type == float:
        return scrub_field(str(val))
    elif val_type == bool:
        return "-"

    return val


def scrub(input: dict, sensitive_fields: list[str], scrub_all: bool = False) -> dict:
    output = {}
    # I'm assuming there are no duplicate keys in this object
    # (excluding nested objects' keys)
    for key, val in input.items():
        # these could be written much more compactly,
        # but for the sake of comprehension I'm writing them out explicitly
        if type(val) == dict:
            if key in sensitive_fields or scrub_all:
                # if the key matches a sensitive field,
                # or is the child of a sensitive field (i.e. "scrub_all" == True)
                # then we recursively scrub ALL the fields
                output[key] = scrub(val, sensitive_fields, scrub_all=True)
            else:
                # if this key is not sensitive, we continue looking for sensitive nested keys
                output[key] = scrub(val, sensitive_fields, scrub_all=False)
        elif type(val) == list:
            output[key] = handle_list(key, val, sensitive_fields)
        else:
            if key in sensitive_fields or scrub_all:
                output[key] = scrub_field(val)
            else:
                output[key] = val

    return output


def handle_list(key: str, val: list[any], sensitive_fields: list[str]):
    output = []
    for inner_val in val:
        if type(inner_val) == dict:
            output.append(scrub(inner_val, sensitive_fields, key in sensitive_fields))
        elif type(inner_val) == list:
            output.append(handle_list(key, inner_val, sensitive_fields))
        else:
            output.append(scrub_field(inner_val) if key in sensitive_fields else inner_val)

    return output





def check_valid_file(filename: str, ext:str):
    if not exists(filename) or not filename.endswith(ext):
        print(f"{filename} is not valid")
        exit(code=1)






if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('sensitive_fields_filename')
    parser.add_argument('input_filename')
    args = parser.parse_args()

    #I wanted auto-completion and type checking,
    # and the IDE wasn't giving it to me if I just used args.*
    input_filename: str = args.input_filename
    sensitive_fields_filename : str = args.sensitive_fields_filename

    check_valid_file(input_filename, ".json")
    check_valid_file(sensitive_fields_filename, ".txt")

    input = json.load(open(input_filename))
    sensitive_fields = [name.strip() for name in open(sensitive_fields_filename, "r").readlines()]

    result = scrub(input,  sensitive_fields)

    print(json.loads(result))

