from fastapi import FastAPI, Request, HTTPException, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import TranslationRequest, TranslationResponse
from ocr import extract_text
from translation import translate_text
from image_completion import complete_image, convert_to_response_format

app = FastAPI()

# Mount static files directory for frontend assets like CSS, JS
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend")

@app.get("/")
def serve_frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/translate_image/", response_model=TranslationResponse)
async def translate_image(target_language: str = Form(...), file: UploadFile = File(...)):
    try:
        image_content = await file.read()

        # Extract text
        extracted_text, bounding_info = extract_text(image_content)

        # Translate text
        translated_text = translate_text(extracted_text, target_language=target_language)

        # Complete image
        result_image = complete_image(image_content, translated_text, bounding_info)

        # Convert final image to desired format for response
        response_image = convert_to_response_format(result_image)

        return TranslationResponse(result_image=response_image)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

