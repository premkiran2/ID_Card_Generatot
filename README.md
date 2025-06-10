# Employee ID Generator

This project generates a single PDF file containing employee ID cards, with one ID per page, using a pre-defined ID template image, a CSV file with employee data, and a directory of employee photos. Each ID card is sized to standard dimensions (3.375 x 2.125 inches), with the employee name at the bottom-left and a photo at the top-left.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)

## Features
- Generates a PDF with one employee ID per page.
- Uses a template image (`ute_id_template.png`) for consistent ID design.
- Reads employee data (name, title, photo path) from a CSV file.
- Places employee photos and text (name and title) on each ID.
- Name is positioned at the bottom-left with a font size of 10 points.
- Title is positioned at (1.7 inches x, 0.6 inches from bottom) with an 8-point font.
- Photo is positioned at (0.37 inches x, 0.33 inches from top) with a 1x1 inch size.

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
```

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/employee_id_generator.git
   cd employee_id_generator
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare Input Files**
   - Place `ute_id_template.png` in `src/`.
   - Place employee photos (e.g., `employee1.jpg`, `employee2.jpg`) in `src/photos/`.
   - Create or update `src/employees.csv` with the following format:
   ```csv
   name,title,photo_path
   John,Software Engineer,employee1.jpg
   Siri,Project Manager,employee2.jpg
   Alice,Software Engineer,employee3.jpg
   Mary,Project Manager,employee4.jpg
   ```

## Usage
1. **Navigate to the `src/` directory:**
    ```bash
    cd src
    ```

2. **Run the script:**
    ```bash
    python main.py
    ```

3. **Check the output:**
    - A file named `employee_ids.pdf` will be generated in `src/`.
    - Each page contains one ID card with the template, employee photo, name, and title.
