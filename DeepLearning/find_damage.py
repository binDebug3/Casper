import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, utils, datasets

from PIL import Image
import os
import numpy as np

class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels, up_sample=False):
        super(ConvBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, (3, 3), padding=(1, 1))
        self.conv2 = nn.Conv2d(out_channels, out_channels, (3, 3), padding=(1, 1))
        self.up_sample = up_sample
        if up_sample:
            # Up sample with up-conv 2x2, doubling along each dimension
            self.up = nn.ConvTranspose2d(out_channels, out_channels // 2, 2, stride=2)
        # We do not want to down sample in the block, since we need the non-down-sampled output for skip connections

    def forward(self, input):
        x = F.relu(self.conv1(input))
        x = F.relu(self.conv2(x))
        if self.up_sample:
            x = self.up(x)
        return x


class DamageDetection(nn.Module):
    def __init__(self):
        super(DamageDetection, self).__init__()
        # Downsample convolution blocks
        self.dblock1 = ConvBlock(3, 32)
        self.dblock2 = ConvBlock(32, 64)
        self.dblock3 = ConvBlock(64, 128)
        self.dblock4 = ConvBlock(128, 256)
        # Upsample convolution blocks
        self.ublock1 = ConvBlock(256, 512, True)
        # The next 4 blocks have doubled input channels due to concatenation of skip connections
        self.ublock2 = ConvBlock(512, 256, True)
        self.ublock3 = ConvBlock(256, 128, True)
        self.ublock4 = ConvBlock(128, 64, True)
        # Output "block"
        self.convf1 = nn.Conv2d(64, 32, (3, 3), padding=(1, 1))
        self.convf2 = nn.Conv2d(32, 32, (3, 3), padding=(1, 1))
        self.convf3 = nn.Conv2d(32, 2, (1, 1), padding=(0, 0))

        self.down = nn.MaxPool2d(2)

    def forward(self, input):
        # Save the last feature maps on each level
        l1 = self.dblock1(input)
        l2 = self.dblock2(self.down(l1))
        l3 = self.dblock3(self.down(l2))
        l4 = self.dblock4(self.down(l3))
        # Concatenate l1 - l4 on inputs across the U in reverse order, matching sizes
        u = self.ublock1(self.down(l4))
        u = self.ublock2(torch.cat((l4, u), dim=1))
        u = self.ublock3(torch.cat((l3, u), dim=1))
        u = self.ublock4(torch.cat((l2, u), dim=1))
        out = F.relu(self.convf1(torch.cat((l1, u), dim=1)))
        out = F.relu(self.convf2(out))
        out = self.convf3(out)
        return out


def resize(file_path):
    # open the image and resize it to a smaller size
    img = Image.open(file_path)

    # Get the size of the original image
    width, height = img.size

    # Find the smaller dimension and calculate the new dimensions
    new_size = min(width, height) * 2 // 3
    left = (width - new_size) // 2
    top = (height - new_size) // 2
    right = left + new_size
    bottom = top + new_size

    # Crop the image
    img = img.crop((left, top, right, bottom))
    img = img.resize((256, 256), resample=Image.LANCZOS)

    # save the compressed image in the same folder with a new name
    dir_path, file_name = os.path.split(file_path)
    base_name, ext = os.path.splitext(file_name)
    new_file_address = os.path.join(dir_path, base_name + "_cropped" + ext)
    img.save(new_file_address, quality=70)

    return new_file_address


def predict(image_path):
    """
    Predicts the damage to a car
    :param image_path: (string or list of strings) the path to the image or a list of paths to images
    :return:
        damaged: (bool or list of bools) True if the car is damaged, False otherwise
        confidence: (float or list of floats) the confidence of the prediction as a percentage
        outputs: (array of floats or list) the raw output of the model as a numpy array of 0s and 1s
    """

    # initialize the model
    model = DamageDetection()
    weights = r'C:\Users\dalli\PycharmProjects\CarMarket\Casper\DeepLearning\car_damage_classifier.pt'
    model.load_state_dict(torch.load(weights, map_location=torch.device('cpu')))
    # Set the model to evaluation mode
    model.eval()

    # Check if the input is a list or a single image
    alt_return = False
    if isinstance(image_path, str):
        image_path = [image_path]
        alt_return = True

    # Initialize the return  lists
    damaged = []
    confidence = []
    outputs = []


    # Loop through the images
    for i, path in enumerate(image_path):
        # Load the image
        cropped_path = resize(path)
        image = Image.open(cropped_path)

        # Transform the image
        transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
        ])
        image = transform(image)

        # Run the model
        output = model.forward(image.unsqueeze(0)).squeeze(0).argmax(0).cpu().detach().numpy()


        # Calculate the confidence and update return lists
        dmg = np.average(output)

        if dmg <= 0.5:
            damaged.append(False)
            confidence.append(100 - round(dmg, 3) * 100)
        else:
            output[0][0] = 0
            damaged.append(True)
            confidence.append(round(dmg, 3) * 100)

        outputs.append(output)

    # Return the correct format
    if alt_return:
        return damaged[0], confidence[0], outputs[0]
    return damaged, confidence, outputs


# path = r"C:\Users\dalli\PycharmProjects\CarMarket\Casper\Used_Car_Undamaged\train\0\2014_Honda_Civic_EX.png"
# damaged, confidence, output = find_damage.predict(path)
# if damaged:
#     result = "damaged"
# else:
#     result = "undamaged"
# print(f"I'm {confidence}% sure that car is {result}.")
# display = input("Would you like to see what I found? (y/n)")
#
# if display == "y":
#     # fig, axs = plt.subplots(1, 2)
#     plt.imshow(output, cmap='gray')
#     if damaged:
#         title = f"Not damaged. Conf: {confidence}%"
#     else:
#         title = f"Damaged. Conf: {confidence}%"
#     plt.title(title)
#     plt.show()
#
#     # # Display the classification image in the first subplot
#     # axs[0].imshow(output, cmap="gray")
#     # axs[0].set_title(title)
#     #
#     # # Display the original image in the second subplot
#     # img = imread(path)
#     # axs[1].imshow(img)
#     # axs[1].set_title("Original Image")
#     # plt.show()