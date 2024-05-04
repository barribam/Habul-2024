# Habul-2024

## Creacion de entorno e instalacion de dependencias para ejecucion del sistema

#### Despues de clonar el repositorio, es necesario crear un entorno para ejecutar correctamente el sistema

python -m venv venv

#### Activacion el entorno virtual

venv\Scripts\activate

#### Instalacion de dependencias

pip install -r requirements.txt

## Paso 1. Recoleccion de imagenes

Ejecutar collect_imgs.py (toma en cuenta el cambiar el numero de video capturadora en 0 para utilizar la camara predeterminada)

## Paso 2. Creacion de base de datos 

Ejecutar create_dataset.py

## Paso 3. Entrenamiento del modelo

Ejecutar train_classifier.py

## Paso 4. Visualizacion del sistema

Ejecutar inference_classifier.py (Toma en cuenta que no puede haber mas de dos manos)

Para terminar la ejecucion, presionar "q" (quit)

## Creditos

