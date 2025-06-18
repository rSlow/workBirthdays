from adaptix import Retort, NameStyle, name_mapping


def get_base_retort():
    return Retort(
        recipe=[
            name_mapping(name_style=NameStyle.LOWER_KEBAB)
        ]
    )
