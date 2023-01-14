# example.py
from typing import List, TypeVar, Optional, Dict, Any
import strawberry

# The dataset to be paginated
user_data = [
  {
    "id": 1,
    "name": "Norman Osborn",
    "occupation": "Founder, Oscorp Industries",
    "age": 42
  },
  {
    "id": 2,
    "name": "Peter Parker",
    "occupation": "Freelance Photographer, The Daily Bugle",
    "age": 20
  },
  {
    "id": 3,
    "name": "Harold Osborn",
    "occupation": "President, Oscorp Industries",
    "age": 19
  },
  {
    "id": 4,
    "name": "Eddie Brock",
    "occupation": "Journalist, The Eddie Brock Report",
    "age": 20
  }
]


@strawberry.type
class User:
    name: str = strawberry.field(
        description="The name of the user."
    )
    occupation: str = strawberry.field(
        description="The occupation of the user."
    )
    age: int = strawberry.field(
        description="The age of the user."
    )

    @staticmethod
    def from_row(row: Dict[str, Any]):
        return User(
            name=row['name'],
            occupation=row['occupation'],
            age=row['age']
        )


GenericType = TypeVar("GenericType")


@strawberry.type
class PaginationWindow(List[GenericType]):
    items: List[GenericType] = strawberry.field(
        description="The list of items in this pagination window."
    )

    total_items_count: int = strawberry.field(
        description="Total items count in the dataset."
    )


def matches(item, filters):
    """
    Test whether the item matches the given filters.
    This demo only supports filtering by string fields.
    """

    for attr_name, val in filters.items():
        if val not in item[attr_name]:
            return False
    return True


def get_pagination_window(
        dataset: List[GenericType],
        ItemType: type,
        order_by: str,
        limit: Optional[int] = None,
        offset: int = 0,
        filters: dict[str, str] = {}) \
        -> PaginationWindow:
    """
    Get one pagination window on the given dataset for the given limit
    and offset, ordered by the given attribute and filtered using the
    given filter
    """

    # validate the limit
    if limit is not None and limit < 1:
        raise Exception(f'limit ({limit}) must be greater than 0')

    # sort the dataset
    dataset.sort(key=lambda x: x[order_by])

    # filter the sorted dataset
    if filters:
        dataset = list(filter(lambda x: matches(x, filters), dataset))

    # validate the offset
    if not 0 <= offset < len(dataset):
        raise Exception(f'offset ({offset}) is out of range '
                        f'(0-{len(dataset) - 1})')

    # calculate the total number of items in the filtered dataset
    total_items_count = len(dataset)

    # slice the relevant items
    items = dataset[offset:] if limit is None \
        else dataset[offset:offset + limit]

    # convert the items from the dataset type to the schema type
    items = [ItemType.from_row(x) for x in items]

    return PaginationWindow(
        items=items,
        total_items_count=total_items_count
    )


@strawberry.type
class Query:
    @strawberry.field(description="Get a list of users.")
    def users(self,
              order_by: str,
              limit: Optional[int] = None,
              offset: int = 0,
              name: Optional[str] = None,
              occupation: Optional[str] = None
              ) -> PaginationWindow[User]:

        filters = {}

        if name:
            filters['name'] = name

        if occupation:
            filters['occupation'] = occupation

        return get_pagination_window(
            dataset=user_data,
            ItemType=User,
            order_by=order_by,
            limit=limit,
            offset=offset,
            filters=filters
        )


schema = strawberry.Schema(query=Query)
