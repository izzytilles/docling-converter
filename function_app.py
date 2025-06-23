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
        content_type = req.headers.get('Content-Type')
        if not content_type or 'multipart/form-data' not in content_type:
            return func.HttpResponse("Invalid content-type, expecting multipart/form-data", status_code=400)

        body = req.get_body()
        multipart_data = decoder.MultipartDecoder(body, content_type)

        file_part = None
        for part in multipart_data.parts:
            if b'name="file"' in part.headers.get(b'Content-Disposition', b''):
                file_part = part
                break

        if not file_part:
            return func.HttpResponse("No file uploaded", status_code=400)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_part.content)
            temp_file.flush()

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


# example curl command:
#   curl -X POST -F "file=@/Users/isabeltilles/Downloads/testfile.pdf" http://localhost:7071/api/docling_converter