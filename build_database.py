from datetime import timezone
import git
import markdown
import pathlib
import sqlite_utils

URL_TEMPLATE = "https://github.com/tsaylor/til/blob/main/{}"
root = pathlib.Path(__file__).parent.resolve()

def created_changed_times(repo_path, ref="main"):
    created_changed_times = {}
    repo = git.Repo(repo_path, odbt=git.GitDB)
    commits = reversed(list(repo.iter_commits(ref)))
    for commit in commits:
        dt = commit.committed_datetime
        affected_files = list(commit.stats.files.keys())
        for filepath in affected_files:
            if filepath not in created_changed_times:
                created_changed_times[filepath] = {
                    "created": dt.isoformat(),
                    "created_utc": dt.astimezone(timezone.utc).isoformat(),
                }
            created_changed_times[filepath].update(
                {
                    "updated": dt.isoformat(),
                    "updated_utc": dt.astimezone(timezone.utc).isoformat(),
                }
            )
    return created_changed_times


def build_database(repo_path):
    all_times = created_changed_times(repo_path)
    db = sqlite_utils.Database(repo_path / "tils.db")
    table = db.table("til", pk="path_slug")
    for filepath in root.glob("*/*.md"):
        slug = filepath.stem
        path = str(filepath.relative_to(root))
        path_slug = path.replace("/", "_")
        url = URL_TEMPLATE.format(path)
        with filepath.open() as fp:
            title = fp.readline().lstrip("#").strip()
            body = fp.read().strip()
        record = {
            "path_slug": path_slug,
            "slug": slug,
            "url": url,
            "topic": path.split("/")[0],
            "title": title,
            "body": body,
            "html": markdown.markdown(body)
        }
        record.update(all_times[path])
        with db.conn:
            table.upsert(record, alter=True)


if __name__ == "__main__":
    build_database(root)
