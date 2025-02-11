import { degrees, PDFDocument, rgb, StandardFonts } from 'pdf-lib';
import fontkit from'@pdf-lib/fontkit';
import emp from './testData';

async function addGrid(page, spacing = 10, font) {
  const { width, height } = page.getSize();

  // Draw vertical grid lines
  for (let x = 0; x <= width; x += spacing) {
    page.drawLine({
      start: { x, y: 0 },
      end: { x, y: height },
      color: rgb(0.8, 0.8, 0.8),
      thickness: 0.5,
    });
    // Optional: label the x-coordinate at the top
    page.drawText(`${x}`, {
      x: x + 2,
      y: height - 10,
      size: 5,
      font,
      color: rgb(0.5, 0.5, 0.5),
    });
  }

  // Draw horizontal grid lines
  for (let y = 0; y <= height; y += spacing) {
    page.drawLine({
      start: { x: 0, y },
      end: { x: width, y },
      color: rgb(0.8, 0.8, 0.8),
      thickness: 0.5,
    });
    // Optional: label the y-coordinate on the left
    page.drawText(`${y}`, {
      x: 2,
      y: y + 2,
      size: 5,
      font,
      color: rgb(0.5, 0.5, 0.5),
    });
  }
}

export default async function generatePdf() {
  const e = emp();
  const firstTemplate = './FSEA_Template_First_Page.pdf';
  // Fetch your PDF file
  const firstTemplateBytes = await fetch(firstTemplate).then(res => {
    if (!res.ok) throw new Error(`Failed to fetch PDF: ${res.statusText}`);
    return res.arrayBuffer();
  });

  

  // Load the PDF document and embed a font for drawing
  const pdfDoc = await PDFDocument.load(firstTemplateBytes);
  pdfDoc.registerFontkit(fontkit);
  
  // Fetch Font
  const titleFontPath = './fonts/Aquire/Aquire.ttf';
  const titleFontBytes = await fetch(titleFontPath).then(res => {
    if (!res.ok) throw new Error(`Failed to fetch font: ${res.statusText}`);
    return res.arrayBuffer();
  });

  const titleFont = await pdfDoc.embedFont(titleFontBytes);

  const pages = pdfDoc.getPages();
  const firstPage = pages[0];

  // Add the grid overlay (remove or comment out when you’re done debugging)
  await addGrid(firstPage, 30, titleFont);

  // Now add your text or any other content
  const title = 'Employee Report'
  const { width, height } = firstPage.getSize();
  firstPage.drawText(title, {
    x: ((width - titleFont.widthOfTextAtSize(title, 40)) / 2) + 50,
    y: height / 2 + 315,
    size: 40,
    font: titleFont,

  });

  const pdfBytes = await pdfDoc.saveAsBase64({dataUri: true});
  // Return the PDF bytes or do whatever you need with them
  return pdfBytes;
}
