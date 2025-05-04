"""
Utility functions for the unsigned_generator package.
"""
from typing import Any
from jsonpath_rw import Child, Fields, Root, parse


class Recipient:
    """Recipient information from roster file.

    Attributes:
        name (str): Name of recipient
        pubkey (str): Public key of recipient
        identity (str): Email of recipient
        additional_fields (object): Additional fields
        information(eg. date and html)
    """

    def __init__(self, fields):
        """Object with mandatory arguments

        Args:
            fields (object): Additional fields information(eg. date and HTML)
        """

        # Name & identity aren't required fields in v3.
        # Mostly keeping it for compatibility
        # with existing rosters but if it's a problem,
        # we can remove it and individual's can
        # add them in via 'additional_per_recipient_fields'
        self.name = fields["name"]
        # self.pubkey = fields.pop('pubkey')
        self.identity = fields["email"]
        # self.record_id = fields.pop('record_id')
        self.slug = fields.pop("slug")
        self.additional_fields = fields

class Utils:
    """
    A collection of utility methods for the unsigned_generator package.
    """
    @staticmethod
    def get_path(match: str):
        """Return an iterator based upon MATCH.PATH. Each item
        is a path component, start from outer most item.

        Args:
            match: Path from additional fields

        Return:
            Return path elements from additional fields
        """
        if match.context is not None:
            for path_element in Utils().get_path(match.context):
                yield path_element
            yield str(match.path)

    @staticmethod
    def recurse(child, fields_reverse: list):
        """Update JSON dictionary PATH with VALUE. Return updated JSON

        Args:
            child (str): Path parse from additional fields
            fields_reverse (str): List of fields in additional fields

        Return:
            Append fields information
        """
        if isinstance(child, Fields):
            fields_reverse.append(child.fields[0])
        else:
            if not isinstance(child, Child):
                raise TypeError("unexpected input")
            if not isinstance(child.left, Root):
                Utils().recurse(child.left, fields_reverse)
            Utils().recurse(child.right, fields_reverse)

    @staticmethod
    def update_json(json: object, path: str, value: str):
        """Update JSON dictionary PATH with VALUE. Return updated JSON

        Args:
            json (object): Json of template file
            path (str): Additional field path string
            value (str): Value of given path

        Return:
            Json value with recipient details
        """
        try:
            first = next(path)
            # Check if item is an array
            if first.startswith("[") and first.endswith("]"):
                try:
                    first = int(first[1:-1])
                except ValueError:
                    pass
            json[first] = Utils().update_json(json[first], path, value)
            return json

        except StopIteration:
            return value

    @staticmethod
    def set_field(raw_json: object, path: str, value: str):
        """This function will create json for additional field and additional per
        recipient field from recipient details.

        Args:
            raw_json (dict): Template json assertion
            path (str): Additional field path string
            value (str): Value of given path

        Return:
            Create row josn for each field
        """
        jp = parse(path)
        matches = jp.find(raw_json)
        if matches:
            for match in matches:
                jsonpath_expr = Utils().get_path(match)
                raw_json = Utils().update_json(raw_json, jsonpath_expr, value)
        else:
            fields = []
            Utils().recurse(jp, fields)
            temp_json = raw_json
            for idx, f in enumerate(fields):
                if f in temp_json:
                    temp_json = temp_json[f]
                elif idx == len(fields) - 1:
                    temp_json[f] = value
                else:
                    msg = "path is not valid! : " + ".".join(fields)
                    raise ValueError(msg)

        return raw_json
