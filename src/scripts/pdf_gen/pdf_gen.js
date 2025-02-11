import { degrees, PDFDocument, rgb, StandardFonts } from 'pdf-lib';

export default async function generatePdf() {
  const firstTemplate = '/FSEA/FSEA_Template_First_Page.pdf';
  const secondTemplate = '/FSEA/FSEA_Template_Second_Page.pdf';

  fetch('/FSEA/FSEA_Template_First_Page.pdf')
  .then(res => res.arrayBuffer())
  .then(buffer => {
    const header = new TextDecoder().decode(buffer);
    console.log('File header:', header);
  })
  .catch(err => console.error(err));


  // Fetch and convert the first template to an ArrayBuffer
  const firstTemplateBytes = await fetch(firstTemplate).then(res => {
    if (!res.ok) throw new Error(`Failed to fetch PDF: ${res.statusText}`);
    return res.arrayBuffer();
  });

  // Fetch and convert the second template to an ArrayBuffer
  const secondTemplateBytes = await fetch(secondTemplate).then(res => res.arrayBuffer());

  // Now load the PDF from the correctly converted first template bytes
  const pdfDoc = await PDFDocument.load(firstTemplateBytes);
  const helveticaFont = await pdfDoc.embedFont(StandardFonts.Helvetica);

  const pages = pdfDoc.getPages();
  const firstPage = pages[0];
  const { width, height } = firstPage.getSize();
  firstPage.drawText('This text was added with JavaScript!', {
    x: 5,
    y: height / 2 + 300,
    size: 50,
    font: helveticaFont,
    color: rgb(0.95, 0.1, 0.1),
    rotate: degrees(-45),
  });

  const doc = await pdfDoc.saveAsBase64({ dataUri: true });
  return doc;
}
