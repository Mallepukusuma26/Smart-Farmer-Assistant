import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Directories strictly EXCLUDED from production LOC count
EXCLUDED_DIRS = {
    'tests', 'docs', 'scripts', '.git', '__pycache__', 'node_modules',
    '.pytest_cache', 'venv', '.venv', 'instance', 'uploads', 'reports',
    'coverage', 'dist', 'build', 'htmlcov'
}

# Production source file extensions
PROD_EXTENSIONS = {
    '.py': 'Python Source',
    '.html': 'Jinja2/HTML Templates',
    '.css': 'CSS Stylesheets',
    '.js': 'JavaScript Logic',
    '.json': 'JSON Schemas/Configs',
    '.sql': 'SQL Scripts'
}

def count_production_loc():
    total_loc = 0
    total_files = 0
    loc_by_category = {}
    file_counts = {}
    loc_by_directory = {}

    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Exclude directories
        dirs[:] = [d for d in dirs if d.lower() not in EXCLUDED_DIRS and not d.startswith('.')]

        rel_dir = os.path.relpath(root, PROJECT_ROOT)
        if rel_dir == '.':
            rel_dir = 'root'

        dir_loc = 0

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in PROD_EXTENSIONS:
                filepath = os.path.join(root, file)
                category = PROD_EXTENSIONS[ext]
                
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        count = len(lines)
                        total_loc += count
                        dir_loc += count
                        total_files += 1

                        loc_by_category[category] = loc_by_category.get(category, 0) + count
                        file_counts[category] = file_counts.get(category, 0) + 1
                except Exception as e:
                    pass

        if dir_loc > 0:
            loc_by_directory[rel_dir] = dir_loc

    print("=" * 68)
    print("      SMART FARMER ASSISTANT — PRODUCTION LOC AUDIT REPORT      ")
    print("=" * 68)
    print(f" Root Directory : {PROJECT_ROOT}")
    print(f" Total Production Files : {total_files}")
    print("-" * 68)
    print(" LOC BY CATEGORY:")
    for cat, loc in sorted(loc_by_category.items(), key=lambda x: x[1], reverse=True):
        cnt = file_counts[cat]
        print(f"   - {cat:25s} : {loc:7,d} LOC ({cnt:3d} files)")
    print("-" * 68)
    print(" LOC BY DIRECTORY:")
    for d, loc in sorted(loc_by_directory.items(), key=lambda x: x[1], reverse=True):
        print(f"   - {d:25s} : {loc:7,d} LOC")
    print("=" * 68)
    print(f" TOTAL PRODUCTION LOC      : {total_loc:7,d} LOC")
    print(" REQUIRED TRAINPLEX LOC    :  50,000 LOC")
    print(f" TRAINPLEX STATUS          : {'PASS' if total_loc >= 50000 else 'FAIL'}")
    print("=" * 68)
    return total_loc

if __name__ == '__main__':
    loc = count_production_loc()
    if loc < 50000:
        sys.exit(1)
    sys.exit(0)
