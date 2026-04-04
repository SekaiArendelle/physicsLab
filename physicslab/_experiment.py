from physicslab import enums
from physicslab._typing import Set, List, Optional, Union

TYPE_TAG_CIRCUIT = "Type-0"
TYPE_TAG_CELESTIAL = "Type-3"
TYPE_TAG_ELECTROMAGNETISM = "Type-4"


def serialize_introduction(introduction: Optional[str]) -> Optional[list[str]]:
    """Convert introduction text to the ``Summary.Description`` save format."""
    if introduction is None:
        return None
    return introduction.split("\n")


def deserialize_introduction(description: Optional[Union[list, str]]) -> Optional[str]:
    """Convert ``Summary.Description`` data back to introduction text."""
    if isinstance(description, list):
        # Check type of all items in the list
        if not all(isinstance(item, str) for item in description):
            raise TypeError(
                f"description must be of type `list[str] | str | None`, but got value {description} of type {type(description).__name__}"
            )
        return "\n".join(description)
    if isinstance(description, str):
        return description
    if description is None:
        return None
    raise TypeError(
        f"description must be of type `list[str] | str | None`, but got value {description} of type {type(description).__name__}"
    )


def serialize_tags(tags: Set[enums.Tag], type_tag: str) -> List[str]:
    if not isinstance(type_tag, str):
        raise TypeError(
            f"type_tag must be of type `str`, but got value {type_tag} of type {type(type_tag).__name__}"
        )
    _tags = set(tags)
    return [type_tag] + sorted(tag.value for tag in _tags)


def construct_tags(raw_tags: Optional[List[str]], type_tag: str) -> Set[enums.Tag]:
    if not isinstance(type_tag, str):
        raise TypeError(
            f"type_tag must be of type `str`, but got value {type_tag} of type {type(type_tag).__name__}"
        )
    if raw_tags is None:
        return set()
    if not isinstance(raw_tags, list):
        raise TypeError(
            f"tags must be of type `list[str] | None`, but got value {raw_tags} of type {type(raw_tags).__name__}"
        )
    if not all(isinstance(tag, str) for tag in raw_tags):
        raise TypeError(
            f"tags must be of type `list[str] | None`, but got value {raw_tags} of type {type(raw_tags).__name__}"
        )

    result: Set[enums.Tag] = set()
    for raw_tag in raw_tags:
        if raw_tag == type_tag:
            continue
        result.add(enums.Tag(raw_tag))
    return result
