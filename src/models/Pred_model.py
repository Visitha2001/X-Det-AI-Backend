from tensorflow.keras.models import load_model

# Load the model once
model = load_model("classification_model2.h5")

# Disease labels
DISEASE_LABELS = [
    'Emphysema', 'Infiltration', 'Pleural_Thickening',
    'Pneumothorax', 'Cardiomegaly', 'No Finding', 'Atelectasis',
    'Edema', 'Effusion', 'Consolidation', 'Mass', 'Nodule',
    'Fibrosis', 'Pneumonia', 'Hernia'
]