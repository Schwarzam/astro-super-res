import torch
from utils import *
from PIL import Image
import matplotlib.pyplot as plt
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def visualize_sr(img, srresnet):
    hr_img = Image.open(img).convert('RGB')
    sr_img_srresnet = srresnet(convert_image(hr_img, source='pil', target='imagenet-norm').unsqueeze(0).to(device))
    sr_img_srresnet = sr_img_srresnet.squeeze(0).cpu().detach()
    sr_img_srresnet = convert_image(sr_img_srresnet, source='[-1, 1]', target='pil')
    sr_img_srresnet1 = sr_img_srresnet
    for i in range(4):
        sr_img_srresnet1 = image_filter(sr_img_srresnet1, "median", 3)
        
    fig, axs = plt.subplots(1, 3, figsize=(10, 5))
    fig.suptitle('Super-Resolution Comparison', fontsize=16)


    axs[0].imshow(hr_img)
    axs[0].set_title('Original')
    axs[0].axis('off')
    
    axs[1].imshow(sr_img_srresnet)
    axs[1].set_title('SRResNet')
    axs[1].axis('off')

    axs[2].imshow(sr_img_srresnet1)
    axs[2].set_title('SRResNet 6x median footprint 3')
    axs[2].axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    srresnet_checkpoint = "./checkpoints/checkpoint_srresnet_37_.pth.tar"

    srresnet = torch.load(srresnet_checkpoint)['model'].to(device)
    srresnet.eval()

    visualize_sr('galaxy_images/galaxy_5.png', srresnet) # Alterar para imagem desejada