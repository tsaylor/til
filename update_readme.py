"Run this after build_database.py - it needs tils.db"
import pathlib
import sqlite_utils
import markdown
import sys
from string import Template


root = pathlib.Path(__file__).parent.resolve()

def index_by_topic(db):
    by_topic = {}
    for row in db["til"].rows_where(order_by="updated_utc desc"):
        by_topic.setdefault(row["topic"], []).append(row)
    index = []
    for topic, rows in by_topic.items():
        index.append("## {}\n".format(topic))
        for row in rows:
            context = row | dict(date=row["updated"].split("T")[0])
            index.append("* [{title}]({url}) - {date}".format(**context))
        index.append("")
    if index[-1] == "":
        index.pop()
    return index

# def index_by_updated(db):
#     index = []
#     for row in db["til"].rows_where(order_by="updated_utc"):
#         context = row | dict(date=row["created"].split("T")[0])
#         index.append("* [{topic} » {title}]({url}) - {date}".format(**context))
#     return index


if __name__ == "__main__":
    db = sqlite_utils.Database(root / "tils.db")
    readme_tpl = (root / "README.tpl.md").open().read()
    new_readme = readme_tpl.format(
        count=db["til"].count,
        index="\n".join(index_by_topic(db)).strip()
    )
    if "--rewrite" in sys.argv:
        readme = root / "README.md"
        readme.open("w").write(new_readme)
    else:
        print(new_readme)
