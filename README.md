# PsychResearch Survey Data Processing Script

## Overview

This Python script simplifies the handling of CSV files derived from survey responses, aiming to produce tables that are easily interpretable by both humans and machines. Tailored for researchers, the script operates on a directory containing multiple CSV files, a common format for survey data storage.

## Features

- **File Merging**: Combines content from all CSV files into a consolidated excel format, facilitating comprehensive analysis.

- **Data Extraction**: Utilizes regular expressions to extract essential information from filenames and tables.

- **Data Cleaning**: Addresses data cleanliness concerns, excluding unnecessary rows and submissions based on specified conditions.

- **Numeric Standardization**: Converts text-based responses to numeric values for consistent interpretation and analysis.

- **Table Organization**: Organizes data into tables, considering both human readability and machine processing.

## Usage

1. **Folder Setup**: Ensure that the CSV files are organized in a directory.

2. **Run Script**: Execute the script, providing the path to the directory containing the CSV files.

3. **Review Output**: Analyze the resulting tables, optimized for human understanding and machine processing.

## Requirements

- Python 3.x
- Pandas

## Getting Started

Clone the repository and run the script using the following commands:

```bash
git clone https://github.com/j-jacboson/PsychResearch.git
cd PsychResearch
python3 formatter.py /path/to/your/csv/files
```

## Contributions

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

---

*Note: Replace placeholder `/path/to/your/csv/files` with the actual value.*