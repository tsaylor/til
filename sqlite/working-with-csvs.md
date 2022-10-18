# Working with CSV data in SQLite

SQLite makes it extremely easy to load CSV data and export it back out. 
Creating a table and loading a CSV file into it is just one command, and
exporting is just a couple. With SQLite's flexible type system it can 
stay out of the way unless you define the schema to enforce something.

## Import a CSV into SQLite
https://stackoverflow.com/questions/14947916/import-csv-to-sqlite
```sql
.import <filename.csv> <tablename> --csv      # creates table and loads data
```

## Review and modify the schema
```sql
.schema <tablename>                          -- prints the schema
  -- copy the printed schema
  -- modify types (i.e. use "integer" for ID columns to support joins)
drop table <tablename>;                      -- drop and recreate
create table <tablename> ...;
.import <filename.csv> <tablename> --csv     -- reimport the data
```

## Export a query to CSV
```sql
.mode csv
.output <filename.csv>
select * from <tablename>;
.output stdout
.mode table
```

