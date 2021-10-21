import alpaca_trade_api as tradeapi

class AlpacaPaperMoneyBot(object):
	def __init__(self, symbol):
		#NOT GOOD PRACTICE 
		self.key = 'PKIZA7TT6UT9ONDBDUAX'
		self.secret = 'mhtVuLxYF3uSnNr6Q98DtYF3ihPgZnVyaWoprG9F'
		self.alpaca_endpoint = 'https://paper-api.alpaca.markets'
		#NOT GOOD PRACTICE 
		self.api = tradeapi.REST(self.key, self.secret, self.alpaca_endpoint)
		self.symbol = symbol
		self.current_order = None
		self.last_price = 1

		try:
			self.position = int(self.api.get_position(self,symbol).qty)
		except:
			self.position = 0

	def submit_order(self, target):
		if self.current_order is not None:
			self.api.cancel_order(self.current_order.id)

		delta = target - self.position
		if delta == 0:
			return
		print(f'Processing the order for {target} shares')

		if delta > 0:
			buy_quantity = delta
			if self.position < 0:
				buy_quantity = min(abs(self.position), buy_quantity)
			print(f'Buying {buy_quantity} shares of {self.symbol}')
			self.current_order = self.api.submit_order(self.symbol, buy_quantity, 'buy', 'limit', 'day', self.last_price)

		elif delta < 0:
				sell_quantity = abs(delta)
				if self.position > 0:
					sell_quantity = min(abs(self.position), sell_quantity)
				print(f'Selling {sell_quantity} shares of {self.symbol}')
				self.current_order = self.api.submit_order(self.symbol, sell_quantity, 'sell', 'limit', 'day', self.last_price)

if __name__ == '__main__':
	ticker = input('What stock would you like execute the trading algorithim on? ')
	quantity = input('How many shares would you like to trade? ')
	bot = AlpacaPaperMoneyBot(ticker)
	bot.submit_order(int(quantity))


