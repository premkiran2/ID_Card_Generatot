import csv
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from PIL import Image
import io
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, filename='id_card_generation.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def resize_image(image_path, target_size=(1013, 638)):
    """Resize image to target_size and return the path to the resized image."""
    try:
        img = Image.open(image_path)
        if img.size != target_size:
            logging.info(f"Resizing template image from {img.size} to {target_size}")
            img = img.resize(target_size, Image.LANCZOS)
            resized_path = f"resized_{os.path.basename(image_path)}"
            img.save(resized_path, format='PNG', dpi=(300, 300))
            logging.info(f"Saved resized template: {resized_path}")
            return resized_path
        return image_path
    except Exception as e:
        logging.error(f"Error resizing image {image_path}: {e}")
        return None

def create_id_pdf(template_path, csv_path, photo_dir, output_pdf):
    # ID card dimensions (3.375 x 2.125 inches at 300 DPI)
    id_width = 3.375 * inch
    id_height = 2.125 * inch

    # Resize template if necessary
    template_path = resize_image(template_path)
    if not template_path:
        logging.error("Failed to load or resize template image. Aborting.")
        return

    # Create a PDF with ID card page size
    c = canvas.Canvas(output_pdf, pagesize=(id_width, id_height))
    skipped_rows = []

    # Read the CSV file
    try:
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            required_columns = {'name', 'title', 'photo_path'}
            if not required_columns.issubset(reader.fieldnames):
                logging.error(f"CSV missing required columns: {required_columns - set(reader.fieldnames)}")
                return
            logging.info(f"CSV Headers: {reader.fieldnames}")

            for i, row in enumerate(reader):
                if not all(row.get(key, '').strip() for key in required_columns):
                    logging.warning(f"Skipping row {i+2} due to missing or empty fields: {row}")
                    skipped_rows.append(row)
                    continue

                name = row['name'].strip()
                title = row['title'].strip()
                photo_path = os.path.join(photo_dir, row['photo_path'].strip())
                logging.info(f"Processing ID for {name} with photo: {photo_path}")

                # Draw the template at (0, 0)
                c.drawImage(template_path, 0, 0, width=id_width, height=id_height)

                # Draw the employee photo (1x1 inch at specified position)
                if os.path.exists(photo_path) and photo_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        img = Image.open(photo_path)
                        img = img.resize((300, 300), Image.LANCZOS)
                        img_byte_arr = io.BytesIO()
                        img.save(img_byte_arr, format='PNG')
                        img_byte_arr.seek(0)
                        # Use ImageReader to handle BytesIO
                        img_reader = ImageReader(img_byte_arr)
                        c.drawImage(img_reader, 0.37 * inch, 0.33 * inch, width=1 * inch, height=1 * inch)
                    except Exception as e:
                        logging.error(f"Error processing photo {photo_path}: {e}")
                        skipped_rows.append(row)
                else:
                    logging.warning(f"Photo not found or invalid format: {photo_path}")
                    skipped_rows.append(row)

                # Draw text
                try:
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(1.7 * inch, 1.05 * inch, name)
                    c.setFont("Helvetica", 8)
                    c.drawString(1.7 * inch, 0.6 * inch, title)
                except Exception as e:
                    logging.error(f"Error drawing text for {name}: {e}")
                    skipped_rows.append(row)

                # Start a new page
                c.showPage()

    except Exception as e:
        logging.error(f"Error reading CSV file {csv_path}: {e}")
        return

    # Save the PDF
    c.save()
    logging.info(f"PDF generated: {output_pdf}")
    if skipped_rows:
        logging.info(f"Skipped {len(skipped_rows)} rows due to errors: {skipped_rows}")

if __name__ == "__main__":
    template_path = "ute_id_template.png"
    csv_path = "employeesMetaData.csv"
    photo_dir = "passportPhotos"
    output_pdf = "employee_id_cards.pdf"
    create_id_pdf(template_path, csv_path, photo_dir, output_pdf)