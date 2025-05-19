import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import io

from models.model import model, DISEASE_LABELS

def generate_prediction_plot(img_bytes):
    # Load and preprocess
    img = Image.open(io.BytesIO(img_bytes)).convert('L').resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = img_array.reshape(1, 224, 224, 1)

    # Predict
    prediction = model.predict(img_array)[0]
    top_5 = sorted(zip(DISEASE_LABELS, prediction), key=lambda x: x[1], reverse=True)[:5]

    # Create plot
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(np.array(img), cmap='gray')
    ax.axis('off')
    ax.set_title("Top 5 Predicted Diseases", fontsize=12)

    for i, (label, prob) in enumerate(top_5):
        ax.text(
            5, 15 + i * 15,
            f"{label}: {prob * 100:.2f}%",
            color='red',
            fontsize=10,
            backgroundcolor='white'
        )

    # Return image as buffer
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf
