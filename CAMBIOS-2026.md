# Cambios de la rama `update-2026`

> Esta rama es el mismo curso —Trading Algorítmico de la A a la Z con Python—, con el código adaptado a
> las librerías de hoy (**yfinance 1.7, pandas 3.0, matplotlib 3.11**, octubre de 2026). La rama
> principal sigue exactamente como en el vídeo.
> Todos los notebooks de los capítulos 1 a 8 se han ejecutado de principio a fin con esas versiones.
> Yahoo Finance no era accesible desde el entorno de prueba, así que se usó una copia fiel de su
> respuesta con precios inventados: el código está comprobado; **tus números saldrán distintos** a los
> del vídeo, porque los precios de verdad han seguido moviéndose desde que se grabó.

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

`period="max"` solo se añade cuando la llamada no tenía fechas. Y donde el código renombra las columnas
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
  instalado y una cuenta, así que **no se ha podido ejecutar aquí**. Un único cambio, sin ejecutar: los dos
  notebooks importaban `Chapter_09_MT5`, pero el fichero del repositorio se llama
  `Capitulo_09_MT5.py`; ahora importan `Capitulo_09_MT5`.
- `mpl_finance` (velas japonesas del capítulo 6) está abandonada pero **sigue instalándose y
  funcionando**; su sucesora es `mplfinance`.
- Avisos amarillos que puedes ver y no rompen nada: el de `mpl_finance`, el de *Could not infer format*
  al leer los CSV por minutos y el de *X does not have valid feature names* de scikit-learn.
