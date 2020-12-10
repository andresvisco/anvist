import streamlit as st
import cargar

# import ptvsd
# ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
# ptvsd.wait_for_attach()

st.set_page_config(page_title='Reconocimiento de Caras',page_icon= 'favicon.jpg', layout = 'centered', initial_sidebar_state = 'auto')
st.markdown('<style>' + open('estilos.css').read() + '</style>' , unsafe_allow_html=True)
filePath = st.sidebar.file_uploader('Subir Archivo', key="uploader")

col1Sb, col2Sb = st.sidebar.beta_columns(2)
col1, col2 = st.beta_columns(2)
row1 = st.beta_container()

@st.cache(allow_output_mutation=True)
def main(_path):
    carga = cargar.Cargar(_path)
    img = carga.cargarImagen()
    # rotCount = carga._rotarCounter
    return carga, img#, rotCount


carga, img= main(filePath)

if row1.button('Rotar',key='RotarImagen'):
    carga._rotar()
    if carga._rotarCounter > 360:
        carga._rotarCounter = 0
    
    col1.subheader('Rotada {} gados'.format(str(carga._rotarCounter)))
    col1.image(carga._imagen ,width=300, use_column_width=True, channels='RGB')    

if col1Sb.button('Mostrar Imagen', key='B1'):
    col1.subheader('Imagen original')
    col1.image(img, width=300, use_column_width=True, channels='RGB')
    # st.image(carga._imagen, width=300, use_column_width=True, channels='RGB')
    
if col2Sb.button('Predecir Imagen', key='B2'):
    resultado, datos = carga._predecir(carga._imagen)
    col1.subheader('Imagen original')
    col1.image(img, width=300, use_column_width=True, channels='RGB')
    col2.subheader('Imagen analizada')
    col2.image(resultado,width=300, use_column_width=True, channels='RGB')

if st.sidebar.button('Pasar a BN', key='B3'):
    imgP = carga._imagenTemp# cargar.Image.Image.load(carga._imagenTemp)
    imgST = imgP.convert('LA')
    col1.subheader('Imagen BN')
    col1.image(imgST, width=300, use_column_width=True, channels='RGB')

