# O que deve ser feito?
# É preciso fazer um modelo de reconhecimento facial de um vídeo da Pifa, que seja preciso a ponto de evitar a detecção de rostos desfocados

# 1°) Definir o modelo de detecção -> Haar
# 2°) Transformar o vídeo em frames 
# 3°) Usar múltiplos modelo para melhorar a precisão de detecção, ao menos 2
# 4°) Detectar e demarcar os rostos
# 5°) Salvar imagens demarcadas 
# 6°) Transformar imagens em vídeo

#=======================================================================================================================================================================#
import cv2
from os.path import exists, join
from threading import Thread
from PIL import Image
from os import makedirs, listdir

raw_imagens_dir_path:str = "./src/imgs/raw" # Caminho dos frames do vídeo original
delimited_imagens_dir_path:str = "./src/imgs/delimited" # Caminho das imagens que tiveram rostos identificados

# 1°) Parte - Modelos Haar
frontal_face_haar_model_path:str = "./src/data/haarcascade_frontalcatface_extended.xml" # Modelo de detecção de rosto frontal
frontal_eyes_haar_model_path:str = "./src/data/haarcascade_eye.xml" # Modelo de detecção de olhos frontal


# 2°) Parte - Transformar frames do vídeo em imagens
def get_frames(video_path:str) -> None :
    """
    Função que transforma vídeo em frames separados

    Parâmetros
    video_path : str : caminho do vídeo
    """
    try:
        video = cv2.VideoCapture(filename=video_path) # Captura de vídeo
        
        current_frame:int = 0 # Número do frame atual do vídeo
        while True:
            ret, frame = video.read()

            if ret: # Verifica se está ocorrendo a leitura do vídeo
                frame_name = f"raw_frame_{str(current_frame)}.jpeg" # Define nome do frame

                if not exists(f"{raw_imagens_dir_path}/{frame_name}"): # Verifica se imagem não existe, para evitar redundâncias
                    cv2.imwrite( # Salva frame como imagem
                        filename=f"{raw_imagens_dir_path}/{frame_name}",
                        img=frame
                    )

            else: # Caso não esteja, quebra o loop
                break

            current_frame += 1

    except Exception as e:
        print(e)


# 4°) Parte - Delimitar
def put_rectangles(img, faces, eyes) :
    """
    Função que desenha retângulos na imagem, delimitando as faces

    Parâmetros
    img : any : imagem a ser delimitada
    faces : vector : valores dos pontos de delimitação das faces
    eyes  : vector : valores dos pontos de delimitação dos olhos
    """

    img_out = img.copy() # Copia imagem

    for face in faces:
        f_position_x, f_position_y, f_width, f_length = face

        for eye in eyes:
            y_position_x, y_position_y, y_width, y_length = eye

            if y_position_x <= f_position_x and y_position_y <= f_position_y and y_width <= f_width and y_length <= f_length:
                print("Desenhou")
                cv2.rectangle( # Desenha retângulo nas faces
                    img=img_out, 
                    pt1=(f_position_x, f_position_y),
                    pt2=(f_width, f_length),
                    color=(255,255,255),
                    thickness=3
                )
            else:
                pass

    # for eye in eyes:
    #     position_x, position_y, width, length = eye

    #     cv2.rectangle( # Desenha retângulo nos olhos
    #         img=img_out, 
    #         pt1=(position_x, position_y),
    #         pt2=(width, length),
    #         color=(255,255,255),
    #         thickness=2
    #     )

    return img_out # Retorna imagem com retângulos desenhados


# 3°) Parte - Modelos de identificação
def classify(img_path:str) -> None :
    """
    Função que faz a classificação dos rostos nas imagens

    Parâmetros
    img_path : str : caminho da imagem
    """
    frame = cv2.imread(filename=img_path) # Faz a leitura da imagem
    
    face_haar_model = cv2.CascadeClassifier(filename=frontal_face_haar_model_path) # Modelo de Classificação Haar Cascade de face frontal
    eyes_haar_model = cv2.CascadeClassifier(filename=frontal_eyes_haar_model_path) # Modelo de classificação Haar Cascade de olhos

    faces = face_haar_model.detectMultiScale(image=frame) # Detecta faces na imagem
    eyes  = eyes_haar_model.detectMultiScale(image=frame) # Detecta olhos na imagem

    print(f"Faces ==> {faces}")
    print(f"Eyes  ==> {eyes}")

    delimited_frame = put_rectangles( # Chama função de delimitação de imagens e olhos
        img=frame,
        faces=faces,
        eyes=eyes
    )

    return delimited_frame # Retorna o frame delimitado


def assembly_video(imgs_dir_path:str) -> None:
    """
    Função que cria o vídeo com os frames delimitados

    Parâmetros 
    imgs_dir_path : str : diretório de imagens 
    """

    for frame in listdir(imgs_dir_path):
        img = Image.open(join(imgs_dir_path, frame))

        w



if __name__ == "__main__":
    try:
        # Cria pastas com as imagens
        if not exists(raw_imagens_dir_path):
            makedirs(raw_imagens_dir_path)

        elif not exists(delimited_imagens_dir_path):
            makedirs(delimited_imagens_dir_path)
    
    except Exception as e:
        print(e)

    get_frames(video_path="./src/video/la_cabra.mp4")

    current_frame = 0

    while True:
        raw_frame = f"{raw_imagens_dir_path}/raw_frame_{str(current_frame)}.jpeg" 
        
        if exists(raw_frame):
            print(current_frame)

            identified_img = classify(img_path=raw_frame)
            identified_img_path = f"{delimited_imagens_dir_path}/delimited_frame_{current_frame}.jpeg"

            if not exists(identified_img_path):
                cv2.imwrite(filename=identified_img_path, img=identified_img)
                cv2.waitKey(0)
            else:
                pass

        else:
            break

        current_frame += 1