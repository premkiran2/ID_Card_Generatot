import csv
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from PIL import Image
import io
import logging

# Set up logging to console only (no file)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def resize_image(image_path, target_size=(1013, 638)):
    """Resize image to target_size and return the path to the resized image."""
    try:
        img = Image.open(image_path)
        # Convert to RGB if necessary for better quality
        if img.mode != 'RGB':
            img = img.convert('RGB')
        if img.size != target_size:
            # Use high-quality resampling
            img = img.resize(target_size, Image.LANCZOS)
        # Always save with high DPI for print quality
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG', dpi=(300, 300), optimize=False)
        img_byte_arr.seek(0)
        return ImageReader(img_byte_arr)
    except Exception as e:
        return None

def create_id_pdf(template_path, csv_path, photo_dir, output_pdf):
    # ID card dimensions (3.375 x 2.125 inches at 300 DPI)
    id_width = 3.375 * inch
    id_height = 2.125 * inch

    # Resize template if necessary
    template_path = resize_image(template_path)
    if not template_path:
        return

    # Create a PDF with ID card page size and high quality settings
    c = canvas.Canvas(output_pdf, pagesize=(id_width, id_height))
    # Set high quality for images
    c.setPageCompression(0)  # Disable compression for better quality
    skipped_rows = []

    # Read the CSV file
    try:
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            required_columns = {'name', 'title', 'photo_path'}
            if not required_columns.issubset(reader.fieldnames):
                return

            for i, row in enumerate(reader):
                if not all(row.get(key, '').strip() for key in required_columns):
                    skipped_rows.append(row)
                    continue

                name = row['name'].strip()
                title = row['title'].strip()
                photo_path = os.path.join(photo_dir, row['photo_path'].strip())

                # Draw the template at (0, 0)
                c.drawImage(template_path, 0, 0, width=id_width, height=id_height)

                # Draw the employee photo (1x1 inch at specified position)
                if os.path.exists(photo_path) and photo_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        img = Image.open(photo_path)
                        # Convert to RGB for better quality
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        # Resize to higher resolution for better quality (600x600 for 1x1 inch at 300 DPI)
                        img = img.resize((600, 600), Image.LANCZOS)
                        img_byte_arr = io.BytesIO()
                        # Save with high quality settings
                        img.save(img_byte_arr, format='JPEG', quality=95, dpi=(300, 300))
                        img_byte_arr.seek(0)
                        # Use ImageReader to handle BytesIO
                        img_reader = ImageReader(img_byte_arr)
                        c.drawImage(img_reader, 1.86 * inch, 0.7 * inch, width=1.2 * inch, height=1.2 * inch)
                    except Exception as e:
                        skipped_rows.append(row)
                else:
                    skipped_rows.append(row)

                # Draw text
                try:
                    c.setFont("Helvetica-Bold", 11)
                    c.drawString(0.3 * inch, 0.25 * inch, name)
                    c.setFont("Helvetica", 9)
                    c.drawString(1.7 * inch, 0.25 * inch, title)
                except Exception as e:
                    skipped_rows.append(row)

                # Start a new page
                c.showPage()

    except Exception as e:
        return

    # Save the PDF
    c.save()
    if skipped_rows:
        pass

if __name__ == "__main__":
    template_path = "ute_id_template.png"
    csv_path = "employeesMetaData.csv"
    photo_dir = "passportPhotos"
    output_pdf = "employee_id_cards.pdf"
    create_id_pdf(template_path, csv_path, photo_dir, output_pdf)