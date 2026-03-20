**🐾 Huellitas al Rescate: Sistema Inteligente de Adopción🐾**
¡Bienvenido a Huellitas al Rescate! Plataforma de Optimización de Refugios y Riesgo de Abandono y Adopción

¿Qué hace este proyecto?
Este sistema no es solo una página web; utiliza modelos de datos para tomar decisiones inteligentes, tales como:

*Análisis de Imágenes:* Una "red neuronal" (simulada) que revisa si las fotos de los animales tienen la luz adecuada para ser publicadas.

*Evaluación de Adoptantes:* Un formulario que analiza, basanándose en la base de datos, si una persona es apta para adoptar basándose en su entorno (casa, tiempo disponible, etc.).

*Gestión de Estancia (Staff):* Herramienta para que el refugio prediga cuántos días podría estar un animal en el centro antes de ser adoptado.

**🛠️Requisitos e Instalación**
Para ejecutar este proyecto en tu computadora, sigue estos pasos sencillos:

1. Clonar o descargar el repositorio
Si usas Git, ejecuta en una nueva terminal:

Bash
git clone [https://github.com/majo100375-creator/huellitas_al_rescate.git]
cd huellitas_al_rescate

2. Crear un entorno virtual (Recomendado)
Esto es como crear una "cajita" limpia donde solo instalaremos lo necesario para este proyecto:

Bash
python -m venv venv

*En Windows:*
venv\Scripts\activate

*En Mac/Linux:*
source venv/bin/activate

3. Instalar las librerías necesarias
Ejecuta el siguiente comando para instalar todas las herramientas que utilizaremos:

Bash
pip install -r requirements.txt

**NOTA:** Si no tienes el archivo requirements.txt, puedes crearlo con este contenido:
streamlit, pandas, numpy, Pillow.

*Estructura del Proyecto*

app.py: El código principal de la página web.

adopcion.json: Base de datos con la información de los animalitos disponibles en el refugio.

images/: Carpeta donde se guardan las fotos de los rescatados desponibles para adopción.

*.pkl: Archivos "Pickle". Son los modelos de IA ya "entrenados" y guardados para que el programa pueda predecir.

**Cómo ejecutar el proyecto**
Una vez instaladas las dependencias, solo tienes que escribir en tu terminal:

Bash
streamlit run app.py
Se abrirá automáticamente una pestaña en tu navegador con la aplicación funcionando. ¡Listo para rescatar huellitas!

*Conceptos de IA usados* -> Datos curiosos 

**IMPORTANTE**
#En el área de "Lanzamientos" encontrarás el Zip de los documentos informativos y el Zip de la primera versión de Huellitas al rescate.

Regresión: Lo usamos para calcular el "score" de adopción y los días de estancia. Fórmula matemática que predice un número basado en variables.

Clasificación: Ayuda a decidir si una adopción es de "Alto" o "Bajo" riesgo según las estadísticas e historial de adopción subyacentes.

Procesamiento de Imágenes: Usamos la librería PIL y numpy para convertir una foto en números (píxeles) y analizar su brillo.
