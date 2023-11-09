import telebot
from roboflow import Roboflow
bot_token = "bot_id"
bot = telebot.TeleBot(bot_token)
def process_image_prediction(message, image_file):
    try:
       
        rf = Roboflow(api_key="71mVaRR1hHsiQBJot1Oh")
        project = rf.workspace().project("glaucoma-0zetc")
        model = project.version(1).model
        pred = model.predict(image_file, confidence=40, overlap=30).json()

        # Extract the class value from the prediction
        class_value = pred['predictions'][0]['class']
        confidence = pred['predictions'][0]['confidence']*100

        # Send the prediction result back to the user
        bot.send_message(message.chat.id, f"Prediction Result: {class_value}\nConfidence : {confidence}")
        if class_value=='glaucoma':
            bot.reply_to(message,f"Glaucoma is an eye condition that damages the optic nerve, leading to vision loss. Symptoms may include gradual peripheral vision loss (open-angle glaucoma) or sudden eye pain and blurred vision (acute angle-closure glaucoma). Early detection is crucial. Treatments include medications, laser therapy, and surgery to lower eye pressure. Regular eye exams and lifestyle modifications are essential for managing the disease and preventing vision loss. Seek immediate medical attention for symptoms to prevent irreversible damage." )
        else :
            bot.reply_to(message,f"It is normal condition")

    except Exception as e:
        # Handle exceptions and report the error back to the user
        bot.reply_to(message, f"Error processing the image: {e}")

@bot.message_handler(content_types=["photo"])
def handle_image(message):
    try:
        # Get the file_id of the photo sent by the user
        bot.reply_to(message,"Welcome to Glaucoma detection !")
        file_id = message.photo[-1].file_id

        # Download the photo using the file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Save the photo with a unique name
        image_file_name = f"{file_id}.jpg"
        with open(image_file_name, "wb") as f:
            f.write(downloaded_file)

        # Process the image prediction
        process_image_prediction(message, image_file_name)

        # Delete the saved image to free up disk space (optional)
        import os
        os.remove(image_file_name)

    except Exception as e:
        # Handle exceptions (e.g., invalid image format)
        bot.reply_to(message, "Error processing the image. Please try again.")

if __name__ == "__main__":
    bot.polling()
