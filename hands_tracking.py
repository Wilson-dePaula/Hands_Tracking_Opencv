#________________Imports___________________
import numpy as np
import cv2
import mediapipe as mp
import matplotlib.pyplot as plt

#________________Functions___________________
# Inicialize o MediaPipe Hands
def hands_track():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.00001, min_tracking_confidence=0.00001)
    return hands

def captura_imagens_mao_sup(hands):
    # Carregue a imagem original
    image = cv2.imread('imagem1.jpg')
    print(f'Dimensões da Imagem: {image.shape}')

    # Detecte as mãos na imagem
    results = hands.process(image)

    # Libere os recursos
    hands.close()

    return image, hands, results

def captura_imagens_mao_inf(hands):
    # Carregue a imagem original
    image2 = cv2.imread('imagem2.jpg')
    print(f'Dimensões da Imagem: {image2.shape}')

    # Detecte as mãos na imagem
    results_2 = hands.process(image2)

    # Libere os recursos
    hands.close()

    return image2, hands, results_2


# ---------------------------Mão Superior ----------------------------------
def exec_mao_sup(image, results, hands):
    # Crie imagens vazias para a mão direita e esquerda com tipo de dados np.uint8
    mao_direita = np.zeros_like(image, dtype=np.uint8)
    mao_esquerda = np.zeros_like(image, dtype=np.uint8)

    x_min, x_max, y_min, y_max = 0, 0, 0, 0  # Inicialize as variáveis com valores padrão

    # Verifique se as mãos foram detectadas
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extrair os pontos-chave da mão
            landmarks = hand_landmarks.landmark
            for landmark in hand_landmarks.landmark:
                print(f'Posição do ponto: x={landmark.x}, y={landmark.y}, z={landmark.z}')

            # Extrair os pontos-chave da mão
            landmarks = hand_landmarks.landmark

            # Copie a imagem original para adicionar a mão
            hand_image = image.copy()

            # Defina uma margem (margem_x e margem_y) para ampliar a ROI da mão
            margem_x = 30
            margem_y = 30

            # Defina uma região de interesse (ROI) para cada mão com margens
            x_min = int(min(landmark.x * image.shape[1] for landmark in landmarks)) - margem_x
            x_max = int(max(landmark.x * image.shape[1] for landmark in landmarks)) + margem_x
            y_min = int(min(landmark.y * image.shape[0] for landmark in landmarks)) - margem_y
            y_max = int(max(landmark.y * image.shape[0] for landmark in landmarks)) + margem_y

            # Certifique-se de que os valores mínimos e máximos estão dentro dos limites da imagem
            x_min = max(0, x_min)
            x_max = min(image.shape[1], x_max)
            y_min = max(0, y_min)
            y_max = min(image.shape[0], y_max)

            # Recorte e salve a imagem da mão direita
            if landmarks[0].x < landmarks[17].x:
                mao_direita = hand_image[y_min:y_max, x_min:x_max]
                cv2.imwrite('sup_mao_direita.jpg', mao_direita)
            # Recorte e salve a imagem da mão esquerda
            else:
                mao_esquerda = hand_image[y_min:y_max, x_min:x_max]
                cv2.imwrite('sup_mao_esquerda.jpg', mao_esquerda)
    else:
        print('Nenhuma mão detectada.')

    print(f'Coordenadas de corte para mão direita: x_min={x_min}, x_max={x_max}, y_min={y_min}, y_max={y_max}')
    print(f'Coordenadas de corte para mão esquerda: x_min={x_min}, x_max={x_max}, y_min={y_min}, y_max={y_max}')

    # Crie uma figura com duas subtramas (uma para a mão direita e outra para a mão esquerda)
    plt.figure(figsize=(12, 6))

    # Subtrama para a mão direita
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(mao_direita, cv2.COLOR_BGR2RGB))  # Converta para o formato de cores correto
    plt.title('Sup_Mão Direita')

    # Subtrama para a mão esquerda
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(mao_esquerda, cv2.COLOR_BGR2RGB))  # Converta para o formato de cores correto
    plt.title('Sup_Mão Esquerda')

    plt.show()

    # possibilidade de ajusta - inverter mãos
    mao_direita_rgb = cv2.cvtColor(mao_direita, cv2.COLOR_BGR2RGB)
    mao_esquerda_rgb = cv2.cvtColor(mao_esquerda, cv2.COLOR_BGR2RGB)

    print('Dimensões da Mão Direita:', mao_direita.shape)
    print('Dimensões da Mão Esquerda:', mao_esquerda.shape)

    mao_direita_rgb = cv2.cvtColor(mao_direita, cv2.COLOR_BGR2RGB)
    mao_esquerda_rgb = cv2.cvtColor(mao_esquerda, cv2.COLOR_BGR2RGB)

    # Aguarde até que uma tecla seja pressionada e, em seguida, feche as janelas
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ---------------------------Mão Inferior----------------------------------
def exec_mao_inf(image2, results_2, hands):
    # Crie imagens vazias para a mão direita e esquerda com tipo de dados np.uint8
    mao_direita = np.zeros_like(image2, dtype=np.uint8)
    mao_esquerda = np.zeros_like(image2, dtype=np.uint8)

    x_min, x_max, y_min, y_max = 0, 0, 0, 0  # Inicialize as variáveis com valores padrão

    # Verifique se as mãos foram detectadas
    if results_2.multi_hand_landmarks:
        for hand_landmarks in results_2.multi_hand_landmarks:
            # Extrair os pontos-chave da mão
            landmarks = hand_landmarks.landmark
            for landmark in hand_landmarks.landmark:
                print(f'Posição do ponto: x={landmark.x}, y={landmark.y}, z={landmark.z}')

            # Extrair os pontos-chave da mão
            landmarks = hand_landmarks.landmark

            # Copie a imagem original para adicionar a mão
            hand_image = image2.copy()

            # Defina uma margem (margem_x e margem_y) para ampliar a ROI da mão
            margem_x = 30
            margem_y = 30

            # Defina uma região de interesse (ROI) para cada mão com margens
            x_min = int(min(landmark.x * image2.shape[1] for landmark in landmarks)) - margem_x
            x_max = int(max(landmark.x * image2.shape[1] for landmark in landmarks)) + margem_x
            y_min = int(min(landmark.y * image2.shape[0] for landmark in landmarks)) - margem_y
            y_max = int(max(landmark.y * image2.shape[0] for landmark in landmarks)) + margem_y

            # Certifique-se de que os valores mínimos e máximos estão dentro dos limites da imagem
            x_min = max(0, x_min)
            x_max = min(image2.shape[1], x_max)
            y_min = max(0, y_min)
            y_max = min(image2.shape[0], y_max)

            # Recorte e salve a imagem da mão direita
            if landmarks[0].x < landmarks[17].x:
                mao_direita = hand_image[y_min:y_max, x_min:x_max]
                cv2.imwrite('inf_mao_esquerda.jpg', mao_direita)
            # Recorte e salve a imagem da mão esquerda
            else:
                mao_esquerda = hand_image[y_min:y_max, x_min:x_max]
                cv2.imwrite('inf_mao_direita.jpg', mao_esquerda)
    else:
        print('Nenhuma mão detectada.')

    print(f'Coordenadas de corte para mão direita: x_min={x_min}, x_max={x_max}, y_min={y_min}, y_max={y_max}')
    print(f'Coordenadas de corte para mão esquerda: x_min={x_min}, x_max={x_max}, y_min={y_min}, y_max={y_max}')

    # Crie uma figura com duas subtramas (uma para a mão direita e outra para a mão esquerda)
    plt.figure(figsize=(12, 6))

    # Subtrama para a mão direita
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(mao_direita, cv2.COLOR_BGR2RGB))  # Converta para o formato de cores correto
    plt.title('inf_Mão Esquerda')

    # Subtrama para a mão esquerda
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(mao_esquerda, cv2.COLOR_BGR2RGB))  # Converta para o formato de cores correto
    plt.title('Inf_Mão Direita')

    plt.show()

    # possibilidade de ajusta - inverter mãos
    mao_direita_rgb = cv2.cvtColor(mao_direita, cv2.COLOR_BGR2RGB)
    mao_esquerda_rgb = cv2.cvtColor(mao_esquerda, cv2.COLOR_BGR2RGB)

    print('Dimensões da Mão Direita:', mao_direita.shape)
    print('Dimensões da Mão Esquerda:', mao_esquerda.shape)

    mao_direita_rgb = cv2.cvtColor(mao_direita, cv2.COLOR_BGR2RGB)
    mao_esquerda_rgb = cv2.cvtColor(mao_esquerda, cv2.COLOR_BGR2RGB)

    # Aguarde até que uma tecla seja pressionada e, em seguida, feche as janelas
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print('Exectute functions')
    image, hands, results = captura_imagens_mao_sup(hands_track())
    image2, hands, results_2 = captura_imagens_mao_inf(hands_track())
    exec_mao_sup(image, results, hands)
    exec_mao_inf(image2, results_2, hands)
