import yfinance as yf
from datetime import datetime, timedelta
from tabulate import tabulate
import matplotlib.pyplot as plt
plt.style.use('./estilos/mi_estilo.mplstyle')


class Accion:
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = None
        self.precio_promedio_semana = None
        self.precio_actual = None

    def obtener_datos_diarios(self, start_date, end_date):
        try:
            self.data = yf.download(self.symbol, start=start_date, end=end_date)
        except Exception as e:
            print(f"Error al obtener datos para {self.symbol}: {e}")

    def calcular_precio_promedio(self):
        if self.data is not None and not self.data.empty:
            self.precio_promedio_semana = self.data['Close'].mean()
        else:
            self.precio_promedio_semana = None

    def obtener_precio_actual(self):
        try:
            ticker = yf.Ticker(self.symbol)
            self.precio_actual = ticker.history(period='1d')['Close'].iloc[-1]
        except Exception as e:
            print(f"Error al obtener el precio actual para {self.symbol}: {e}")
            self.precio_actual = None

    def comparar_precios(self):
        if self.precio_promedio_semana is not None and self.precio_actual is not None:
            if self.precio_actual < self.precio_promedio_semana:
                porcentaje_diferencia = ((self.precio_promedio_semana - self.precio_actual) / self.precio_promedio_semana) * 100
                return [self.symbol, self.precio_actual, self.precio_promedio_semana, porcentaje_diferencia]
        return None

class GestorAcciones:
    def __init__(self, symbols):
        self.acciones = [Accion(symbol) for symbol in symbols]

    def procesar_acciones(self):
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        resultados = []

        for accion in self.acciones:
            accion.obtener_datos_diarios(start_date, end_date)
            accion.calcular_precio_promedio()
            accion.obtener_precio_actual()
            resultado = accion.comparar_precios()
            if resultado:
                resultados.append(resultado)

        return resultados

def main():
    symbols = ['AAPL.BA', 'AMZN.BA', 'AZN.BA', 'BABA.BA', 'BCS.BA', 'BRKB.BA', 'C.BA', 'COST.BA', 'CRM.BA', 'CVX.BA', 'DISN.BA', 
               'GOOGL.BA', 'HD.BA', 'HPQ.BA', 'HSBC.BA', 'JNJ.BA', 'JPM.BA','KO.BA','MCD.BA', 'MRVL.BA','MSFT.BA','NFLX.BA',
               'NVDA.BA','NVS.BA','ORAN.BA', 'ORCL.BA','PG.BA','SAN.BA','SHEL.BA','T.BA','TGT.BA','VOD.BA','WMT.BA','XOM.BA']


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
        
        # Leer el contenido actual de informe_acciones.html
        with open('informe_acciones.html', 'r') as file:
            informe_acciones_content = file.read()

        # Reemplazar el contenido entre los marcadores
        new_content = f'{start_marker}\n{table_html}\n{end_marker}'
        updated_content = informe_acciones_content.split(start_marker)[0] + new_content + informe_acciones_content.split(end_marker)[1]

        # Guardar el contenido actualizado de nuevo en informe_acciones.html
        with open('informe_acciones.html', 'w') as file:
            file.write(updated_content)
   

        # Seleccionar las 5 acciones con mayor baja
        top_5_bajas = resultados[:5]
        
        # Graficar las 5 acciones con mayor baja
        plt.figure(figsize=(14, 7))
        
        for accion in top_5_bajas:
            symbol = accion[0]
            datos_accion = yf.download(symbol, start=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'), end=datetime.now().strftime('%Y-%m-%d'))
            plt.plot(datos_accion.index, datos_accion['Close'], label=symbol)
        
        plt.xlabel('Fecha')
        plt.ylabel('Precio de Cierre')
        plt.title('Acciones con Mayor Baja en la Última Semana')
        plt.legend()
        plt.grid(True)

       #se guarda el gráfico como una imagen
        plt.savefig("img/grafico_acciones.png")

        plt.show()
    else:
        print("\nNo hay acciones por debajo del promedio esta semana.")

if __name__ == "__main__":
    main()
