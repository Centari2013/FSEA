from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pdfrw import PdfReader, PdfWriter, PageMerge
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

# Step 1: Register the font
# Replace 'path_to_Acquire_font.ttf' with the actual path to your Acquire font file
pdfmetrics.registerFont(TTFont('Roboto', 'Roboto Font/Roboto-Black.ttf'))
pdfmetrics.registerFont(TTFont('RobotoRegular', 'Roboto Font/Roboto-Regular.ttf'))

def create_text_overlay(output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter, bottomup=0)
   

    # Define the margins
    right_margin = inch * 0.5  # 0.5 inches from the right edge
    top_margin = inch * 0.75  # 0.75 inches from the top edge
    left_margin = inch * 0.5
    page_width, page_height = letter

    title_size = 20
    body_size = 12

    # Define your text
    title = "Early Universe Formation Investigation"
    body_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, \
        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut \
        aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate \
        velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non \
        proident, sunt in culpa qui officia deserunt mollit anim id est laborum." * 3
    
    body_style = ParagraphStyle('BodyStyle', fontName='RobotoRegular', fontSize=body_size, leading=22)

    body = Paragraph(body_text, body_style)

    # Calculate text width and position
    title_width = pdfmetrics.stringWidth(title, 'Roboto', title_size)

    # Calculate the X coordinates for right alignment
    title_x = page_width - right_margin - title_width
    title_y = top_margin  

    body_x = left_margin
    body_y = 200

    # Draw the strings
    c.setFont("Roboto", title_size)
    c.drawString(title_x, title_y, title)
    body.drawOn(c, left_margin, letter[1] - 2)

    c.save()

create_text_overlay("text_overlay.pdf")

def merge_pdfs(background_pdf, overlay_pdf, output_pdf):
    background = PdfReader(background_pdf)
    overlay = PdfReader(overlay_pdf)
    writer = PdfWriter()

    for bg_page, ol_page in zip(background.pages, overlay.pages):
        merger = PageMerge(bg_page)
        merger.add(ol_page)
        merger.render()
        writer.addpage(bg_page)

    writer.write(output_pdf)

# Example usage
merge_pdfs("FSEA_Template_First_Page.pdf", "text_overlay.pdf", "printable.pdf")
