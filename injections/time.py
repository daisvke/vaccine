from core.analyzer import Analyzer
from core.requester import Requester
from utils.constants import InjectionContext

class TimeInjector:
	"""
	Detects time-based SQL injection vulnerabilities.

	These vulnerabilities are identified by measuring whether an injected
	delay function causes the database to respond significantly slower.
	"""

	def __init__(self, requester: Requester, analyzer: Analyzer):
		self.requester = requester
		self.analyzer = analyzer

	def test(
     	self,
      	url: str,
		param: str,
  		ctx: InjectionContext,
    	sleep: int = 1
	) -> bool:
		"""
		Test for time-based SQL injection.

		A normal request is compared against a request containing a delay
		function. If the second response takes significantly longer,
		the parameter is likely injectable.
		"""

		r_normal = self.requester.send(
			url,
			{param: ctx.prefix + "AND 1=1" + ctx.suffix}
		)

		r_sleep = self.requester.send(
			url,
			{param: f"{ctx.prefix}AND SLEEP({sleep}){ctx.suffix}"}
		)

		return self.analyzer.is_delayed(r_normal, r_sleep, sleep)
