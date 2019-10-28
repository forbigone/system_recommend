

#cosin相似度（余弦相似度）
from PIL import Image
from numpy import average, dot, linalg
 
# 对图片进行统一化处理
def get_thum(image, size=(64,64), greyscale=False):
    # 利用image对图像大小重新设置, Image.ANTIALIAS为高质量的
    image = image.resize(size, Image.ANTIALIAS)
    if greyscale:
        # 将图片转换为L模式，其为灰度图，其每个像素用8个bit表示
        image = image.convert('L')
    return image
 
# 计算图片的余弦距离
def image_similarity_vectors_via_numpy(image1, image2):
    image1 = get_thum(image1)
    image2 = get_thum(image2)
    images = [image1, image2]
    vectors = []
    norms = []
    for image in images:
        vector = []
        for pixel_tuple in image.getdata():
            vector.append(average(pixel_tuple))
        vectors.append(vector)
        # linalg=linear（线性）+algebra（代数），norm则表示范数
        # 求图片的范数？？
        norms.append(linalg.norm(vector, 2))
    a, b = vectors
    a_norm, b_norm = norms
    # dot返回的是点积，对二维数组（矩阵）进行计算
    res = dot(a / a_norm, b / b_norm)
    return res
 
 
image1 = Image.open('house1.jpg')
image2 = Image.open('house2.jpg')
cosin = image_similarity_vectors_via_numpy(image1, image2)
print('图片余弦相似度',cosin)










'''
#利用SSIM（结构相似度度量）计算图片的相似度
from skimage.measure import compare_ssim
from scipy.misc import imread
import numpy as np
 
# 读取图片
img1 = imread('house1.jpg')
img2 = imread('house2.jpg')
img2 = np.resize(img2, (img1.shape[0], img1.shape[1], img1.shape[2]))
print(img1.shape)
print(img2.shape)
ssim =  compare_ssim(img1, img2, multichannel = True)
print(ssim)



'''




'''
#通过直方图计算
#直方图过于简单，只能捕捉颜色信息的相似性，捕捉不到更多的信息。只要颜色分布相似，就会判定二者相似度较高。

from PIL import Image
 
# 将图片转化为RGB
def make_regalur_image(img, size=(64, 64)):
    gray_image = img.resize(size).convert('RGB')
    return gray_image
 
# 计算直方图
def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    hist = sum(1 - (0 if l == r else float(abs(l-r))/max(l,r))for l, r in zip(lh, rh))/len(lh)
    return hist
 
# 计算相似度
def calc_similar(li, ri):
    calc_sim = hist_similar(li.histogram(), ri.histogram())
    return calc_sim
 
if __name__ == '__main__':
    image1 = Image.open('house1.jpg')
    image1 = make_regalur_image(image1)
    image2 = Image.open('house2.jpg')
    image2 = make_regalur_image(image2)
    print("图片间的相似度为",calc_similar(image1, image2))
'''