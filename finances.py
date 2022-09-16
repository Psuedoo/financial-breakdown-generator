from mdutils.mdutils import MdUtils

class Income:
    def __init__(self, label: str, amount: int):
        self.label = label
        self.amount = amount


class Bill:
    def __init__(self, label: str, amount: int):
        self.label = label
        self.amount = amount


class Budget:
    def __init__(self, label: str, percentage: int, amount: int = 0):
        self.label = label
        self.percentage = percentage
        self.amount = amount


class Finances:
    def __init__(self, bills: list, incomes: list, budgets: list):
        self.bills = bills
        self.incomes = incomes
        self.bill_total = 0
        self.income_total = 0
        self.set_totals()
        self.budgets = budgets
        self.set_budgets()

    def __str__(self):
        return (
            f"Total bill amount: {self.bill_total}\n"
            f"Total income amount: {self.income_total}\n"
        )

    def set_totals(self):
        for bill in self.bills:
            self.bill_total += bill.amount

        for income in self.incomes:
            self.income_total += income.amount

    def set_budgets(self):
        budget_percentage_total = 0
        for budget in self.budgets:
            budget_percentage_total += budget.percentage

        if budget_percentage_total > 100:
            print("Your budget totals are impossible lol")
        else:
            for budget in self.budgets:
                budget.amount = (budget.percentage / 100) * self.income_total

    def generate_budget_table_text(self):
        headers = ["Label", "Percentage", "Amount"]

        for budget in self.budgets:
            headers.extend(
                [str(budget.label), str(budget.percentage), "$" + str(budget.amount)]
            )

        return headers

    def generate_bill_table_text(self):
        headers = ["Label", "Amount"]

        for bill in self.bills:
            headers.extend([str(bill.label), "$" + str(bill.amount)])

        return headers

    def generate_income_table_text(self):
        headers = ["Label", "Amount"]

        for income in self.incomes:
            headers.extend([str(income.label), "$" + str(income.amount)])

        return headers

    def generate_current_situation_text(self):
        headers = [
            "Label",
            "Target Percentage",
            "Actual Percentage",
            "Actual Amount",
            "Safe Amount",
            "Health",
        ]

        needs = self.bill_total
        needs_percentage = round((self.bill_total / self.income_total) * 100, 2)

        if needs_percentage > 50:
            needs_health = "Unhealthy"
            wants_health = "Unhealthy"
            savings_health = "Unhealthy"
        else:
            needs_health = "Healthy"
            wants_health = "Health"
            savings_health = "Health"

        needs_actual_amount = round((needs_percentage / 100) * self.income_total, 2)
        needs_safe_amount = round(0.5 * self.income_total, 2)

        headers.extend(
            [
                "Needs",
                str(50) + "%",
                str(needs_percentage) + "%",
                "$" + str(needs_actual_amount),
                "$" + str(needs_safe_amount),
                needs_health,
            ]
        )

        savings_amount = self.income_total * 0.2
        wants_amount = self.income_total - (savings_amount + needs_actual_amount)
        wants_actual_percentage = round(100 / (self.income_total / wants_amount))

        headers.extend(
            [
                "Wants",
                str(30) + "%",
                str(wants_actual_percentage) + "%",
                "$" + str(round(wants_amount, 2)),
                "$" + str(self.income_total * 0.3),
                wants_health,
            ]
        )

        headers.extend(
            [
                "Savings",
                str(20) + "%",
                str(20) + "%",
                "$" + str(savings_amount),
                "$" + str(savings_amount),
                savings_health,
            ]
        )

        return headers

    def generate_md(self, filename: str = "Finances Breakdown"):

        file = MdUtils(file_name=filename, title="Finances Breakdown")

        file.new_header(1, "Budgets")
        file.new_table(
            columns=3,
            rows=len(self.budgets) + 1,
            text=self.generate_budget_table_text(),
            text_align="center",
        )

        file.new_header(1, "Bills")
        file.new_table(
            columns=2,
            rows=len(self.bills) + 1,
            text=self.generate_bill_table_text(),
            text_align="center",
        )
        file.write(f"\nTotal: ${self.bill_total}\n")

        file.new_header(1, "Incomes")
        file.new_table(
            columns=2,
            rows=len(self.incomes) + 1,
            text=self.generate_income_table_text(),
            text_align="center",
        )
        file.write(f"\nTotal: ${self.income_total}\n")

        file.new_header(1, "Current Financial Situation")
        file.new_table(
            columns=6,
            rows=4,
            text=self.generate_current_situation_text(),
            text_align="center",
        )

        file.create_md_file()
