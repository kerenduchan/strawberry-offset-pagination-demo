# strawberry-offset-pagination-demo
A small demo project showing how to implement **offset-based pagination** 
using [Strawberry](https://strawberry.rocks/) GraphQL.

For more info , refer to the Strawberry 
[documentation](https://strawberry.rocks/docs/guides/pagination/offset-based) 
on offset-based pagination.

# Install

```
python -m venv virtualenv
source virtualenv/bin/activate
pip install 'strawberry-graphql[debug-server]'
```

# Run the Strawberry GraphQL server
```
strawberry server example:schema
```
You will get the following message:
```
Running strawberry on http://0.0.0.0:8000/graphql 🍓
```

# Query the server
Go to [http://0.0.0.0:8000/graphql](http://0.0.0.0:8000/graphql) to
open **GraphiQL**, and run the following query to get first two users, 
ordered by name:

```
{
  users(
    orderBy: "name",
    offset: 0,
    limit: 2
  ) {
    items {
      name
      age
      occupation
    }
    totalItemsCount
  }
}
```
The result should look like this: 
```
{
  "data": {
    "users": {
      "items": [
        {
          "name": "Eddie Brock",
          "age": 20,
          "occupation": "Journalist, The Eddie Brock Report"
        },
        {
          "name": "Harold Osborn",
          "age": 19,
          "occupation": "President, Oscorp Industries"
        }
      ],
      "totalItemsCount": 4
    }
  }
}
```

The result contains:
- `items` - A list of the users in this pagination window 
- `totalItemsCount` - The total number of pages in the filtered dataset

Get the next page of users by running the same query, after incrementing 
`offset` by `limit`.

Repeat until `offset` reaches `totalItemsCount`.

## Filtering

Run the following query to get the first two users, ordered by name, whose 
occupation contains the substring "ie".

```
{
  users(
    orderBy: "name",
    offset: 0,
    limit: 2,
    occupation: "ie"
  ) {
    items {
      name
      age
      occupation
    }
    totalItemsCount
  }
}
```
This is the result:
```
{
  "data": {
    "users": {
      "items": [
        {
          "name": "Eddie Brock",
          "age": 20,
          "occupation": "Journalist, The Eddie Brock Report"
        },
        {
          "name": "Harold Osborn",
          "age": 19,
          "occupation": "President, Oscorp Industries"
        }
      ],
      "totalItemsCount": 3
    }
  }
}
```
Note that `totalItemsCount` is now 3 and not 4, because only 3 users in total 
match the filter.

