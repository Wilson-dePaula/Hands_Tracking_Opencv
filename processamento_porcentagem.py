#________________Imports___________________
import numpy as np
from matplotlib import pyplot as plt
import cv2

#________________Functions___________________
def contar_faixas_de_cores(faixa1, faixa2, faixa3):
    imgg = cv2.imread('final.jpg')
    # Converta as faixas de cores para arrays NumPy
    faixa1 = np.array(faixa1, dtype=np.uint8)
    faixa2 = np.array(faixa2, dtype=np.uint8)
    faixa3 = np.array(faixa3, dtype=np.uint8)

    # Crie máscaras para as três faixas de cores
    mascara1 = cv2.inRange(imgg, faixa1[0], faixa1[1])
    mascara2 = cv2.inRange(imgg, faixa2[0], faixa2[1])
    mascara3 = cv2.inRange(imgg, faixa3[0], faixa3[1])

    # pixels em cada máscara
    contagem_faixa1 = cv2.countNonZero(mascara1)
    contagem_faixa2 = cv2.countNonZero(mascara2)
    contagem_faixa3 = cv2.countNonZero(mascara3)

    # Exiba a contagem de pixels em cada faixa de cores
    print(f"Contagem na faixa de cores escuras: {contagem_faixa1} pixels")
    print(f"Contagem na faixa de cores claras: {contagem_faixa2} pixels")
    print(f"Contagem na faixa de cores verde: {contagem_faixa3} pixels")
    return contagem_faixa1, contagem_faixa2, contagem_faixa3

def calcular_e_atualizar_percentual(por):

    valor_referencia = 80

    if por > valor_referencia:
        return (f'O valor percentual ({por}%) é maior do que o valor de referência ({valor_referencia}%)')
    elif por < valor_referencia:
        return(f'O valor percentual ({por}%) é menor do que o valor de referência ({valor_referencia}%)')
    else:
       return(f'O valor percentual ({por}%) é igual ao valor de referência ({valor_referencia}%)')

def exec_calc_porc(path):
    # Insira o caminho da imagem que você deseja analisar
    #path = 'imagem1.jpg'
    img = cv2.imread(path)
    (b, g, r) = cv2.split(img)
    #cv2.imshow('blue channel', b)

    # filtro preto
    image_copy = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([80, 80, 80])  # default 150, 53, 100
    mask = cv2.inRange(image_copy, lower_black, upper_black)

    # preto & branco - imagem1
    ret, thresh6 = cv2.threshold(b, 68, 255, cv2.THRESH_BINARY)  # default 68,255

    borda = cv2.Canny(img, 20, 80)
    #cv2.imshow('borda', borda)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # filtros imagem1
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (15, 15))  # 15,15
    ele1 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    erode1 = cv2.erode(thresh6, ele1)
    dst = cv2.GaussianBlur(erode1, (5, 5), cv2.BORDER_DEFAULT)
    opening = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel)

    masked = cv2.bitwise_and(b, b, mask=thresh6)
    #cv2.imshow('mascara', masked)
    #cv2.waitKey(0)

    # apresentar imagem 1
    #plt.subplot(2, 2, 1), plt.imshow(thresh6, "gray"), plt.title('imagem 1 - Binary')
    #plt.subplot(2, 2, 2), plt.imshow(dst, "gray"), plt.title('imagem 1 -Mediana')
    #plt.subplot(2, 2, 3), plt.imshow(erode1, "gray"), plt.title('imagem 1 -Erosão')
    #plt.subplot(2, 2, 4), plt.imshow(opening, "gray"), plt.title('imagem 1 -opening')

    # Aplica a dilatação na máscara para suavizar as bordas
    kernel_dilate = np.ones((2, 2), np.uint8)
    dilated_mask = cv2.dilate(masked, kernel_dilate, iterations=1)  # masked

    # detector de bordas 1
    Imagem_fundo_alt = cv2.cvtColor(dilated_mask, cv2.COLOR_BGR2RGB)  # converte a imagem para fundo verde
    #cv2.imshow('teste', Imagem_fundo_alt)

    masked_image = np.copy(Imagem_fundo_alt)
    masked_image[mask != 0] = [0, 255, 0]
    cv2.imshow('Imagem 1 - Final', masked_image)
    cv2.waitKey()

    #image = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)  # cinza
    #cv2.imshow('Imagem Final - 1', image)
    #cv2.waitKey()

    # salvar imagem png

    nome_do_arquivo_jpg = "final.jpg"
    cv2.imwrite(nome_do_arquivo_jpg, masked_image)
    cv2.waitKey()

    # Defina as duas faixas de cores como intervalos [B, G, R] mínimos e máximos
    faixa1 = ([0, 0, 0], [149, 149, 149])  # faixa de cores escuras
    faixa2 = ([150, 150, 150], [255, 255, 255])  # faixa de cores claras
    faixa3 = ([0, 255, 0], [0, 255, 0])  # faixa de cores verdes
    contagem_faixa1, contagem_faixa2, contagem_faixa3 = contar_faixas_de_cores(faixa1, faixa2, faixa3)
    # porcentagem
    por = (contagem_faixa2 / (contagem_faixa1 + contagem_faixa2)) * 100
    return por


if __name__ == "__main__":
    exec_calc_porc('imagem1.jpg')
