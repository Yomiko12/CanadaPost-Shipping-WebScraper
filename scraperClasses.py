class Item:
	productName = ''
	length = 0
	width = 0
	height = 0
	weight = 0
	def __init__(self, name, l, w, h, wt):
		self.productName = name
		self.length = l
		self.width = w
		self.height = h
		self.weight = wt

class Province:
	provinceName = ''
	postalCode = ''
	def __init__(self, name, postal):
		self.provinceName = name
		self.postalCode = postal

class priceInfo:
	productName = ''
	locationName = ''
	shippingPrice = 0
	def __init__(self, pName, lName, sPrice):
		self.productName = pName
		self.locationName = lName
		self.shippingPrice = sPrice