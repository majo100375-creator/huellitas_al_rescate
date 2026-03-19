import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
import os
from PIL import Image
from datetime import date

st.set_page_config(
    page_title="Huellitas al rescate",
    page_icon="🐾",
    layout="wide"
)

if 'menu_actual' not in st.session_state:
    st.session_state.menu_actual = "Inicio"

def analizar_foto_cnn(imagen_pil):
    img_array = np.array(imagen_pil.convert('L'))
    brillo_promedio = np.mean(img_array)
    if brillo_promedio > 220:
        return "MUCHA_LUZ", "No logramos apreciar a nuestro amigo, hay mucha luz 🙁."
    elif brillo_promedio < 50:
        return "OSCURA", "Nuestro amigo anda por ahí 👀, no logro verlo esta muy oscuro."
    else:
        return "PERFECTA", "Excelente, Nuestro amigo encontrará una nueva familia muy pronto ❤️."

@st.cache_resource
def cargar_modelos():
    modelos = {}
    archivos = {
        'clasificacion': 'modelo_clasificacion.pkl',
        'regresion': 'modelo_regresion.pkl',
        'adopcion': 'modelo_adopcion.pkl',
        'adoptante': 'modelo_adoptante.pkl',
        'encoder': 'encoder_animal_type.pkl'
    }
    for nombre, archivo in archivos.items():
        try:
            with open(archivo, 'rb') as f:
                modelos[nombre] = pickle.load(f)
        except: 
            modelos[nombre] = None
    return modelos
modelos = cargar_modelos()

@st.cache_data
def cargar_datos_adopcion():
    try:
        with open('adopcion.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except: 
        return []

def evaluar_regresion(datos, modelo):
    if modelo is None:
        score = 100
        if datos['alquilada'] == "Alquilada" and datos['permiso'] == "No": score -= 40
        if datos['solo'] == "Si": score -= 10
        if datos['entrenador'] == "No": score -= 20
        if datos['adaptacion'] == "Menos de una semana": score -= 20
        return max(0, min(100, score))
    df_input = pd.DataFrame([datos])
    return modelo.predict(df_input)[0]

def main():
    modelos = cargar_modelos()
    animales = cargar_datos_adopcion()
    st.sidebar.title("🐾Menú🐾")
    opciones = ["Inicio", "Animales en adopción", "Formulario completo", "Análisis de imágenes", "Estadísticas", "Gestión de Estancia (Staff)"]
    menu = st.sidebar.radio("Ir a:", opciones, index=opciones.index(st.session_state.menu_actual))
    st.session_state.menu_actual = menu

    if st.session_state.menu_actual == "Inicio":
        st.title("🐾 Bienvenidos a Huellitas al Rescate 🐾")
        st.image("images/inicio.png", use_container_width=True)

    elif st.session_state.menu_actual == "Animales en adopción":
        st.title("🐱🐶 Encuentra a tu mejor amigo 🐦🐮")
        
        categorias = ["Todos", "Perro", "Gato", "Aves", "Bovinos"]
        tabs = st.tabs(categorias)
        
        for i, cat in enumerate(categorias):
            with tabs[i]:
                if cat == "Todos":
                    busqueda = animales
                else:
                    busqueda = [
                        a for a in animales
                        if str(a.get('especie', '')).strip().lower() == cat.strip().lower()
                    ]

                if not busqueda:
                    st.info(f"No hay {cat} disponibles.")
                else:
                    cols = st.columns(3)
                    for idx, r in enumerate(busqueda):
                        with cols[idx % 3]:
                            with st.container(border=True):
                                foto_ruta = r.get('foto', '')
                                img_final = None
                                posibles_rutas = [foto_ruta, os.path.join("images", os.path.basename(foto_ruta)), foto_ruta.replace(".jpeg", ".jpg"), foto_ruta.replace(".jpg", ".jpeg")]

                                for ruta in posibles_rutas:
                                    if os.path.exists(ruta):
                                        img_final = Image.open(ruta)
                                        break
                                
                                if img_final:
                                    st.image(img_final, use_container_width=True)
                                else:
                                    st.warning("Foto no disponible")
                                    
                                st.subheader(r.get('nombre'))
                                st.write(f"**Raza:** {r.get('raza')} | **Edad:** {r.get('edad')}")
                                if st.button(f"Adoptar a {r.get('nombre')}", key=f"btn_{r.get('id')}_{cat}_{idx}"):
                                    st.session_state.menu_actual = "Formulario completo"
                                    st.rerun()

    elif st.session_state.menu_actual == "Formulario completo":
        st.title("🐾Formulario de Adopción Responsable🐾")
        with st.form("form_oficial"):
            st.header("Información Personal")
            c1, c2 = st.columns(2)
            with c1: 
                nombre = st.text_input("Nombre completo")
                dni = st.text_input("Dni/Identificación")
                edad_u = st.number_input("Edad", min_value=18)
            with c2: 
                direccion = st.text_input("Dirección")
                telefono = st.number_input("Teléfono", min_value=0)
                ocupacion = st.text_input("Ocupación")
            
            st.header("Entorno Familiar")
            c3, c4 = st.columns(2)
            with c3: 
                tipo_v = st.selectbox("Tipo de vivienda", ["Casa", "Apartamento", "Finca/Otro"])
                propiedad = st.radio("La propiedad es:", ["Propia", "Alquilada"])
                if propiedad == "Alquilada":
                    permiso = st.radio("¿Tiene permiso?", ["Si", "No"])
                else:
                    permiso = "Si"

            with c4: 
                personas = st.slider("Personas en casa", 0, 20, 1)
                ninos = st.radio("¿Hay niños?", ["No", "Si"])
                if ninos == "Si":
                    cant_ninos = st.slider("¿Cuantos?", 0, 10, 0)
                else:
                    cant_ninos = 0

            solo = st.radio("¿El animal estará solo?", ["No", "Si"])
            entrenador = st.radio("¿Invertirá en un entrenador en caso de que la mascota desarrolle conductas inapropiadas?", ["Sí", "No"])
            adaptacion = st.selectbox("Tiempo de adaptación", ["Menos de una semana", "Un mes", "El tiempo que sea necesario"])
            firma = st.text_input("Firma del Solicitante")
            aceptar = st.checkbox("Declaro que la información es verdadera.")

            if st.form_submit_button("Enviar Solicitud"):
                if aceptar and firma:
                    datos = {"alquilada": propiedad, "permiso": permiso, "solo": solo, "entrenador": entrenador, "adaptacion": adaptacion}
                    score = evaluar_regresion(datos, modelos['regresion'])
                    if score > 85: 
                        st.success(f"{score:.1f}% ¡FELICIDADES! Estás una huella más cerca de tener un nuevo amigo.✅")
                    elif score > 65: 
                        st.warning(f"{score:.1f}% Nos falta información, contáctaremos contigo⚠️")
                    else: 
                        st.error(f"{score:.1f}% Lamentablemente no cumples con los requisitos mínimos para adoptar. 😔")
                else: 
                    st.error("Firma y acepta los términos.")

    elif st.session_state.menu_actual == "Análisis de imágenes":
        st.title("🐾Verificación de Imagen de Rescate🐾")
        subido = st.file_uploader("Sube la foto...", type=["jpg", "jpeg", "png"])
        if subido:
            img = Image.open(subido)
            st.image(img, width=400)
            est, msg = analizar_foto_cnn(img)
            if est == "PERFECTA": st.success(msg)
            elif est == "MUCHA_LUZ": st.error(msg)
            else: st.warning(msg)

    elif st.session_state.menu_actual == "Estadísticas":
        st.title("🐾Estadísticas y Árbol de Decisión🐾")
        if animales:
            df_stats = pd.DataFrame(animales)
            df_stats['Horas Solo'] = np.random.choice([2, 4, 8, 10], len(df_stats))
            df_stats['Presencia Niños'] = np.random.choice(['Si', 'No'], len(df_stats))
            
            def clasificar_riesgo(row):
                if row['Horas Solo'] > 8 and "Cachorro" in row['edad']: 
                    return "Alto Riesgo 🔴"
                return "Bajo Riesgo 🟢"
            
            df_stats['Clasificación Riesgo'] = df_stats.apply(clasificar_riesgo, axis=1)
            st.dataframe(df_stats[['nombre', 'especie', 'raza', 'edad', 'Clasificación Riesgo']], use_container_width=True)
            st.metric("Total Animales", len(animales))

    elif st.session_state.menu_actual == "Gestión de Estancia (Staff)":
        st.title("🛠️ Gestión de Estancia para el Staff")
        st.markdown("### Predecir tiempo de salida y estrategias (Austin Animal Center)")
        
        col_form, col_res = st.columns([1, 1])
        
        with col_form:
            st.subheader("🐾Datos del Animal🐾")
            with st.container(border=True):
                esp = st.selectbox("Especie", ["Dog", "Cat", "Bird", "Livestock"], key="staff_esp")
                raz = st.text_input("Raza / Mezcla", "Mixed Breed", key="staff_raz")
                edad_m = st.number_input("Edad (en meses)", min_value=0, value=12, key="staff_edad")
                motivo = st.selectbox("Estado de salud", ["Normal", "Enfermo (Sick)", "Herido (Injured)", "Anciano"], key="staff_mot")
                calcular = st.button("Calcular Tiempo Estimado")

        with col_res:
            st.subheader("💡Resultados y Estrategias")
            resultado_cont = st.container()

            if calcular:
                with resultado_cont:
                    if modelos['regresion'] and modelos['encoder']:
                        try:
                            esp_enc = modelos['encoder'].transform([esp])[0]
                            pred = modelos['regresion'].predict(np.array([[esp_enc, edad_m]]))[0]
                            st.metric("Estancia Prevista", f"{int(abs(pred))} días")
                        except:
                            st.info("Nota: Modelo requiere ajuste de dimensiones. Estimación: 45 días.")
                    else:
                        st.warning("Usando lógica de reserva: 30-60 días estimados.")

                    if motivo == "Enfermo (Sick)":
                        st.error("🚨 **Protocolo Médico:** Priorizar casa de acogida para evitar contagios y estrés.")
                    if edad_m > 95:
                        st.warning("👴 **Perfil Senior:** Se recomienda 'Senior for Senior' (descuento en tasas).")
            
                    st.info("📸**Tip de Marketing:** Asegura una foto de alta calidad en la pestaña 'Análisis de Imágenes'. 🐾Asi aumentaremos las oportunidades de acogida de nuestro amigo peludo🐾.")

if __name__ == "__main__":
    main()