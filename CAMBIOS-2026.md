# Cambios de la rama `update-2026`

> Esta rama es el mismo curso —Trading Algorítmico de la A a la Z con Python—, con el código adaptado a
> las librerías de hoy (**yfinance 1.7, pandas 3.0, matplotlib 3.11**, octubre de 2026). La rama
> principal sigue exactamente como en el vídeo.
> Todos los notebooks de los capítulos 1 a 8 se han ejecutado de principio a fin con esas versiones.
> Yahoo Finance no era accesible desde el entorno de prueba, así que se usó una copia fiel de su
> respuesta con precios inventados: el código está comprobado; **tus números saldrán distintos** a los
> del vídeo, porque los precios de verdad han seguido moviéndose desde que se grabó.
> En noviembre de 2026 se corrigieron además errores del propio código del curso, que dan resultados
> distintos a los del vídeo: ver [Correcciones de errores del curso](#correcciones-de-errores-del-curso-noviembre-de-2026).

## Cómo usarla

> **Qué está comprobado y qué no.** Comprobado: que cada celda de los capítulos 1 a 8 se ejecuta sin
> error con las versiones de `requirements.txt` y que los datos tienen la forma del vídeo (histórico
> completo, mismas columnas en el mismo orden). **No comprobado:** la descarga real desde Yahoo, que no
> era accesible desde el entorno de prueba; se usó una réplica de su respuesta con precios inventados.

- **En Google Colab (como en el vídeo):** abre el notebook de esta rama y, cuando el código lea un CSV
  (`EURUSD_D1.csv`, `assets.csv`…), súbelo al panel de archivos igual que en el vídeo.
- **En tu ordenador:** `git clone -b update-2026 https://github.com/joanby/trading-algoritmico-a-z-con-python`,
  instala `pip install -r requirements.txt` (versiones **fijadas**: las mismas con las que se ha
  comprobado, para que un cambio futuro de las librerías no vuelva a romperlo) y copia junto al notebook los CSV que use (están en
  `FOREX D1/`, `FOREX M1/` y `CRYPTO H1/`).

## Qué ha cambiado y por qué

### 1. Descargar precios con yfinance (capítulos 3 a 8)

yfinance cambió tres comportamientos por defecto de `yf.download` y el código del vídeo deja de
funcionar, a veces sin dar error:

| En el vídeo | Hoy, si no dices nada | Qué pasa con el código del curso |
|---|---|---|
| Sin fechas, descarga **todo el histórico** | Descarga **solo el último mes** | Medias de 60 días vacías, `.loc["2020"]` da `KeyError` |
| Con solo `end="2021-01-01"`, desde el principio hasta esa fecha | **Solo el mes anterior** a esa fecha | Sortino y backtests calculados sobre un mes, sin ningún error |
| Columnas `Open, High, Low, Close, Adj Close, Volume` | Sin `Adj Close` (`auto_adjust=True`) | `KeyError: 'Adj Close'` y *Length mismatch* al renombrar |
| Columnas simples, en ese orden | Columnas de dos niveles (precio, ticker) y en **orden alfabético** | Aunque arregles lo anterior, al renombrar por posición `open` acabaría siendo `Adj Close` |

(Comprobado leyendo yfinance 0.1.70, la versión de cuando se grabó, y la 1.7.0 de hoy.
`yf.Ticker(...).history()` no ha cambiado: ya ajustaba los precios y bajaba un mes por defecto.)

Los dobles corchetes de `df[["Close"]].rolling(15).mean()` **no son un fallo**: funcionan igual en
pandas 3. No hace falta cambiarlos.

Por eso cada `yf.download(...)` lleva ahora tres argumentos que devuelven el comportamiento del vídeo:

```python
yf.download("EURUSD=X", period="max", auto_adjust=False, multi_level_index=False)
```

`period="max"` se añade siempre que la llamada no tenga fecha de inicio (`start`). Y donde el código renombra las columnas
por posición (`df.columns = ["open", "high", ...]`), se reordenan antes como estaban:
`[["Open", "High", "Low", "Close", "Adj Close", "Volume"]]`.

**Si escribes el código siguiendo el vídeo**, añade esos argumentos en tu `yf.download`.

### 2. pandas 3: `fillna(method="ffill")` ya no existe (capítulo 6)

Se escribe `.ffill()` (y `.bfill()` para `method="bfill"`). Hace exactamente lo mismo.

### 3. matplotlib: el estilo `seaborn` cambió de nombre (capítulos 7 y 8)

`plt.style.use('seaborn')` → `plt.style.use('seaborn-v0_8')`. Es el mismo estilo de gráficos.

### 4. Rutas de Colab

`pd.read_csv("/content/EURUSD_D1.csv")` → `pd.read_csv("EURUSD_D1.csv")`. En Colab es lo mismo (la
carpeta de trabajo es `/content`) y además funciona en tu ordenador.

### 5. Errores que el vídeo provoca a propósito

En el capítulo 1 hay una celda que da `NameError` para enseñar qué es una variable local. Sigue dando
el error; solo se ha marcado (etiqueta `raises-exception`) para que *Ejecutar todo* no se pare ahí.

## Lo que no se ha tocado

- **El capítulo 9 (MetaTrader 5)**: la librería `MetaTrader5` solo funciona en Windows con MetaTrader 5
  instalado y una cuenta, así que **no se ha podido ejecutar aquí**. Cambios, sin ejecutar: los dos
  notebooks importaban `Chapter_09_MT5`, pero el fichero del repositorio se llama
  `Capitulo_09_MT5.py`; ahora importan `Capitulo_09_MT5`. Y los de noviembre de 2026 (abajo, punto 5).
- `mpl_finance` (velas japonesas del capítulo 6) está abandonada pero **sigue instalándose y
  funcionando**; su sucesora es `mplfinance`. Necesita `six`, que no declara: por eso está en
  `requirements.txt` (ver abajo).
- Avisos amarillos que puedes ver y no rompen nada: el de `mpl_finance`, el de *Could not infer format*
  al leer los CSV por minutos y el de *X does not have valid feature names* de scikit-learn.

## Correcciones de errores del curso (noviembre de 2026)

Aquí no ha cambiado ninguna librería: son fallos del código del curso que enseñaban algo mal. **Lo que
verás en pantalla será distinto del vídeo**, y está explicado en cada punto. Comprobado: los capítulos 1
a 8 se han vuelto a ejecutar enteros con `requirements.txt` y la réplica de Yahoo de arriba (todos sin error). Las cifras de antes y
después de los capítulos 6 y 8 bis salen de los CSV del repositorio. Las del capítulo 5 salen de Yahoo
Finance real, descargado el 19 de noviembre de 2026. El capítulo 9 **no se ha ejecutado**.
Los notebooks conservan la salida guardada del vídeo: en las celdas de estos puntos, lo guardado es el
resultado antiguo (por ejemplo, `Alpha: 0.9 %`); al ejecutarlas, sale el nuevo.

### 0. `requirements.txt`: falta `six` (capítulo 6)

Desde el 1 de noviembre de 2026, una instalación limpia con `pip install -r requirements.txt` hacía
fallar el capítulo 6 con `ModuleNotFoundError: No module named 'six'`. `mpl_finance` usa `six` pero no
la declara, y hasta entonces llegaba de rebote con `python-dateutil`, que en su versión 4.0 ha dejado de
necesitarla. Ahora `six` está fijada en `requirements.txt`.

### 1. Alfa (capítulo 5)

**En el vídeo:** alfa se calcula como `252 * mean * (1-beta)` (celda 13) y, dentro de `BackTest`, como
`serie.mean() - beta*serie.mean()`. Sale un 0,9 % para Google.

**Qué estaba mal:** las dos expresiones son el retorno medio de la cartera multiplicado por (1 − beta).
Ahí no aparece el mercado, así que no dicen si la cartera lo ha hecho mejor que él, y el signo puede salir
al revés que el real. La fórmula escrita en la celda 12 tenía el mismo fallo.

**Ahora:** es el alfa de Jensen, con tipo libre de riesgo cero: el retorno medio de la cartera menos beta
por el retorno medio del SP500, anualizado igual que antes.

```python
alpha = (252 * (mean - beta*val["SP500"].mean()))*100                        # celda 13
alpha = annualiazed_scalar * (serie.mean() - beta*val["SP500"].mean())       # BackTest
```

La fórmula de la celda 12 pasa a ser $r_{PF} - r_f - \beta (r_M - r_f)$. `BackTest` se llama igual y
recibe lo mismo.

**Qué cambia en los números:** Google (2004–2020, beta 0,965) pasa de un **0,9 %** a un **17,2 %**
anual. En una prueba con datos inventados de beta 1,2 y un alfa real de +5 % al año, el cálculo antiguo
daba **−1,6 %** y el nuevo da **+5,0 %**. Y alfa no mide seguridad: en el vídeo, un 0,9 % se lee como
«Google es una acción un 0,9 % más segura». En realidad, alfa es la rentabilidad que se obtiene por
encima de la que tocaría por el riesgo de mercado asumido (beta).

### 2. `preprocessing_yf` descargaba siempre EURUSD (capítulo 5)

**Qué estaba mal:** recibe `symbol`, pero descargaba siempre `"EURUSD=X"`. Con cualquier otro símbolo
devolvía EURUSD sin avisar.

**Ahora:** `yf.download(symbol, ...)`, como la `preprocessing_yf` de los capítulos 3 y 4.

**Qué cambia en los números:** nada en el notebook, que la llama con `"EURUSD=X"`. Cambia si la usas
con otro activo.

### 3. `support_resistance` no restaba el spread (capítulo 6)

**En el vídeo:** se añade el parámetro `spread` para que, «cada vez que colocáis una orden de compra o
de venta», se reste ese coste. Luego se aplica a seis pares de divisas con `spread=0.0001`.

**Qué estaba mal:** se restaba solo en las filas en las que `df["return"]` valía exactamente 1 o −1. Es
un rendimiento, del orden de 0,0001: no vale ±1 nunca, así que el coste **no se restaba nunca**. Daba lo
mismo pasar `spread=0` que `spread=0.0001`.

**Ahora:** se resta en cada operación. Es decir, en las filas en las que la posición,
`df["signal"].shift(duration)`, vale 1 o −1.

```python
df.loc[df["signal"].shift(duration)==-1, "return"] = df["return"]-spread
df.loc[df["signal"].shift(duration)==1, "return"] = df["return"]-spread
```

**Qué cambia en los números:** mucho. Con estos datos, la estrategia hace **entre 12.700 y 14.400
operaciones por par**. A 0,0001 cada una, son entre 1,3 y 1,4 puntos menos de rentabilidad acumulada por par. La
tabla final (`RETURN`, `DRAWDOWN`, `RETURN DRAWDOWN RATIO`) queda así:

| | RETURN antes | RETURN ahora | RATIO antes | RATIO ahora |
|---|---|---|---|---|
| GBPUSD | 0,149 | −0,701 | 4,34 | −0,97 |
| cartera | 0,075 | −0,943 | 4,24 | −1,00 |
| AUDCAD | 0,189 | −0,690 | 3,62 | −1,00 |
| EURUSD | 0,103 | −1,316 | 1,45 | −1,00 |
| USDCHF | 0,040 | −1,234 | 0,77 | −1,00 |
| USDJPY | 0,009 | −0,873 | 0,14 | −1,00 |
| USDCAD | −0,040 | −0,845 | −0,46 | −1,00 |

El ratio que en el vídeo «llega a superar el 4» sale de no contar el coste. Con el coste, todos los pares
pierden. Esa es la lección: en *scalping*, con miles de operaciones, el spread decide el resultado.

### 4. La estrategia del capítulo 8 bis se evaluaba con los datos de entrenamiento

**En el vídeo:** `lin_reg_trading` devuelve la estrategia de todo el periodo, y la curva de ETH se
presenta como «una estrategia muy muy muy segura».

**Qué estaba mal:** el modelo se entrena con el primer 80 % de los datos y la curva incluía ese
tramo. Es el error que el propio vídeo del capítulo 8 avisa de no cometer: «para ser realistas tendríamos
que representar únicamente [...] el conjunto de testing».

**Ahora:** devuelve solo el periodo de test, `dfc["strategy"].iloc[split:]`. El modelo se entrena igual.

**Qué cambia en los números** (suma acumulada, como en el notebook):

| | Antes (train + test) | Ahora (solo test) |
|---|---|---|
| ETHUSD | 24.949 horas, 2018-07 → 2022-03, **3,73** | 4.990 horas, 2021-07 → 2022-03, **0,59** |
| BTCUSD | 35.303 horas, 2011-03 → 2022-03, 11,10 | 7.061 horas, 2021-04 → 2022-03, 0,08 |
| Cartera BTC + ETH | 2,70 · retorno/drawdown 9,64 | −0,06 · retorno/drawdown −0,15 |

En el tramo que el modelo no ha visto, ETH gana y la cartera de los dos pierde un poco.

### 5. Capítulo 9: instalación y etiqueta (sin ejecutar)

- **Celda 0 de los dos notebooks:** se han comentado `numpy==1.19.2` y `scipy==1.6.2`, que no se
  instalan en un Python actual: numpy 1.19.2 solo trae instaladores hasta Python 3.8, y scipy 1.6.2 no
  admite Python 3.10 o posterior (en 3.12, pip intenta compilar numpy y falla). También se ha comentado `pip install datetime`: `datetime` viene con Python, y en
  PyPI ese nombre es otro paquete. `numpy` se sigue instalando, porque la piden `ta` y `MetaTrader5`. Si
  instalas en un entorno virtual, quita también `--user`, que ahí da error.
- **Notebook SMA:** la orden se llamaba `"Bitcoin"`, pero opera `EURUSD` con 1 lote. Ahora se llama
  `"Euro vs US dollar"`, como en el notebook Random. El símbolo y el volumen no cambian.
- **Avisos, sin cambiar el código:** hay un comentario en `filling_mode - 1` (`Capitulo_09_MT5.py`) y
  otro en los `while True`. `filling_mode` es una máscara de bits del broker: restarle 1 solo acierta si el
  símbolo admite un único modo de ejecución, y si no, la orden puede rechazarse. El bucle no tiene
  ninguna pausa: repite la ronda durante todo el segundo de arranque y luego da vueltas sin parar. Opera
  siempre en una **cuenta demo**, y empieza con `live = False`.

## Erratas del vídeo (el código no cambia)

- **«Funciones: variable local».** Se dice que lo mismo pasa con las variables definidas dentro de un `if`
  o de un `for`. En Python no es así: `if` y `for` no crean un ámbito nuevo, solo las funciones. Una
  variable creada dentro de un `if` o de un `for` sigue existiendo después.
- **pandas (capítulo 2).** `rolling(15)` usa la fila actual y las 14 anteriores, no «los 15 valores
  anteriores». Y en `reset_index(drop=True)`, `drop=True` descarta el índice viejo en vez de convertirlo
  en columna: no elimina valores ausentes.
- **RSI (capítulos 6 y 7).** El vídeo dice que cerca de 100 es momento de comprar y cerca de 0 de vender.
  La lectura habitual es la contraria: por encima de 70 hay sobrecompra y por debajo de 30, sobreventa. El
  código del curso no usa esos niveles: en el capítulo 6 compara el RSI con el del periodo anterior, y en
  los capítulos 7 y 8 es solo una variable más del modelo. Por eso no cambia ningún resultado.
- **Capítulo 8 bis.** Se dice que ETH acaba en un «38 %» y la cartera en un «28 %». Con los CSV del
  repositorio, la suma acumulada de todo el periodo da 3,73 y 2,70, es decir, ≈ 373 % y ≈ 270 % (el
  gráfico no multiplica por 100). Ahora el notebook enseña solo el periodo de test (punto 4).
- **Tráiler.** Se habla de una plantilla para «sacar el rendimiento desde el minuto 0». El curso enseña a
  construir estrategias y a evaluarlas con datos pasados. Ninguna garantiza rentabilidad, y los puntos 3
  y 4 de esta misma lista lo demuestran.
