# strawberry-offset-pagination-demo
A small demo project showing how to implement offset-based pagination using strawberry GraphQL

# About

This is a small demo python project, showing how to implement a Strawberry GraphQL 
server with **offset** pagination.

Refer to the [strawberry documentation for offset-based pagination](https://strawberry.rocks/docs/guides/pagination/offset-based) for more info.

## Why Offset Pagination?

Why **offset** pagination and not **cursor** pagination?

**Offset** pagination is simpler and less bug-prone compared to **cursor** pagination.

With **cursor** pagination, sort-by columns have to be unique (read 
[here](https://medium.com/@keren.duchan/set-up-a-strawberry-graphql-server-with-pagination-python-711c2f4652b2) 
for an explanation why). With **offset** pagination, they don't have to be.

These are the advantages of using **offset** pagination instead of **cursor** pagination:

- No risk of elusive bugs where entries are skipped because the column is not unique.
- No need to create synthetic unique db columns per non-unique sort-by column.
- The graphql interface is much cleaner and simpler.
- Gives the client (UI) exactly what it needs: the items in a page number of a given size, 
and how many pages there are in total.
- Easy to implement in SQL databases using *limit* and *offset*.

There is a performance hit, but IMO it is negligible in many use cases.
For small datasets containing up to several thousands or maybe even up to a million items or more,
and depending on other factors of your project, **offset** pagination may be the way to go.

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
