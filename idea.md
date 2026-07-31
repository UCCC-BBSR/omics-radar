The idea: Create a web application that allows users to manage and publish a newsletter based on entries stored in a database. The application will be built using Python, Streamlit, and DuckDB, and will be hosted on GitHub Pages.

https://bbsr-uccc.github.io/omics-radar/

Aquiring new entries: Users will be able to add new entries to the database through a user-friendly interface. Each entry will have the following fields: title, summary, date, url, and tags. The application will also allow users to view existing entries within a specific date range, as well as edit or delete entries as needed.


dev stack:
Python as the base language
UV as the python package manager and virtual environment tool
streamlit for building interactive web applications
duckdb for database management and querying


architecture:
Local Streamlit admin app
        │
        ├── Add/edit/delete entries
        ├── Query DuckDB
        └── Generate static HTML
                    │
                    ▼
             docs/ or site/
        ├── index.html
        ├── reports/
        │   ├── 2026-07.html
        │   └── 2026-08.html
        └── assets/
                    │
                    ▼
              GitHub Pages



id
title
summary
publication_date
date_added
url
source
primary_category
tags
status
featured
created_at
updated_at


The user interface should look like:

The user interface should have these features / components:

- ability to add a new entry to the database
- ability to view existing entries in the database within a specific date range
- ability to edit or delete existing entries
- button to create or publish a report based on the entries in the database
- enties should have the following fields: title, summary, date, url, and tags

The report should look like a newsletter. There should be a title : "BBSR Omics Radar". And a subtitle: "Scanning the frontiers of bioinformatics, AI, and cancer research." Simple straight forward design with a clean layout. Next should be the report date window, typically for a monthly interval. Next there should be sections based on the tags of the entries, with each section containing the title, summary, and url of the entries that fall under that tag.

can this be published to github pages?
if so:
githuub pages should link to a master html page that contains the latest report with the ability to navigate to previous reports. The master html page should be updated automatically whenever a new report is generated and published.

workflow:

1. Clone or pull the repository.
2. Run `uv sync`.
3. Launch the local Streamlit admin application.
4. Add imported or manually curated entries.
5. Review, categorize, and select entries.
6. Create a report record and choose its date range.
7. Preview the generated newsletter.
8. Publish the report.
9. Regenerate the homepage, archive, and RSS feed.
10. Commit and push the generated files and database.
11. GitHub Pages automatically deploys the static site.
