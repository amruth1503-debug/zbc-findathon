import imagehash
from PIL import Image

def calculate_phash(image_path):
    """Calculates the perceptual hash of an image."""
    try:
        img = Image.open(image_path)
        # pHash is robust against resizing and minor compression changes
        hash_val = imagehash.phash(img)
        return str(hash_val)
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def are_images_near_duplicates(hash1_str, hash2_str, threshold=5):
    """
    Compares two hashes using Hamming distance.
    A lower threshold means stricter matching (default 5 is great for near-duplicates).
    """
    h1 = imagehash.hex_to_hash(hash1_str)
    h2 = imagehash.hex_to_hash(hash2_str)
    
    # h1 - h2 returns the Hamming distance
    return (h1 - h2) <= threshold