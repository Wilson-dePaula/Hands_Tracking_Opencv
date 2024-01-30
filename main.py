#________________Imports___________________
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os
import mediapipe as mp
from hands_tracking import hands_track, exec_mao_sup, exec_mao_inf, captura_imagens_mao_inf, captura_imagens_mao_sup
from processamento_porcentagem import exec_calc_porc, contar_faixas_de_cores, calcular_e_atualizar_percentual

#_____________ Variáveis globais para armazenar as imagens e as mãos detectadas_____________
imagem1 = None
imagem2 = None
processamento_habilitado = False  # Variável para controlar o reconhecimento
reconhecimento_habilitado = False  # Variável para controlar o reconhecimento

#________________Functions___________________

# Função para alternar o estado de processamento
def alternar_processamento(label_processamento):
    global processamento_habilitado
    processamento_habilitado = not processamento_habilitado
    if processamento_habilitado:
        label_processamento.config(text="Processamento Habilitado")
    else:
        label_processamento.config(text="Processamento Desabilitado")

def capturar_imagem1():
    global imagem1
    ret, frame = cap.read()
    if ret:
        imagem1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imagem1_tk = ImageTk.PhotoImage(image=Image.fromarray(imagem1))
        canvas_imagem1.create_image(0, 0, anchor=tk.NW, image=imagem1_tk)
        canvas_imagem1.imagem = imagem1_tk
        # Salva a imagem
        cv2.imwrite("imagem1.jpg", frame)
        image, hands, results = captura_imagens_mao_sup(hands_track())
        exec_mao_sup(image, results, hands)

def capturar_imagem2():
    global imagem2
    ret, frame = cap.read()
    if ret:
        imagem2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imagem2_tk = ImageTk.PhotoImage(image=Image.fromarray(imagem2))
        canvas_imagem2.create_image(0, 0, anchor=tk.NW, image=imagem2_tk)
        canvas_imagem2.imagem = imagem2_tk
        # Salva a imagem
        cv2.imwrite("imagem2.jpg", frame)
        image2, hands, results_2 = captura_imagens_mao_inf(hands_track())
        exec_mao_inf(image2, results_2, hands)

# Função para calcular a porcentagem da mão
def calcular_porcentagem_mao(imagem, label, label_aviso):

    media = []
    for im in imagem:
        porcentagem = exec_calc_porc(im)
        media.append(int(porcentagem))
    label.config(text=f"Porcentagem da Mão: {sum(media)/len(media):.2f}% | "
                      f"Porcentagem superior: {media[0]:.2f}% | "
                      f"Porcentagem inferior: {media[1]:.2f}%")
    aviso = calcular_e_atualizar_percentual(int(sum(media)/len(media)))
    label_aviso.config(text=f"Aviso Mão: {aviso}")


# Função para atualizar o vídeo no canvas
def exibir_video():
    ret, frame = cap.read()
    if ret:
        photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        canvas_video.create_image(0, 0, image=photo, anchor=tk.NW)
        canvas_video.photo = photo
        janela.after(10, exibir_video)

# Função para fechar a janela e excluir as imagens
def fechar_janela():

    # Verifique se a imagem1 foi capturada e exclua-a
    if os.path.exists("imagem1.jpg"):
        os.remove("imagem1.jpg")

    # Verifique se a imagem2 foi capturada e exclua-a
    if os.path.exists("imagem2.jpg"):
        os.remove("imagem2.jpg")

    # Verifique se a mao_esquerda foi gerada e exclua-a
    if os.path.exists("inf_mao_direita.jpg"):
        os.remove("inf_mao_direita.jpg")

    if os.path.exists("sup_mao_direita.jpg"):
        os.remove("sup_mao_direita.jpg")

    # Verifique se a mao_direita foi gerada e exclua-a
    if os.path.exists("inf_mao_esquerda.jpg"):
        os.remove("inf_mao_esquerda.jpg")

    if os.path.exists("sup_mao_esquerda.jpg"):
        os.remove("sup_mao_esquerda.jpg")

    if os.path.exists("final.jpg"):
        os.remove("final.jpg")

    cap.release()
    janela.destroy()


if __name__ == '__main__':
    # Configuração da interface tkinter
    janela = tk.Tk()
    janela.title("Exibição de Vídeo e Captura de Imagens")
    janela.geometry("1000x600")  # Define o tamanho da janela

    # Inicialize o MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    # Configurar o canvas para exibir o vídeo
    canvas_video = tk.Canvas(janela, width=640, height=480)
    canvas_video.grid(row=0, column=0, padx=10, pady=10,
                      rowspan=4)  # Aumentei o rowspan para ocupar mais espaço verticalmente

    # Configurar o canvas para exibir a primeira imagem capturada
    canvas_imagem1 = tk.Canvas(janela, width=480, height=320)  # Reduzi as dimensões para caber na tela
    canvas_imagem1.grid(row=0, column=2, padx=10, pady=10,
                        rowspan=2)  # Aumentei o rowspan para ocupar mais espaço verticalmente

    # Configurar o canvas para exibir a segunda imagem capturada
    canvas_imagem2 = tk.Canvas(janela, width=480, height=320)  # Reduzi as dimensões para caber na tela
    canvas_imagem2.grid(row=2, column=2, padx=10, pady=10,
                        rowspan=2)  # Aumentei o rowspan para ocupar mais espaço verticalmente

    # Configurar os botões de captura
    botao_captura1 = tk.Button(janela, text="Capturar Imagem 1", command=capturar_imagem1)
    botao_captura1.grid(row=0, column=1, padx=10, pady=10, sticky="w")  # Adicionei sticky para alinhar à esquerda

    botao_captura2 = tk.Button(janela, text="Capturar Imagem 2", command=capturar_imagem2)
    botao_captura2.grid(row=1, column=1, padx=10, pady=10, sticky="w")  # Adicionei sticky para alinhar à esquerda

    # Configurar os labels para exibir a porcentagem da mão
    label_porcentagem_mao1 = tk.Label(janela, text="Porcentagem Mão Direita: ")
    label_porcentagem_mao1.grid(row=5, column=0, padx=10, pady=10,
                                sticky="w")  # Adicionei sticky para alinhar à esquerda

    # Aviso
    label_aviso_mao1 = tk.Label(janela, text="Aviso Mão:")
    label_aviso_mao1.grid(row=6, column=0, padx=10, pady=10,
                                sticky="w")  # Adicionei sticky para alinhar à esquerda


    label_porcentagem_mao2 = tk.Label(janela, text="Porcentagem Mão Esquerda: ")
    label_porcentagem_mao2.grid(row=5, column=1, padx=10, pady=10,
                                sticky="w")  # Adicionei sticky para alinhar à esquerda

    #Aviso
    label_aviso_mao2 = tk.Label(janela, text="Aviso Mão:")
    label_aviso_mao2.grid(row=6, column=1, padx=10, pady=10,
                                sticky="w")  # Adicionei sticky para alinhar à esquerda

    # Configurar os botões para calcular a porcentagem da mão
    botao_calcular_mao1 = tk.Button(janela, text="Calcular Mão Direita",
                                    command=lambda: calcular_porcentagem_mao(["sup_mao_direita.jpg", "inf_mao_direita.jpg"], label_porcentagem_mao1, label_aviso_mao1))
    botao_calcular_mao1.grid(row=4, column=0, padx=10, pady=10, sticky="w")  # Adicionei sticky para alinhar à esquerda

    botao_calcular_mao2 = tk.Button(janela, text="Calcular Mão Esquerda",
                                    command=lambda: calcular_porcentagem_mao(["sup_mao_esquerda.jpg", "inf_mao_esquerda.jpg"], label_porcentagem_mao2, label_aviso_mao2))
    botao_calcular_mao2.grid(row=4, column=1, padx=10, pady=10, sticky="w")  # Adicionei sticky para alinhar à esquerda

    # Configurar o botão de fechar janela
    botao_fechar = tk.Button(janela, text="Fechar Janela", command=fechar_janela)
    botao_fechar.grid(row=6, column=4, columnspan=2, padx=10, pady=10,
                      sticky="w")  # Aumentei o rowspan para ocupar mais espaço verticalmente e adicionei sticky para alinhar à esquerda

    # Configurar o label para informar o estado do processamento
    label_processamento = tk.Label(janela, text="Processamento Desabilitado")
    label_processamento.grid(row=7, column=0, columnspan=2, padx=10, pady=10,
                             sticky="w")  # Adicionei sticky para alinhar à esquerda

    # Configurar o botão para habilitar/desabilitar processamento
    botao_processamento = tk.Button(janela, text="Habilitar/Desabilitar Processamento",
                                    command=lambda: alternar_processamento(label_processamento))
    botao_processamento.grid(row=8, column=0, columnspan=2, padx=10, pady=10,
                             sticky="w")  # Adicionei sticky para alinhar à esquerda

    # Inicializar a captura de vídeo
    cap = cv2.VideoCapture(0)
    exibir_video()

    janela.protocol("WM_DELETE_WINDOW", fechar_janela)
    janela.mainloop()
