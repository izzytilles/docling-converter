import azure.functions as func
import logging
from docling.document_converter import DocumentConverter
import tempfile
from requests_toolbelt.multipart import decoder

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="docling_converter", methods=["POST"])
def docling_converter(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # get blob name from request
        if 'file' not in req.files:
            return func.HttpResponse(f"Please upload a file", status_code=400)

        user_file = req.Form.Files['file']
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            user_file.save(temp_file.name)

            # process the file to markdown
            converter = DocumentConverter()
            result = converter.convert(temp_file.name)
            markdown_text = result.document.export_to_markdown()

        return func.HttpResponse(
            markdown_text,
            mimetype="text/markdown"
        )

    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        return func.HttpResponse(f"Error processing file: {str(e)}", status_code=500)


# curl -X POST -F "file=@/Users/isabeltilles/Downloads/testfile.pdf" http://127.0.0.1:5001/docling_converter -o result.md