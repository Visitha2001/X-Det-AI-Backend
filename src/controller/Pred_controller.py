import io
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import uuid
import os
from models.Pred_model import model, DISEASE_LABELS

TEMP_DIR = "tmp_predictions"
os.makedirs(TEMP_DIR, exist_ok=True)

def generate_prediction_plot(img_bytes):
    # (Same preprocessing and prediction as before)

    img = Image.open(io.BytesIO(img_bytes)).convert('L').resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = img_array.reshape(1, 224, 224, 1)
    prediction = model.predict(img_array)[0]
    top_5 = sorted(zip(DISEASE_LABELS, prediction), key=lambda x: x[1], reverse=True)[:5]

    # Create plot
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(np.array(img), cmap='gray')
    ax.axis('off')
    ax.set_title("Top 5 Predicted Diseases", fontsize=12)
    for i, (label, prob) in enumerate(top_5):
        ax.text(5, 15 + i * 15, f"{label}: {prob * 100:.2f}%", color='red', fontsize=10, backgroundcolor='white')

    # Save image to a unique file
    image_id = str(uuid.uuid4())
    image_path = os.path.join(TEMP_DIR, f"{image_id}.png")
    plt.tight_layout()
    plt.savefig(image_path, format='png')
    plt.close(fig)

    # Prepare top 5 list as dict
    top_5_list = [{"disease": label, "probability": float(prob)} for label, prob in top_5]

    return image_id, top_5_list