
    // Get the URL of the PDF file (replace with your context variable)
    var pdfUrl = "{{ article.files.url }}";

    // Create a PDF.js viewer
    var pdfContainer = document.getElementById('pdf-viewer');
    var pdfViewer = pdfContainer.appendChild(document.createElement('div'));
    pdfViewer.className = 'pdf-viewer';

    // Load and display the PDF
    pdfjsLib.getDocument(pdfUrl).promise.then(function (pdf) {
        pdf.getPage(1).then(function (page) {
            var canvas = document.createElement('canvas');
            pdfContainer.appendChild(canvas);
            var context = canvas.getContext('2d');

            var viewport = page.getViewport({ scale: 1 });
            canvas.width = viewport.width;
            canvas.height = viewport.height;

            page.render({
                canvasContext: context,
                viewport: viewport,
            });
        });
    });

