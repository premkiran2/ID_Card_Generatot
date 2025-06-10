# Employee ID Generator

This project generates a single PDF file containing employee ID cards, with one ID per page, using a pre-defined ID template image, a CSV file with employee data, and a directory of employee photos. Each ID card is sized to standard dimensions (3.375 x 2.125 inches), with the employee name at the bottom-left and a photo at the top-left.

## Table of Contents
- [Features](#features)
- [File Structure](#file-structure)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Input File Details](#input-file-details)
- [Troubleshooting](#troubleshooting)
- [Notes](#notes)

## Features
- Generates a PDF with one employee ID per page.
- Uses a template image (`ute_id_template.png`) for consistent ID design.
- Reads employee data (name, title, photo path) from a CSV file.
- Places employee photos and text (name and title) on each ID.
- Name is positioned at the bottom-left with a font size of 10 points.
- Title is positioned at (1.7 inches x, 0.6 inches from bottom) with an 8-point font.
- Photo is positioned at (0.37 inches x, 0.33 inches from top) with a 1x1 inch size.

## File Structure
employee_id_generator/
├── src/
│   ├── main.py              # Python script to generate the PDF
│   ├── ute_id_template.png  # ID template image
│   ├── employees.csv        # CSV file with employee data
│   └── photos/              # Directory containing employee photos
│       ├── employee1.jpg
│       ├── employee2.jpg
│       └── ...
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
└── .gitignore               # Git ignore file

## Requirements
- **Python**: Version 3.8 or higher
- **Libraries**:
  - `reportlab`: For PDF generation
  - `pillow`: For image processing
- **Input Files**:
  - `ute_id_template.png`: ID template image (1013x638 pixels for 3.375x2.125 inches at 300 DPI)
  - `employees.csv`: CSV file with columns `name`, `title`, `photo_path`
  - Employee photos in `src/photos/` (e.g., `employee1.jpg`, `employee2.jpg`)

Install dependencies via:
```bash
pip install -r requirements.txt
