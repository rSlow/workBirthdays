import re

from jinja2 import Template


def render_template(template: Template, context: dict | None = None):
    if context is None:
        context = dict()

    rendered = template.render(**context)
    rendered = rendered.replace("\n", " ")
    rendered = rendered.replace("<br>", "\n")
    rendered = re.sub(" +", " ", rendered).replace(" .", ".").replace(" ,", ",")
    rendered = "\n".join(line.strip() for line in rendered.split("\n"))

    return rendered
