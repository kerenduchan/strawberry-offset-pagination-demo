# strawberry-offset-pagination-demo
A small demo project showing how to implement offset-based pagination using strawberry GraphQL

# About

This is a small demo python project, showing how to implement a Strawberry GraphQL 
server with **offset** pagination.

Refer to the [strawberry documentation for offset-based pagination](https://strawberry.rocks/docs/guides/pagination/offset-based) for more info.

# Quickstart

## Install

```
pip install -r requirements.txt
```

## Run the Strawberry GraphQL server
```
strawberry server schema
```
You will get the following message:
```
Running strawberry on http://0.0.0.0:8000/graphql 🍓
```

## Query the server
Go to [http://0.0.0.0:8000/graphql](http://0.0.0.0:8000/graphql) to open **GraphiQL**,
and run the following query to get the first page of books, ordered by title,
three books per page:

```
{
  books(orderBy: "title", pageNumber: 1, pageSize: 3) {
    pagesCount
    items {
      id
      title
    }
  }
}

```
The result should look like this: 
```
{
  "data": {
    "books": {
      "pagesCount": 4,
      "items": [
        {
          "id": "4",
          "title": "1984"
        },
        {
          "id": "5",
          "title": "Anne of Avonlea"
        },
        {
          "id": "8",
          "title": "Anne of Green Gables"
        }
      ]
    }
  }
}
```

The result contains:
- `pagesCount` - The total number of pages
- `items` - a list of the books in this page

Get the next page of books by running the same query, after incrementing `pageNumber`.

Repeat until `pageNumber` is equal to `pagesCount`.
