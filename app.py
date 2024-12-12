from flask import Flask, render_template, request, redirect, url_for
from helper import preprocessing, vectorizer, get_prediction
from logger import logging

app = Flask(__name__)

logging.info("Flask server started")

# Initialize global state
data = {
    "images": [
        {"id": 1, "path": "products/metro.jpg", "name": "Metro Last Light", "reviews": [], "positive": 0, "negative": 0, },
        {"id": 2, "path": "products/Cyberpunk2077.jpg", "name": "Cyberpunk 2077", "reviews": [], "positive": 0, "negative": 0},
        {"id": 3, "path": "products/Rage2.jpg", "name": "Rage 2", "reviews": [], "positive": 0, "negative": 0},
        {"id": 4, "path": "products/tokyo.png", "name": "Ghostwire Tokyo", "reviews": [], "positive": 0, "negative": 0},
        {"id": 5, "path": "products/fallout.jpg", "name": "Fallout 4", "reviews": [], "positive": 0, "negative": 0},
        {"id": 6, "path": "products/borderland.jpg", "name": "Borderlands 3", "reviews": [], "positive": 0, "negative": 0},
        {"id": 7, "path": "products/riderr.jpg", "name": "Riders Republic", "reviews": [], "positive": 0, "negative": 0},
        {"id": 8, "path": "products/hell.png", "name": "Helldivers II", "reviews": [], "positive": 0, "negative": 0},
        {"id": 9, "path": "products/payday3.jpg", "name": "Payday 3", "reviews": [], "positive": 0, "negative": 0},
        {"id": 10, "path": "products/Left4Dead2.jpg", "name": "Left 4 Dead 2", "reviews": [], "positive": 0, "negative": 0},
        {"id": 11, "path": "products/Thefinal.jpg", "name": "The Finals", "reviews": [], "positive": 0, "negative": 0},
        {"id": 12, "path": "products/des.jpg", "name": "Destiny 2", "reviews": [], "positive": 0, "negative": 0},
    ]
}

@app.route("/")
def index():
    """Render the home page with the image gallery."""
    logging.info("========== Open home page ===========")
    return render_template("index.html", images=data["images"])

@app.route("/image/<int:image_id>")
def image_reviews(image_id):
    """Render reviews for a specific image."""
    image = next((img for img in data["images"] if img["id"] == image_id), None)
    if not image:
        logging.warning(f"Image with ID {image_id} not found.")
        return redirect(url_for("index"))
    
    logging.info(f"Viewing reviews for Image ID: {image_id}")
    return render_template("image_reviews.html", image=image)

@app.route("/image/<int:image_id>", methods=["POST"])
def add_review(image_id):
    """Handle review submissions for a specific image."""
    image = next((img for img in data["images"] if img["id"] == image_id), None)
    if not image:
        logging.warning(f"Image with ID {image_id} not found.")
        return redirect(url_for("index"))

    text = request.form.get("text", "").strip()
    if not text:
        logging.warning("Empty review submitted.")
        return redirect(url_for("image_reviews", image_id=image_id))
    
    logging.info(f"Received review for Image {image_id}: {text}")

    # Preprocess and analyze the input text
    try:
        preprocessed_text = preprocessing(text)
        vectorized_text = vectorizer(preprocessed_text)
        prediction = get_prediction(vectorized_text)
        logging.info(f"Prediction for Image {image_id}: {prediction}")

        # Update counts based on the prediction
        if prediction == "negative":
            image["negative"] += 1
        else:
            image["positive"] += 1

        # Add the review to the image's review list
        image["reviews"].insert(0, text)
    except Exception as e:
        logging.error(f"Error during sentiment analysis: {e}")
    
    return redirect(url_for("image_reviews", image_id=image_id))

if __name__ == "__main__":
    app.run(debug=True)
