import csv
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from PIL import Image

def create_id_pdf(template_path, csv_path, photo_dir, output_pdf):
    # ID card dimensions (3.375 x 2.125 inches at 300 DPI)
    id_width = 3.375 * inch
    id_height = 2.125 * inch

    # Create a PDF with letter page size
    c = canvas.Canvas(output_pdf, pagesize=letter)

    # Read the CSV file with comma delimiter
    try:
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            print("CSV Headers:", reader.fieldnames)
            for i, row in enumerate(reader):
                print("Row:", row) 
                # Verify required columns
                if not all(key in row for key in ['name', 'title', 'photo_path']):
                    print(f"Skipping row due to missing columns: {row}")
                    continue

                name = row['name'].strip()
                title = row['title'].strip()
                photo_path = os.path.join(photo_dir, row['photo_path'].strip())
                print(f"Processing photo for {name}: {photo_path}") 

                # Draw the template
                c.drawImage(template_path, 0, letter[1] - id_height, width=id_width, height=id_height)

                # Draw the employee photo (1x1 inch at specified position)
                if os.path.exists(photo_path):
                    try:
                        # Resize photo to 1x1 inch (300x300 pixels at 300 DPI)
                        img = Image.open(photo_path)
                        img = img.resize((300, 300), Image.LANCZOS)
                        # Use unique temp filename to avoid conflicts
                        temp_photo = f"temp_photo_{i}_{name.replace(' ', '_')}.png"
                        img.save(temp_photo)
                        print(f"Saved temp photo: {temp_photo}") 
                        c.drawImage(temp_photo, 0.37 * inch, letter[1] - id_height + 0.33 * inch, width=1 * inch, height=1 * inch)
                        if os.path.exists(temp_photo):
                            os.remove(temp_photo)
                            print(f"Deleted temp photo: {temp_photo}") 
                    except Exception as e:
                        print(f"Error processing photo {photo_path}: {e}")
                else:
                    print(f"Photo not found: {photo_path}")

                # Draw text
                c.setFont("Helvetica-Bold", 10)
                c.drawString(1.7 * inch, letter[1] - id_height + 1.05 * inch, name)
                c.setFont("Helvetica", 8)
                c.drawString(1.7 * inch, letter[1] - id_height + 0.6 * inch, title)

                # Start a new page for the next ID
                c.showPage()

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # Save the PDF
    c.save()
    print(f"PDF generated: {output_pdf}")

if __name__ == "__main__":
    template_path = "ute_id_template.png"
    csv_path = "employees.csv"
    photo_dir = "photos"
    output_pdf = "employee_ids.pdf"
    create_id_pdf(template_path, csv_path, photo_dir, output_pdf)