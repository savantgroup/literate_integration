"""Console scripts for generating documentation."""

import re
import json


CAPITALS = re.compile('[A-Z]')
LEADING_SPACE = re.compile('^\s*')


def _to_title(name):
    """Generate a title from a class name.

    Args:
        name: The name of the class.

    Returns:
        A markdown title from the class name.

    """
    uppers = CAPITALS.findall(name)
    # The first string will be blank -- it should start with a capital.
    lowers = CAPITALS.split(name)[1:]
    new_name = ' '.join([
        ''.join([x, y]) for x, y in zip(uppers, lowers)
    ])
    return '## {}'.format(new_name)


def _get_leading_space(line):
    spaces = LEADING_SPACE.findall(line)
    if len(spaces) > 0:
        return len(spaces[0])
    return 0


def _format_docstring(docstring):
    lines = docstring.split('\n')
    if len(lines) == 0:
        return docstring

    subtitle = lines[0]
    remaining = lines[1:]
    if len(remaining) > 0:
        indentation = _get_leading_space(remaining[0])
        remaining = [x[indentation:] for x in remaining]
    ret = '### {}\n\n{}'.format(subtitle, '\n'.join(remaining))
    return ret


def _format_example(test_class):
    try:
        data = json.dumps(test_class.data)
    except Exception as ex:
        raise Exception(
            'data "{}" must be valid json: {}'.format(data, ex)
        )
    request = 'curl -X {} -d \'{}\' {}'.format(
        test_class.request_method,
        data,
        test_class.url,
    )
    return '### Example:\n\n```\n{}\n```'.format(request)


def generate_rest_documentation(test_class):
    """Generate documentation from a LiterateRESTTest.

    The docstring in the LiterateRESTTest will be passed as the
    main description of the example request.  The first line of
    the docstring will be made into a level-3 title.  The rest should
    be valid markdown and will be passed in as-is.

    Args:
        test_class: A subclass of LiterateRESTTest.

    Returns:
        A string representation of the LiterateRESTTest.
        The string will be valid markdown.

    """
    title = _to_title(test_class.__name__)
    body = _format_docstring(test_class.__doc__)
    example = _format_example(test_class)

    return '\n'.join([
        title,
        '',
        body,
        example,
        '',
    ])
