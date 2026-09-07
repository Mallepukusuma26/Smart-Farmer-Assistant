import os
import csv

class CSVReportGenerator:
    """CSV report generator for exporting financial and farm data."""

    @staticmethod
    def generate_csv(output_path, headers, rows):
        """Generate a CSV report locally."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        return output_path
