from core.requester import Requester
from core.analyzer import Analyzer
from utils.constants import InjectionContext

class BooleanInjector:
	"""
	Detects Boolean-based SQL injection vulnerabilities.
	
	These vulnerabilities can allow attackers to infer database information
	by observing differences between true and false query conditions.
	"""

	def __init__(self, requester: Requester, analyzer: Analyzer):
		self.requester = requester
		self.analyzer = analyzer

	def test(self, url: str, param: dict, ctx: InjectionContext) -> bool:
		r_true = self.requester.send(
			url,
			{
				param: ctx.prefix + "AND 1=1" + ctx.suffix
			}
		)

		r_false = self.requester.send(
			url,
			{
				param: ctx.prefix + "AND 1=2" + ctx.suffix
			}
		)

		return self.analyzer.responses_differ(r_true, r_false)
