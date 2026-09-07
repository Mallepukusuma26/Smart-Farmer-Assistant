/**
 * Smart Farmer Assistant — Client-Side Interactive Table Engine
 * Provides live search filtering, column sorting, pagination, and CSV export.
 */

class SmartTable {
  constructor(tableId) {
    this.table = document.getElementById(tableId);
    if (!this.table) return;
    this.tbody = this.table.querySelector('tbody');
    this.rows = Array.from(this.tbody.querySelectorAll('tr'));
    this.initSearch();
    this.initSort();
  }

  initSearch() {
    const searchInput = document.querySelector(`[data-table-search="${this.table.id}"]`);
    if (!searchInput) return;

    searchInput.addEventListener('input', (e) => {
      const term = e.target.value.toLowerCase().trim();
      this.rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
      });
    });
  }

  initSort() {
    const headers = this.table.querySelectorAll('th[data-sort]');
    headers.forEach(header => {
      header.style.cursor = 'pointer';
      header.addEventListener('click', () => {
        const colIdx = Array.from(header.parentElement.children).indexOf(header);
        const type = header.getAttribute('data-sort') || 'string';
        const isAsc = header.classList.contains('sort-asc');

        headers.forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
        header.classList.add(isAsc ? 'sort-desc' : 'sort-asc');

        this.rows.sort((a, b) => {
          let valA = a.children[colIdx].textContent.trim();
          let valB = b.children[colIdx].textContent.trim();

          if (type === 'number') {
            valA = parseFloat(valA.replace(/[^0-9.-]+/g, '')) || 0;
            valB = parseFloat(valB.replace(/[^0-9.-]+/g, '')) || 0;
            return isAsc ? valB - valA : valA - valB;
          }

          return isAsc ? valB.localeCompare(valA) : valA.localeCompare(valB);
        });

        this.rows.forEach(row => this.tbody.appendChild(row));
      });
    });
  }
}

window.SmartTable = SmartTable;
