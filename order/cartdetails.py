from .models import ShippingMethod
import sys, datetime

class cartDetails:
	def __init__(self, scart):
		self.__cart = scart
		self.subtotal = self.__subtotal_cost()
		self.coupon_discount = self.__coupon_dis()
		self.free_ship = False
		self.ship_name = self.__ship_info()['ship_name']
		self.ship_cost = self.__ship_info()['ship_cost']
		self.totalcost = self.subtotal + self.ship_cost - self.coupon_discount
	
	def __subtotal_cost(self):
		total_cost = 0
		for item in self.__cart.carts.all():
			opt_cost = 0
			for opt in item.options.all():
				opt_cost += opt.price
			main_price = float(item.product.main_price) + float(opt_cost)
			main_price -= (( main_price * float(item.product.discount)) / 100)
			if item.product.hot_deal_end and item.product.hot_deal_end >= datetime.date.today():
				if item.product.hot_deal_discount_type == 'percentage':
					main_price -= ((main_price * item.product.hot_deal_discount) / 100)
				else:
					main_price -= item.product.hot_deal_discount
			cost = main_price * item.quantity
			total_cost += cost
		return total_cost

	def __coupon_dis(self):
		c_dis = 0
		if self.__cart.coupon.all().count() > 0:
			for coupon in self.__cart.coupon.all():
				if coupon.discount_type == 'Percent':
					c_dis += self.subtotal*coupon.value/100
				else:
					c_dis += coupon.value
		return c_dis

	def __ship_info(self):
		free_shipping = ShippingMethod.objects.filter(method_type='free').first()
		local_shipping = ShippingMethod.objects.filter(method_type='local').first()
		if self.__cart.coupon.all().count() > 0:
			for coupon in self.__cart.coupon.all():
				if coupon.free_shipping:
					self.free_ship = True
		if self.free_ship:
			if free_shipping.active:
				ship_name = free_shipping.name
				ship_cost = 0
			else:
				ship_name = 'Free Shipping'
				ship_cost = 0

		else:
			total_cost = self.subtotal - self.coupon_discount
			if free_shipping and free_shipping.active and total_cost > free_shipping.fee:
				ship_name = free_shipping.name
				ship_cost = 0
				self.free_ship = True
			elif local_shipping and local_shipping.active:
				ship_name = local_shipping.name
				ship_cost = local_shipping.fee
		return {
			'ship_name': ship_name,
			'ship_cost': ship_cost
		}

sys.path.append(".")