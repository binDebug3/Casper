from scipy import linalg as la
import numpy as np
from matplotlib import pyplot as plt
from imageio import imread


def svd_approx(A, s):
    """Return the best rank s approximation to A with respect to the 2-norm
    and the Frobenius norm, along with the number of bytes needed to store
    the approximation via the truncated SVD.
    Parameters:
        A ((m,n), ndarray)
        s (int): The rank of the desired approximation.
    Returns:
        ((m,n), ndarray) The best rank s approximation of A.
        (int) The number of entries needed to store the truncated SVD.
    """
    # get the SVD of A and compact it using s
    U, W, V = la.svd(A)
    if s > len(W):
        raise ValueError("Rank request is too big")

    UHat = U[:,:s]
    WHat = W[:s]
    VHat = V[:s,:]

    # calculate the number of elements to store and return compressed A
    size = UHat.size + WHat.size + VHat.size
    return UHat @ np.diag(WHat) @ VHat, size

# Problem 5
def compress_image(filename, s):
    """Plot the original image found at 'filename' and the rank s approximation
    of the image found at 'filename.' State in the figure title the difference
    in the number of entries used to store the original image and the
    approximation.
    Parameters:
        filename (str): Image file path.
        s (int): Rank of new image.
    """
    # import the image and find the shape
    image = imread(filename) / 255.
    entries = image.size

    # find the SVD approximation for each color based on s
    red, costRed = svd_approx(image[:,:,0], s)
    green, costGreen = svd_approx(image[:,:,1], s)
    blue, costBlue = svd_approx(image[:,:,2], s)

    red = np.clip(red, 0, 1)
    green = np.clip(green, 0, 1)
    blue = np.clip(blue, 0, 1)

    grayScale = np.dstack([red, green, blue])
    entries -= costRed + costBlue + costGreen

    # plot the original and the compressed colored images
    plt.subplot(1,2,1)
    plt.title("Original")
    plt.suptitle("Entries: " + str(image.size))
    plt.imshow(image)
    plt.subplot(1, 2, 2)
    plt.title(f"Compressed ({s})")
    plt.suptitle("Entries: " + str(entries))
    plt.imshow(grayScale)
    # plt.show()

    return
