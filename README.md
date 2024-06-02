# Análisis de Acciones con MATPLOTLIB

Este repositorio contiene scripts que ilustran el uso de la biblioteca MATPLOTLIB para el análisis de precios de acciones. En el ejemplo principal, se busca identificar acciones de empresas argentinas cuyo precio actual tenga una mayor diferencia porcentual respecto a su promedio semanal.

## Descripción

El propósito de estos scripts es proporcionar herramientas para el análisis de precios de acciones, específicamente:

- **Identificación de Acciones Subvaloradas**: Determinar qué acciones tienen un precio actual significativamente menor que su precio promedio semanal. Esto puede ayudar a los operadores bursátiles a identificar oportunidades de compra.
- **Visualización de Datos**: Utilizar MATPLOTLIB para visualizar los datos históricos de precios de las acciones seleccionadas, facilitando así la toma de decisiones informadas.

## Contenido

### Script Principal: `analisis_acciones.py`

Este script realiza los siguientes pasos:

1. **Descarga de Datos**: Utiliza la biblioteca `yfinance` para descargar los datos históricos de precios de las acciones.
2. **Cálculo del Promedio Semanal**: Calcula el precio promedio semanal de cada acción.
3. **Comparación de Precios**: Compara el precio actual con el promedio semanal para identificar acciones subvaloradas.
4. **Visualización**: Genera gráficos utilizando MATPLOTLIB para visualizar las acciones con la mayor diferencia porcentual.

### Ejecución del Script

Para ejecutar el script, sigue estos pasos:

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```

2. Instala las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```

3. Ejecuta el script principal:
    ```bash
    python analisis_acciones.py
    ```

## Ejemplo de Uso

El script se centra en obtener una visión semanal de los precios de las acciones de empresas argentinas. El objetivo es identificar aquellas acciones cuyo precio actual sea menor que su promedio semanal. Esto puede proporcionar información valiosa para realizar operaciones de compra o venta de acciones adecuadas.

```python
import yfinance as yf
from datetime import datetime, timedelta
from tabulate import tabulate
import matplotlib.pyplot as plt

# Definición de la clase y funciones (ver código principal en el repositorio)

