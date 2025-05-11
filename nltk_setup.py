import nltk

# Completely remove existing NLTK data folder (optional but safe)
import shutil
import os

nltk_path = os.path.join(os.path.expanduser('~'), 'nltk_data')
if os.path.exists(nltk_path):
    shutil.rmtree(nltk_path)

# Now download ONLY necessary resources freshly
nltk.download('punkt')
