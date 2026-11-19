import warnings
from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
warnings.filterwarnings("ignore")
mt5.initialize()


class MT5:

   def get_data(symbol, n, timeframe=mt5.TIMEFRAME_D1):
        """ Función para importar los datos del símbolo elegido"""

        # Inicializamos la conexión si no estaba activa
        mt5.initialize()

        # Current date extract
        utc_from = datetime.now()

        # Import the data into a tuple
        rates = mt5.copy_rates_from(symbol, timeframe, utc_from, n)

        # Tuple to dataframe
        rates_frame = pd.DataFrame(rates)

        # Convert time in seconds into the datetime format
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

        # Convert the column "time" in the right format
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], format='%Y-%m-%d')

        # Set column time as the index of the dataframe
        rates_frame = rates_frame.set_index('time')
        return rates_frame

   def orders(symbol, lot, buy=True, id_position=None):
       """ Enviamos las órdenes """

        # Inicializamos la conexión si no estaba activa
       if mt5.initialize() == False:
           mt5.initialize()

       # Get filling mode 
       filling_mode = mt5.symbol_info(symbol).filling_mode - 1  # ojo: según el broker puede no valer (ver CAMBIOS-2026.md)

       # Take ask price
       ask_price = mt5.symbol_info_tick(symbol).ask

       # Take bid price
       bid_price = mt5.symbol_info_tick(symbol).bid

       # Take the point of the asset
       point = mt5.symbol_info(symbol).point

       deviation = 20  # mt5.getSlippage(symbol)
       # **************************** Open a trade *****************************
       if id_position == None:

           # Buy order Parameters
           if buy:
               type_trade = mt5.ORDER_TYPE_BUY
               sl = ask_price*(1-0.01)
               tp = ask_price*(1+0.01)
               price = ask_price

           # Sell order Parameters
           else:
               type_trade = mt5.ORDER_TYPE_SELL
               sl = bid_price*(1+0.01)
               tp = bid_price*(1-0.01)
               price = bid_price

           # Open the trade
           request = {
               "action": mt5.TRADE_ACTION_DEAL,
               "symbol": symbol,
               "volume": lot,
               "type": type_trade,
               "price": price,
               "deviation": deviation,
               "sl": sl,
               "tp": tp,
               "magic": 234000,
               "comment": "python script order",
               "type_time": mt5.ORDER_TIME_GTC,
               "type_filling": filling_mode,
           }
           # send a trading request
           result = mt5.order_send(request)
           result_comment = result.comment

       # **************************** Close a trade *****************************
       else:
           # Buy order Parameters
           if buy:
               type_trade = mt5.ORDER_TYPE_SELL
               price = bid_price

           # Sell order Parameters
           else:
               type_trade = mt5.ORDER_TYPE_BUY
               price = ask_price

           # Close the trade
           request = {
               "action": mt5.TRADE_ACTION_DEAL,
               "symbol": symbol,
               "volume": lot,
               "type": type_trade,
               "position": id_position,
               "price": price,
               "deviation": deviation,
               "magic": 234000,
               "comment": "python script order",
               "type_time": mt5.ORDER_TIME_GTC,
               "type_filling": filling_mode,
           }

           # send a trading request
           result = mt5.order_send(request)
           result_comment = result.comment
       return result.comment

   def resume():
      """ Return the current positions. Position=0 --> Buy """
      # Initialize the connection if there is not
      mt5.initialize()

      # Define the name of the columns that we will create
      columns = ["ticket", "position", "symbol", "volume"]

      # Go take the current open trades
      current = mt5.positions_get()

      # Create a empty dataframe
      summary = pd.DataFrame()

      # Loop to add each row in dataframe
      # (Can be ameliorate using of list of list)
      for element in current:
           element_pandas = pd.DataFrame([element.ticket,
                                          element.type,
                                          element.symbol,
                                          element.volume],
                                         index=columns).transpose()
           summary = pd.concat((summary, element_pandas), axis=0)

      return summary


   def run(symbol, long, short, lot):

        # Inicializamos la conexión si no estaba activa
        if mt5.initialize() == False:
            mt5.initialize()

        # Choose your  symbol
        print("------------------------------------------------------------------")
        print("Date: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("SYMBOL:", symbol)

        # Initialize the device
        current_open_positions = MT5.resume()
        # Buy or sell
        print(f"BUY: {long} \t  SHORT: {short}")

        """ Close trade eventually """
        # Extraction type trade
        try:
            position = current_open_positions.loc[current_open_positions["symbol"]==symbol].values[0][1]

            identifier = current_open_positions.loc[current_open_positions["symbol"]==symbol].values[0][0]
        except:
            position= None
            identifier = None

        print(f"POSITION: {position} \t ID: {identifier}")

        # Close trades
        if long==True and position==0:
            long=False

        elif long==False and position==0:
            res = MT5.orders(symbol, lot, buy=True, id_position=identifier)
            print(f"CLOSE LONG TRADE: {res}")

        elif short==True and position ==1:
            short=False

        elif short == False and position == 1:
            res = MT5.orders(symbol, lot, buy=False, id_position=identifier)
            print(f"CLOSE SHORT TRADE: {res}")

        else:
            pass


        """ Buy or short """
        if long==True:

            res = MT5.orders(symbol, lot, buy=True, id_position=None)
            print(f"OPEN LONG TRADE: {res}")

        if short==True:
            res = MT5.orders(symbol, lot, buy=False, id_position=None)
            print(f"OPEN SHORT TRADE: {res}")

        print("------------------------------------------------------------------")

   def close_all_night():
        result = MT5.resume()
        for i in range(len(result)):
            before =  mt5.account_info().balance
            row = result.iloc[0+i:1+i,:]
            if row["position"][0]==0:
                res = MT5.orders(row["symbol"][0], row["volume"][0], buy=True, id_position=row["ticket"][0])

            else:
                res = MT5.orders(row["symbol"][0], row["volume"][0], buy=False, id_position=row["ticket"][0])