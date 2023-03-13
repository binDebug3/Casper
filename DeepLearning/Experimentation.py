import json
import numpy as np
from PIL import Image, ImageDraw

# Load the JSON data
with open('Training_Data/damage/damage_coco/train/COCO_train_annos.json') as f:
    data = json.load(f)

# Get the image size
width, height = data['images'][0]['width'], data['images'][0]['height']

# Create an empty mask
mask = np.zeros((height, width), dtype=np.uint8)

# Draw polygons on the mask for each damaged area
for annotation in data['annotations']:
    segmentation = annotation['segmentation'][0]
    polygon = [(segmentation[i], segmentation[i+1]) for i in range(0, len(segmentation), 2)]
    ImageDraw.Draw(Image.fromarray(mask)).polygon(polygon, outline=1, fill=1)

# Save the mask as an image
Image.fromarray(mask).save('mask.png')