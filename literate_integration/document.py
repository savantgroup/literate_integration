"""Console scripts for generating documentation."""

import re
import json

from .models import LiterateRESTTest


MAX_LENGTH = 60

CAPITALS = re.compile('[A-Z]')
LEADING_SPACE = re.compile('^\s*')
SECTION_DATA = re.compile(' -\w')
CODE_CLASS = '{ .example-code }'
H2_CLASS = '{ .integration-test }'


def _to_title(name, add_class=True):
    """Generate a title from a class name.

    Args:
        name: The name of the class.
        add_class: If true, adds a pandoc-style class statement
            to the title.

    Returns:
        A markdown title from the class name.

    """
    uppers = CAPITALS.findall(name)
    # The first string will be blank -- it should start with a capital.
    lowers = CAPITALS.split(name)[1:]
    new_name = ' '.join([
        ''.join([x, y]) for x, y in zip(uppers, lowers)
    ])
    return '## {} {}'.format(
        new_name,
        H2_CLASS if add_class else '',
    )


def get_leading_whitespace(line):
    spaces = LEADING_SPACE.findall(line)
    if len(spaces) > 0:
        return len(spaces[0])
    return 0


def remove_leading_whitespace(lines):
    """Remove leading whitespace, based on the first line.

    Args:
        lines: A list of strings which may be indented.

    Returns:
        A list of strings without indentation.

    """
    spaces = get_leading_whitespace(lines[0])
    return [x[spaces:] for x in lines]


def _format_docstring(docstring):
    """Format the class docstring.

    Expects the docstring to be a single line and (optionally) a blank
    line followed by the rest of the body.  The rest of the body will
    have its main indentation removed.

    Args:
        docstring: The docstring from the class.

    Returns:
        The docstring, with indentation removed and a title created
        from the first line.

    """
    lines = docstring.split('\n')
    if len(lines) == 0:
        return docstring

    subtitle = lines[0]
    remaining = lines[2:]
    if len(remaining) > 0:
        indentation = get_leading_whitespace(remaining[0])
        remaining = [x[indentation:] for x in remaining]
    ret = '*{}*\n\n{}'.format(subtitle, '\n'.join(remaining))
    return ret


def format_json(raw_data):
    data = json.dumps(raw_data)
    if len(data) < MAX_LENGTH:
        return data

    # Get the data with indents (it will have at least 3)
    data = json.dumps(raw_data, indent=4)
    data = data.split('\n')
    # Put five spaces before each line but the first.
    for i in range(1, len(data)):
        data[i] = ' ' * 5 + data[i]
    return '\n'.join(data)


def _format_example(TestClass, add_class=True):
    test_class = TestClass()
    try:
        data = format_json(test_class.data)
    except Exception as ex:
        raise Exception(
            'data "{}" must be valid json: {}'.format(test_class.data, ex)
        )
    request = 'curl -H {} -X {} -d \'{}\''.format(
        '"Content-Type: application/json"',
        test_class.request_method,
        data,
    )
    wrapped_request = wrap_curl(request)
    wrapped = '\n' in wrapped_request
    long_url = (len(wrapped_request) + len(test_class.url) + 1) > MAX_LENGTH
    if wrapped or long_url:
        request = wrapped_request + ' \\\n' + ' ' * 3 + test_class.url
    else:
        request = wrapped_request + ' ' + test_class.url
    return '### Example:\n\n```{}\n{}\n```'.format(
        CODE_CLASS if add_class else '',
        request,
    )


def _format_setup(TestClass):
    """Describe necessary setup steps.

    Only uses everything after the first line.
    (That is, the docstring should have the first line, followed
    by an empty line, followed by the body.)

    Args:
        TestClass: The LiterateRESTTest subclass.

    Returns:
        The body of the docstring with leading indentation removed,
        and a title added.

    """
    docstring = TestClass.setUp.__doc__
    same_as_default = docstring == LiterateRESTTest.setUp.__doc__
    not_specified = docstring == '' or docstring is None
    if same_as_default or not_specified:
        return None

    # Take everything after the first newline and empty line.
    # That is,
    remaining = docstring.split('\n')[2:]
    if remaining == []:
        return None
    return '### Setup Required\n\n{}'.format(
        '\n'.join(remove_leading_whitespace(remaining))
    )


def wrap_curl(curl):
    """Wrap a curl example.

    Assumes there is no url in the curl statement yet.

    Args:
        curl (str): The curl statement.

    Returns:
        The formatted curl statement.

    """
    if len(curl) < MAX_LENGTH:
        return curl

    flags = SECTION_DATA.findall(curl)  # len(flags) == n

    contents = SECTION_DATA.split(curl)  # len(content) == n+1

    # After this, len(contents) == len(flags)
    ret = [contents.pop(0)]

    # If we wrap once, we always want to wrap.
    wrapped = False
    first_line = True

    for flag, content in zip(flags, contents):
        prev = ret.pop(len(ret) - 1)
        if wrapped or len(prev) + len(flag) + len(content) > MAX_LENGTH:
            if not first_line:
                ret.append(prev)
                ret.append(' ' * 4 + flag + content)
            else:
                ret.append(prev + flag + content)
            wrapped = True
        else:
            ret.append(prev + flag + content)
        first_line = False

    # Add backslashes
    for i in range(len(ret) - 1):
        ret[i] = ret[i] + ' \\'

    return '\n'.join(ret)


def generate_rest_documentation(TestClass):
    """Generate documentation from a LiterateRESTTest.

    The docstring in the LiterateRESTTest will be passed as the
    main description of the example request.  The first line of
    the docstring will be made into a level-3 title.  The rest should
    be valid markdown and will be passed in as-is.

    Args:
        TestClass: A subclass of LiterateRESTTest.

    Returns:
        A string representation of the LiterateRESTTest.
        The string will be valid markdown.

    """
    title = _to_title(TestClass.__name__)
    body = _format_docstring(TestClass.__doc__)
    example = _format_example(TestClass)
    setup = _format_setup(TestClass)

    documentation = [title, '', body, setup, example, '']

    return '\n'.join([
        section for section in documentation
        if section is not None
    ])
