from mdutils.mdutils import MdUtils
from data import budgets, incomes, bills
from finances import Finances


finances = Finances(bills=bills, incomes=incomes, budgets=budgets)
finances.generate_md()
print("Generated your financial breakdown")
