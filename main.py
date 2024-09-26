import ollama


def generate_code():
    # response = ollama.chat(
    #     model="llava:13b",
    #     messages=[{
    #         "role": "user",
    #         "content": "Describe the design in the image",
    #         "images":["image.png"]
    #     }]
    # )

    # llava_response = response['message']['content']
    # print(llava_response)
    description = ' The image shows a login screen for an application or website. At the top, there is a placeholder for a logo or banner area, which is currently blank. Below this, centered on the screen, are three input fields: "Email," "Password," and a "Forgot password / Register" link. Each field has a placeholder text that reads "Enter username/email." To the right of these fields, there is a "Sign in" button with a green background, suggesting it is meant to initiate the login process. The color scheme is minimalistic, using a light beige or off-white for the background and dark gray for the input fields and sign-in button, which creates a clean and simple design that focuses on readability and user interaction. The layout suggests a straightforward user experience with clear separation between the email and password fields and an easily accessible "Forgot" link for users who need assistance.'
    response = ollama.chat(
        model="stable-code:3b",
        messages=[{
            "role": "user",
            "content": "Generate HTML/CSS code in one html file for this" + description,
        }]
    )

    code_response = response['message']['content']
    code_response = code_response.split('```')[1]
    
    start_index = code_response.find("<!DOCTYPE html>")
    if start_index != -1:
        code_response = code_response[start_index:]
    
    with open('index.html', 'w+') as f:
        f.write(code_response)
        
    print(code_response)


if __name__ == '__main__':
    generate_code()
