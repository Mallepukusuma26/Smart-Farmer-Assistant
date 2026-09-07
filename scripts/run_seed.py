import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.seeds.seed import seed_database

if __name__ == '__main__':
    seed_database()
