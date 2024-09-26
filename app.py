from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import uuid
import ollama

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_unique_filename(extension):
    return str(uuid.uuid4()) + '.' + extension

def generate_code(image_path):
    response = ollama.chat(
        model="llava:13b",
        messages=[{
            "role": "user",
            "content": "Describe the design in the image",
            "images":[f"{image_path}"]
        }]
    )

    llava_response = response['message']['content']
    print(llava_response)
    
    response = ollama.chat(
        model="stable-code:3b",
        messages=[{
            "role": "user",
            "content": f"Generate HTML/CSS code in one html file for this: {llava_response}",
        }]
    )

    code_response = response['message']['content']
    code_response = code_response.split('```')[1]
    
    start_index = code_response.find("<!DOCTYPE html>")
    if start_index != -1:
        code_response = code_response[start_index:]
    
    with open('index.html', 'w+') as f:
        f.write(code_response)
        
    # print(code_response)
    return code_response

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    contents = await file.read()
    extension = filename.split('.')[-1] # image.png -> ['image', 'png'] -> 'png'
    new_filename = generate_unique_filename(extension)
    with open(f"{new_filename}", "wb") as buffer:
        buffer.write(contents)
    
    print("Convering to Code")
    
    generated_code = generate_code(new_filename)
    print("Task Complete!!")
    
    return {"status": "Code Generated", "code": generated_code}