import time
import datetime as dt
import warnings
import mplfinance as mpf
import pandas as pd
from matplotlib import animation
from datetime import timedelta
import pandas_ta as ta
from threading import Thread
from web3 import Web3
from web3.middleware import geth_poa_middleware

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

node = 'https://bscrpc.com'
w3 = Web3(Web3.HTTPProvider(node))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

PCS_BNB_ORACLE_CONTRACT = '0x0567F2323251f0Aab15c8dFb1967E4e8A7D42aeE'
PCS_BNB_ORACLE_ABI = '[{"inputs":[{"internalType":"address","name":"_aggregator","type":"address"},{"internalType":"address","name":"_accessController","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"int256","name":"current","type":"int256"},{"indexed":true,"internalType":"uint256","name":"roundId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"updatedAt","type":"uint256"}],"name":"AnswerUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"roundId","type":"uint256"},{"indexed":true,"internalType":"address","name":"startedBy","type":"address"},{"indexed":false,"internalType":"uint256","name":"startedAt","type":"uint256"}],"name":"NewRound","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"OwnershipTransferRequested","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"acceptOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"accessController","outputs":[{"internalType":"contract AccessControllerInterface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"aggregator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_aggregator","type":"address"}],"name":"confirmAggregator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_roundId","type":"uint256"}],"name":"getAnswer","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_roundId","type":"uint256"}],"name":"getTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestAnswer","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRound","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"phaseAggregators","outputs":[{"internalType":"contract AggregatorV2V3Interface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"phaseId","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_aggregator","type":"address"}],"name":"proposeAggregator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"proposedAggregator","outputs":[{"internalType":"contract AggregatorV2V3Interface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"proposedGetRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proposedLatestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_accessController","type":"address"}],"name":"setController","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
BNB_ORACLE_CONTRACT = w3.eth.contract(address=PCS_BNB_ORACLE_CONTRACT, abi=PCS_BNB_ORACLE_ABI)


def price_updater(n):
    blank = pd.DataFrame(columns=[''])
    blank.to_csv('tick_data.csv', encoding='utf-8')

    def get_oracle_tick_data(n):
        df = pd.DataFrame(columns=['timestamp', 'price'])
        latest_round = BNB_ORACLE_CONTRACT.functions.latestRound().call()
        current_write_round = latest_round - n
        while current_write_round != latest_round:
            current_round_data = BNB_ORACLE_CONTRACT.functions.getRoundData(current_write_round).call()
            if int(current_round_data[2]) != 0:
                df.loc[len(df)] = [int(current_round_data[2]), float(current_round_data[1]) / 100000000]
                current_write_round += 1
                print(f'Downloading last {n} tick datas for technical analysis generation: {abs(current_write_round - latest_round)}/{n}      ', end='\r')
        df.to_csv('tick_data.csv', encoding='utf-8')
        return df

    def tick_data_to_ohlc(df):
        df.set_index(df['timestamp'], inplace=True)
        df.index = pd.to_datetime(df.index, unit='s')
        df = df.drop(columns=['timestamp'])
        df = df.resample('1Min').ohlc()
        df.columns = df.columns.droplevel(0)
        return df

    def check_for_tick_updates():
        df = pd.read_csv('tick_data.csv').iloc[:, 1:]
        current_round = BNB_ORACLE_CONTRACT.functions.latestRound().call()
        current_round_data = BNB_ORACLE_CONTRACT.functions.getRoundData(current_round).call()
        if df['timestamp'].iloc[-1] == current_round_data[2] and df['price'].iloc[-1] == current_round_data[1]:
            return False
        elif df['timestamp'].iloc[-1] != current_round_data[2] and df['price'].iloc[-1] != current_round_data[1] and \
                current_round_data[2] != 0:
            df.loc[len(df)] = [int(current_round_data[2]), float(current_round_data[1]) / 100000000]
            df.to_csv('tick_data.csv', encoding='utf-8')
            return True

    get_oracle_tick_data(n)
    while True:
        update = check_for_tick_updates()
        if update is True:
            candles = pd.read_csv('tick_data.csv').iloc[:, 1:]
            candles = tick_data_to_ohlc(candles)
            # candles = technical_analysis(candles)
            candles.to_csv('candle_data.csv', encoding='utf-8')
            latest_price = candles['close'].iloc[-1]
            dt_string = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f'[{dt_string}] Price update: ${latest_price}')
            # print(candles)
        time.sleep(1)


def pcs_chart(interval):
    time.sleep(3)
    while True:
        try:
            isblank = pd.read_csv('tick_data.csv')
            if len(isblank) > 0:
                isexist = pd.read_csv('candle_data.csv')
                break
            else:
                time.sleep(1)
        except FileNotFoundError:
            time.sleep(3)

    def read_candle():
        def technical_analysis(df):
            df.ta.macd(append=True)
            df.ta.stochrsi(append=True)
            df.ta.rsi(append=True)
            df.ta.ema(close=df['RSI_14'], length=14, append=True)
            df.ta.supertrend(append=True, length=10, multiplier=1)
            return df

        ohlc = {
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last'
        }

        candles = pd.read_csv('candle_data.csv', index_col='timestamp', parse_dates=True)
        # candles.ta.ha(append=True)
        # candles.drop(columns=['open', 'high', 'low', 'close'], inplace=True)
        # candles = candles.rename(
        #     columns={'HA_open': 'open', 'HA_high': 'high', 'HA_low': 'low', 'HA_close': 'close'})

        return technical_analysis(candles.resample(interval).apply(ohlc)).drop(columns=['SUPERT_10_1.0', 'SUPERTl_10_1.0', 'SUPERTs_10_1.0'])

    fig = mpf.figure()
    fig.suptitle('PancakeSwap BNBUSD Chart 1min via Oracle (Live)')
    rows = 4
    ax1 = fig.add_subplot(rows, 1, 1)
    ax2 = fig.add_subplot(rows, 1, 2)
    ax3 = fig.add_subplot(rows, 1, 3)
    # ax4 = fig.add_subplot(rows, 1, 4)
    ax5 = fig.add_subplot(rows, 1, 4)

    def chart(ival):
        candles = read_candle()
        candles_view_limit = 60
        ax1.clear()
        ax2.clear()
        ax3.clear()
        # ax4.clear()
        ax5.clear()
        mpf.plot(candles, ax=ax1, type='candle', style='charles',
                 xlim=(candles.index[-candles_view_limit], candles.index[-1] + timedelta(minutes=1)))
        price_sizes = candles['close'][(len(candles) - candles_view_limit):len(candles)]
        ax1.set_ylim(price_sizes.min() - 0.1, price_sizes.max() + 0.1)

        ax2.plot(candles['MACD_12_26_9'], color="blue")
        ax2.plot(candles['MACDs_12_26_9'], color="orange")
        for i in range(len(candles)):
            if candles['MACDh_12_26_9'][i] > 0:
                ax2.bar(candles.index[i], candles['MACDh_12_26_9'][i], bottom=0, width=0.0007, color='green')
            else:
                ax2.bar(candles.index[i], candles['MACDh_12_26_9'][i], bottom=0, width=0.0007, color='red')
        ax2.set_ylabel('MACD')
        ax2.yaxis.set_label_position("right")
        ax2.yaxis.tick_right()
        macd_sizes = candles['MACD_12_26_9'][(len(candles) - candles_view_limit):len(candles)]
        ax2.set_xlim(candles.index[-candles_view_limit], candles.index[-1] + timedelta(minutes=1))
        ax2.set_ylim(macd_sizes.min() - 0.05, macd_sizes.max() + 0.05)

        ax3.plot(candles['RSI_14'], color="red")
        ax3.plot(candles['EMA_14'], color="yellow")
        ax3.set_ylabel('RSI')
        ax3.yaxis.set_label_position("right")
        ax3.yaxis.tick_right()
        ax3.set_ylim(0, 100)
        ax3.set_xlim(candles.index[-candles_view_limit], candles.index[-1] + timedelta(minutes=1))

        # ax4.plot(candles['SUPERTd_10_1.0'])
        # ax4.set_ylabel('SuperTrend')
        # ax4.yaxis.set_label_position("right")
        # ax4.yaxis.tick_right()

        ax5.plot(candles['STOCHRSIk_14_14_3_3'], color="purple")
        ax5.plot(candles['STOCHRSId_14_14_3_3'], color="royalblue")
        ax5.set_ylabel('Stochastic RSI')
        ax5.yaxis.set_label_position("right")
        ax5.yaxis.tick_right()
        ax3.set_ylim(0, 100)
        ax5.set_xlim(candles.index[-candles_view_limit], candles.index[-1] + timedelta(minutes=1))

    chart(0)

    ani = animation.FuncAnimation(fig, chart)

    mpf.show()
    

chart_thread = Thread(target=pcs_chart, args=('1Min',), daemon=True).start()

try:
    price_updater(350)
except KeyboardInterrupt:
    print('Goodbye.')
