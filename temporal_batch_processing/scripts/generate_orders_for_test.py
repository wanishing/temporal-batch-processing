import os.path
import random
import sys
from datetime import datetime, timedelta
from typing import List, Tuple
import logging

import duckdb

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def random_timestamps(count: int) -> List[str]:
    base_date = datetime(2025, 1, 1)
    random_seconds = [random.randint(0, 30 * 24 * 60 * 60) for _ in range(count)]
    return [
        (base_date + timedelta(seconds=s)).strftime("%Y-%m-%d %H:%M:%S")
        for s in random_seconds
    ]


def get_destination_path():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(parent_dir, "tests", "resources")


def create_orders_table(con):
    logger.info("Creating orders table...")
    con.execute("DROP TABLE IF EXISTS orders")
    con.execute("""
    CREATE TABLE orders (
        order_id INTEGER,
        email VARCHAR,
        created_at TIMESTAMP
    )
    """)


def insert_orders(con, orders_data):
    if not isinstance(orders_data, list):
        orders_data = list(orders_data)
    con.executemany(
        """
    INSERT INTO orders (order_id, email, created_at)
    VALUES (?, ?, ?)
    """,
        orders_data,
    )


def export_to_parquet(con, query, filename):
    destination = get_destination_path()
    logger.info(f"Exporting to {filename}...")
    con.execute(f"""
    COPY ({query})
    TO '{destination}/{filename}' (FORMAT PARQUET, COMPRESSION 'ZSTD')
    """)
    logger.info(f"Export to {filename} completed")


def generate_static_orders():
    return [
        (1, "john.doe@email.com", "2025-01-28 09:15:00"),
        (2, "sara.smith@email.com", "2025-01-28 09:30:00"),
        (3, "mike.jones@email.com", "2025-01-28 10:00:00"),
        (4, "lisa.brown@email.com", "2025-01-28 10:45:00"),
        (5, "david.wilson@email.com", "2025-01-28 11:20:00"),
        (6, "emma.davis@email.com", "2025-01-28 12:00:00"),
        (7, "alex.taylor@email.com", "2025-01-28 13:15:00"),
        (8, "rachel.white@email.com", "2025-01-28 14:30:00"),
        (9, "chris.miller@email.com", "2025-01-28 15:45:00"),
        (10, "anna.garcia@email.com", "2025-01-28 16:00:00"),
        (11, "tom.anderson@email.com", "2025-01-28 16:30:00"),
        (12, "julia.martinez@email.com", "2025-01-28 17:00:00"),
        (13, "ryan.thompson@email.com", "2025-01-28 17:30:00"),
        (14, "sophie.lee@email.com", "2025-01-28 18:00:00"),
        (15, "peter.wong@email.com", "2025-01-28 18:30:00"),
        (16, "kevin.chen@email.com", "2025-01-28 19:00:00"),
        (17, "mary.johnson@email.com", "2025-01-28 19:30:00"),
        (18, "paul.adams@email.com", "2025-01-28 20:00:00"),
        (19, "laura.martin@email.com", "2025-01-28 20:30:00"),
        (20, "james.wilson@email.com", "2025-01-28 21:00:00"),
    ]


def generate_dynamic_orders(count: int, batch_size: int = 100000) -> List[Tuple]:
    total_batches = (count + batch_size - 1) // batch_size
    current_batch = 0
    batch = []

    logger.info(f"Starting to generate {count} orders in batches of {batch_size}")

    for i in range(1, count + 1):
        batch.append((i, f"email{i}@gmail.com", random_timestamp()))
        if len(batch) >= batch_size:
            current_batch += 1
            logger.info(
                f"Generated batch {current_batch}/{total_batches} ({(current_batch / total_batches) * 100:.1f}%)"
            )
            yield batch
            batch = []

    if batch:
        current_batch += 1
        logger.info(f"Generated final batch {current_batch}/{total_batches} (100%)")
        yield batch


def random_timestamp():
    random_seconds = random.randint(0, 30 * 24 * 60 * 60)  # 30 days in seconds
    base_date = datetime(2025, 1, 1)  # Start from January 1, 2025
    random_date = base_date + timedelta(seconds=random_seconds)
    return random_date.strftime("%Y-%m-%d %H:%M:%S")


def run():
    logger.info("Starting static orders generation")
    with duckdb.connect() as con:
        create_orders_table(con)
        orders_data = generate_static_orders()
        insert_orders(con, orders_data)

        # Export different segments
        export_to_parquet(
            con, "SELECT * FROM orders WHERE order_id <= 5", "orders_5.parquet"
        )
        export_to_parquet(
            con,
            "SELECT * FROM orders WHERE order_id > 5 AND order_id <= 12",
            "orders_7.parquet",
        )
        export_to_parquet(
            con,
            "SELECT * FROM orders WHERE order_id > 12 AND order_id <= 20",
            "orders_8.parquet",
        )
    logger.info("Static orders generation completed")


def run_many_orders():
    logger.info("Starting dynamic orders generation")
    with duckdb.connect() as con:
        # Enable faster inserts
        con.execute("PRAGMA threads=8")
        con.execute("PRAGMA memory_limit='4GB'")

        create_orders_table(con)
        count = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
        logger.info(f"Generating {count} orders...")

        # Process in batches
        total_inserted = 0
        for batch in generate_dynamic_orders(count):
            insert_orders(con, batch)
            total_inserted += len(batch)
            logger.info(
                f"Inserted {total_inserted}/{count} orders ({(total_inserted / count) * 100:.1f}%)"
            )

        export_to_parquet(con, "SELECT * FROM orders", "many_orders.parquet")

    logger.info("Dynamic orders generation completed")
