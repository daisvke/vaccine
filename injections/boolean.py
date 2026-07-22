from core.requester import Requester
from core.analyzer import Analyzer
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
			{ param: ctx.prefix + "AND 1=1" + ctx.suffix }
		)

		r_false = self.requester.send(
			url,
			{ param: ctx.prefix + "AND 1=2" + ctx.suffix }
		)

		return self.analyzer.responses_differ(r_true, r_false, differ_length_bool)
