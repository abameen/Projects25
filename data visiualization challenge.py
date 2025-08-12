import csv 
import matplotlib.pyplot as plt
from typing import List, Optional, Union, Dict
from datetime import datetime
import numpy as np



def load_csv(filepath: str) -> List[List[str]]:
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        return [row for row in reader]

def standardize_row_length(data: List[List[str]], expected_length: int) -> List[List[Optional[str]]]:
    standardized = []
    for row in data:
        # Pad with None if shorter, truncate if longer
        if len(row) < expected_length:
            row += [None] * (expected_length - len(row))
        elif len(row) > expected_length:
            row = row[:expected_length]
        standardized.append(row)
    return standardized

def replace_invalid_values(data: List[List[Optional[str]]], invalid_values: set[str]) -> List[List[Optional[str]]]:
    cleaned = []
    for row in data:
        new_row = []
        for val in row:
            if val is None or val.strip() == '' or val in invalid_values:
                new_row.append(None)
            else:
                new_row.append(val)
        cleaned.append(new_row)
    return cleaned

def convert_column_types(data: List[List[Optional[str]]], 
                         column_types: dict[int, type]) -> List[List[Optional[Union[int, float, str, datetime]]]]:
    converted = []
    header = data[0]
    converted.append(header)  # Keep header as is

    for row in data[1:]:
        new_row = []
        for i, val in enumerate(row):
            if val is None:
                new_row.append(None)
                continue
            # Convert based on column type
            desired_type = column_types.get(i, str)
            try:
                if desired_type == int:
                    new_row.append(int(float(val)))  # Handles if val is '30.0' etc.
                elif desired_type == float:
                    new_row.append(float(val))
                elif desired_type == datetime:
                    # Try parsing common date formats
                    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                        try:
                            new_row.append(datetime.strptime(val, fmt))
                            break
                        except ValueError:
                            continue
                    else:
                        new_row.append(None)  # Couldn’t parse date
                else:
                    new_row.append(val)
            except Exception:
                new_row.append(None)
        converted.append(new_row)
    return converted

def clean_csv_file(filepath: str, invalid_values: set[str], column_types: dict[int, type]) -> List[List[Optional[Union[int, float, str, datetime]]]]:
    data = load_csv(filepath)
    if not data:
        return []
    header_length = len(data[0])
    data = standardize_row_length(data, header_length)
    data = replace_invalid_values(data, invalid_values)
    data = convert_column_types(data, column_types)
    return data

def make_bar_chart(data: List[List[Optional[Union[int, float, str]]]], 
                x_col: int, y_col: int, title: str, xlabel: str, ylabel: str) -> None:
    x = [row[x_col] for row in data[1:] if row[x_col] is not None]
    y = [row[y_col] for row in data[1:] if row[y_col] is not None]

    plt.figure(figsize=(10, 6))
    plt.bar(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
def make_scatter_plot(data: List[List[Optional[Union[int, float, str]]]], 
                      x_col: int, y_col: int, 
                      title: str, xlabel: str, ylabel: str) -> None:
    x = []
    y = []
    for row in data[1:]:
        x_val = row[x_col]
        y_val = row[y_col]
        if x_val is not None and y_val is not None:
            x.append(x_val)
            y.append(y_val)

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()
    

def main():
    # Define invalid values and column types
    invalid_vals = {"unknown", "NaN", ""}
    col_types = {
        0: int,        # ID
        1: str,        # Name
        2: int,        # Age
        3: str,        # City
        4: str,        # Department
        5: float,      # Salary
        6: datetime    # Joining Date
    }

    # Clean the CSV data
    cleaned_data = clean_csv_file("messy_data.csv", invalid_vals, col_types)

    # 1. Bar Chart: Average Salary by Department
    # We need to aggregate average salary per department first
    dept_salary = {}
    dept_counts = {}
    for row in cleaned_data[1:]:
        dept = row[4]
        salary = row[5]
        if dept is not None and salary is not None:
            dept_salary[dept] = dept_salary.get(dept, 0) + salary
            dept_counts[dept] = dept_counts.get(dept, 0) + 1

    avg_salary_per_dept = [(dept, dept_salary[dept] / dept_counts[dept]) for dept in dept_salary]

    # Prepare data format for bar chart (replacing cleaned_data subset)
    bar_data = [cleaned_data[0]] + [[dept, None, None, None, dept, avg_salary, None] for dept, avg_salary in avg_salary_per_dept]

    make_bar_chart(bar_data, x_col=4, y_col=5, title="Average Salary by Department", xlabel="Department", ylabel="Average Salary")

    # 2. Scatter Plot: Age vs Salary
    # Use cleaned_data directly
    make_scatter_plot(cleaned_data, x_col=2, y_col=5, title="Age vs Salary", xlabel="Age", ylabel="Salary")


if __name__ == "__main__":
    main()





    




