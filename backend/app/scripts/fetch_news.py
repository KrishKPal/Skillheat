"""
Run all RSS fetches and recompute heat scores.

Manual run:
    python3 -m app.scripts.fetch_news

Schedule with cron for automatic refresh:
    */15 * * * * cd /path/to/backend && /path/to/venv/bin/python3 -m app.scripts.fetch_news
"""
import logging
import sys

from app.database import SessionLocal
from app.services.rss_fetcher import fetch_all
from app.services.heat_scorer import recompute_heat_scores


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


def main() -> int:
    db = SessionLocal()
    try:
        log.info("=== fetch_news start ===")
        stats = fetch_all(db)

        total = sum(n for n in stats.values() if n > 0)
        failed = [name for name, n in stats.items() if n < 0]

        log.info(f"Total inserted: {total}")
        if failed:
            log.warning(f"Failed sources ({len(failed)}): {failed}")

        log.info("Recomputing heat scores...")
        recompute_heat_scores(db)

        log.info("=== done ===")
        return 0 if not failed else 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
