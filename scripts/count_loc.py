import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

EXTENSIONS = {
    '.py': 'Python Source',
    '.html': 'HTML Templates',
    '.css': 'CSS Stylesheets',
    '.js': 'JavaScript',
    '.md': 'Documentation',
    '.ini': 'Configuration',
    '.txt': 'Configuration/Reqs'
}

def count_lines():
    total_loc = 0
    file_counts = {}
    loc_by_type = {}

    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Exclude virtualenvs, git, cache, and instance folders
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.pytest_cache', 'venv', 'instance', 'brain', 'uploads', 'reports']]
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in EXTENSIONS:
                category = EXTENSIONS[ext]
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        count = len(lines)
                        total_loc += count
                        loc_by_type[category] = loc_by_type.get(category, 0) + count
                        file_counts[category] = file_counts.get(category, 0) + 1
                except Exception as e:
                    pass

    print("=" * 60)
    print("      SMART FARMER ASSISTANT — LINES OF CODE (LOC) REPORT      ")
    print("=" * 60)
    for cat, loc in sorted(loc_by_type.items(), key=lambda x: x[1], reverse=True):
        files_cnt = file_counts[cat]
        print(f" {cat:25s} : {loc:7,d} LOC ({files_cnt:3d} files)")
    print("-" * 60)
    print(f" TOTAL CODEBASE LOC         : {total_loc:7,d} LOC")
    print("=" * 60)
    return total_loc

if __name__ == '__main__':
    count_lines()
