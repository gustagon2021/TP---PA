import yfinance as yf
from datetime import datetime, timedelta
from tabulate import tabulate
import matplotlib.pyplot as plt
plt.style.use('./estilos/mi_estilo.mplstyle')

class Accion:     #DEFINE LA CLASE ACCION 
    def __init__(self, symbol): #ATRIBUTOS DE LA CLASE ACCION
        self.symbol = symbol
        self.data = None
        self.precio_promedio_semana = None
        self.precio_actual = None
        self.porcentaje_diferencia = None

    def obtener_datos_diarios(self, start_date, end_date): #METODO PARA OBTENER DATOS DURANTE EL PLAZO DE DIAS QUE SE ESTIPULE
        try:
            self.data = yf.download(self.symbol, start=start_date, end=end_date)
        except Exception as e:
            print(f"Error al obtener datos para {self.symbol}: {e}")

    def calcular_precio_promedio(self):  #CALCULA EL PROMEDIO SEMANAL (EN ESTE CASO) DEL PRECIO DE LA ACCION
        if self.data is not None and not self.data.empty:
            self.precio_promedio_semana = self.data['Close'].mean()
        else:
            self.precio_promedio_semana = None

    def obtener_precio_actual(self): #OBTIENE EL PRECIO ACTUAL CONTRA EL CUAL SE VA A COMPARAR EL PROMEDIO
        try:
            ticker = yf.Ticker(self.symbol)
            self.precio_actual = ticker.history(period='1d')['Close'].iloc[-1]
        except Exception as e:
            print(f"Error al obtener el precio actual para {self.symbol}: {e}")
            self.precio_actual = None

    def comparar_precios(self): # SI EL PRECIO ACTUAL ES MENOR AL SEMANAL, CALCULA EL PROCETAJE DE DIFERENCIA ENTRE EL PRECIO ACTUAL Y EL PROMEDIO SEMANAL
        if self.precio_promedio_semana is not None and self.precio_actual is not None:
            if self.precio_actual < self.precio_promedio_semana:
                self.porcentaje_diferencia = ((self.precio_promedio_semana - self.precio_actual) / self.precio_promedio_semana) * 100
                return [self.symbol, self.precio_actual, self.precio_promedio_semana, self.porcentaje_diferencia]
        return None

class GestorAcciones:
    def __init__(self, symbols):
        self.acciones = [Accion(symbol) for symbol in symbols]

    def procesar_acciones(self):
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
        resultados = []

        for accion in self.acciones:
            accion.obtener_datos_diarios(start_date, end_date)
            accion.calcular_precio_promedio()
            accion.obtener_precio_actual()
            resultado = accion.comparar_precios()
            if resultado:
                resultados.append(resultado)

        return resultados

def main(): #DEFINIMOS QUE ACCIONES VAMOS A ANALIZAR
    symbols = ['AGRO.BA', 'ALUA.BA', 'AUSO.BA', 'BBAR.BA', 'BHIP.BA', 'BMA.BA', 'BOLT.BA', 'BPAT.BA', 'BYMA.BA', 'CADO.BA',
                'CAPX.BA', 'CARC.BA', 'CECO2.BA', 'CELU.BA', 'CEPU.BA', 'CGPA2.BA', 'COME.BA', 'CRES.BA', 'CVH.BA', 'CTIO.BA',
                'DGCU2.BA', 'DOME.BA', 'DYCA.BA', 'EDN.BA', 'FERR.BA', 'FIPL.BA', 'GAMI.BA', 'GARO.BA', 'GBAN.BA', 'GCDI.BA',
                'GCLA.BA', 'GGAL.BA', 'GRIM.BA', 'HARG.BA', 'HAVA.BA', 'INTR.BA', 'INVJ.BA', 'IRSA.BA', 'LEDE.BA', 'LONG.BA',
                'LOMA.BA', 'METR.BA', 'MIRG.BA', 'MOLA.BA', 'MOLI.BA', 'MORI.BA', 'OEST.BA', 'PAMP.BA', 'PATA.BA', 'POLL.BA',
                'RIGO.BA', 'ROSE.BA', 'SAMI.BA', 'SEMI.BA', 'SUPV.BA', 'Teco2.BA', 'TGNO4.BA', 'TGSU2.BA', 'TRAN.BA',
                'TXAR.BA', 'VALO.BA', 'YPFD.BA']

    gestor_acciones = GestorAcciones(symbols)
    resultados = gestor_acciones.procesar_acciones()

    if resultados: 
        headers = ["Símbolo", "Precio Actual", "Precio Promedio Semanal", "Porcentaje de Diferencia"]
        print("\nAcciones por debajo del promedio:")
        resultados = sorted(resultados, key=lambda x: x[3], reverse=True)
        print(tabulate(resultados, headers=headers, tablefmt="grid"))
        table_html = tabulate(resultados, headers=headers, tablefmt="html")
        
        # Marcar el inicio y fin del contenido que debe actualizarse
        start_marker = '<!-- Inicio Tabla de Resultados -->'
        end_marker = '<!-- Fin Tabla de Resultados -->'
        
        # Leer el contenido actual de informe.html
        with open('informe.html', 'r') as file:
            informe_content = file.read()

        # Reemplazar el contenido entre los marcadores
        new_content = f'{start_marker}\n{table_html}\n{end_marker}'
        updated_content = informe_content.split(start_marker)[0] + new_content + informe_content.split(end_marker)[1]

        # Guardar el contenido actualizado de nuevo en informe.html
        with open('informe.html', 'w') as file:
            file.write(updated_content)
        # Seleccionar las 5 acciones con mayor baja
        top_5_bajas = resultados[:5]
        
        # Graficar las 5 acciones con mayor baja
        plt.figure(figsize=(14, 7))
        
        for accion in top_5_bajas:
            symbol = accion[0]
            # Agregar el porcentaje de diferencia al gráfico
            plt.bar(symbol, accion[3])
        
        plt.xlabel('Símbolo de la Acción')  # Establece la etiqueta del eje X
        plt.ylabel('Porcentaje de Diferencia')  # Establece la etiqueta del eje Y
        plt.title('Acciones con Mayor Baja en la Última Semana')  # Establece el título del gráfico
        plt.grid(True)  # Activa la cuadrícula en el gráfico
        plt.savefig("img/grafico_acciones.png") #se guarda el gráfico como una imagen
        plt.show()  # Muestra el gráfico
        
        
    else:
        print("\nNo hay acciones por debajo del promedio esta semana.")

if __name__ == "__main__":
    main()