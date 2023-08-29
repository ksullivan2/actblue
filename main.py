sample_input = {
    "name": "Kelly Doe",
    "email": "kdoe@example.com",
    "id": 12324,
    "phone": "5551234567"
}

sample_output = {
    "name": "***** ***",
    "email": "****@*******.***",
    "id": 12324,
    "phone": "**********"
}


def scrub_field(val: str) -> str:
    return val


def scrub(input: dict, sensitive_fields: list[str], scrub_all: bool = False):
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
        else:
          if key in sensitive_fields or scrub_all:
              output[key] = scrub_field(val)
          else:
              output[key] = val

    return output