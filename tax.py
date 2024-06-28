import solara
from utils import *
import pandas as pd
import plotly.graph_objects as go
import pygwalker as pyg
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

class Income:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Income, cls).__new__(cls)
            cls._instance.period = solara.reactive("Monthly")
            cls._instance.period_multiplier = solara.reactive(12)
            cls._instance.total_income = solara.reactive(0)
            cls._instance.basic_pay = solara.reactive(0)

            # HRA
            cls._instance.hra_received = solara.reactive(0)
            cls._instance.city_type = solara.reactive("Non Metro City")
            cls._instance.rent_paid = solara.reactive(0)
            cls._instance.basic_pay_city_dependent_percentage = solara.reactive(40)
            cls._instance.basic_pay_city_dependent_percentage_amount = solara.reactive(0)
            cls._instance.rent_paid_excess_to_basic_10_percentage = solara.reactive(0)
            cls._instance.exempted_hra = solara.reactive(0)
            cls._instance.max_rent_to_be_paid = solara.reactive(0)

            # 80C components
            cls._instance.pf_amount = solara.reactive(0)
            cls._instance.ppf_amount = solara.reactive(0)
            cls._instance.term_insurance_amount = solara.reactive(0)
            cls._instance.ells_amount = solara.reactive(0)
            cls._instance.total_80_deduction = solara.reactive(0)

            # deductions and tax regime
            cls._instance.total_deductions = solara.reactive(0)
            cls._instance.standard_deductions = solara.reactive(50000)
            cls._instance.old_regime_taxable_income = solara.reactive(0)
            cls._instance.old_regime_tax_amount = solara.reactive(0)
            cls._instance.new_regime_taxable_income = solara.reactive(0)
            cls._instance.new_regime_tax_amount = solara.reactive(0)

        return cls._instance

    def __init__(self):
        pass

    def __str__(self):
        return f"Income - total_income: {self.total_income.value}, basic_pay: {self.basic_pay.value}, hra_received: {self.hra_received.value}"

    def __repr__(self):
        return f"Income - total_income: {self.total_income.value}, basic_pay: {self.basic_pay.value}, hra_received: {self.hra_received.value}"


    def reset(self):
        self.period.value = "Monthly"
        self.period_multiplier.value = 12
        self.total_income.value = 0
        self.basic_pay.value = 0

        # HRA
        self.hra_received.value = 0
        self.city_type.value = "Non Metro City"
        self.rent_paid.value = 0
        self.basic_pay_city_dependent_percentage.value = 40
        self.basic_pay_city_dependent_percentage_amount.value = 0
        self.rent_paid_excess_to_basic_10_percentage.value = 0
        self.exempted_hra.value = 0
        self.max_rent_to_be_paid.value = 0

        # 80C components 
        self.pf_amount.value = 0
        self.ppf_amount.value = 0
        self.term_insurance_amount.value = 0
        self.ells_amount.value = 0
        self.total_80_deduction.value = 0

        # deductions and tax regime
        self.total_deductions.value = 0
        self.standard_deductions.value = 50000
        self.old_regime_taxable_income.value = 0
        self.old_regime_tax_amount.value = 0
        self.new_regime_taxable_income.value = 0
        self.new_regime_tax_amount.value = 0

    def update_basic_pay(self, val):
        self.basic_pay.value = val
        self.basic_pay_city_dependent_percentage_amount.value = round(self.basic_pay.value*(self.basic_pay_city_dependent_percentage.value/100))
        self.rent_paid_excess_to_basic_10_percentage.value = round(self.rent_paid.value-(self.basic_pay.value*0.1))
        self.rent_paid_excess_to_basic_10_percentage.value = max(0, self.rent_paid_excess_to_basic_10_percentage.value)
        self.exempted_hra.value = min(self.hra_received.value, self.basic_pay_city_dependent_percentage_amount.value, self.rent_paid_excess_to_basic_10_percentage.value)
        self.exempted_hra.value = max(0, self.exempted_hra.value)
        self.max_rent_to_be_paid.value = round(self.hra_received.value + (self.basic_pay.value*0.1))

    def update_hra_received(self, val):
        self.hra_received.value = val
        self.basic_pay_city_dependent_percentage_amount.value = round(self.basic_pay.value*(self.basic_pay_city_dependent_percentage.value/100))
        self.rent_paid_excess_to_basic_10_percentage.value = round(self.rent_paid.value-(self.basic_pay.value*0.1))
        self.rent_paid_excess_to_basic_10_percentage.value = max(0, self.rent_paid_excess_to_basic_10_percentage.value)
        self.exempted_hra.value = min(self.hra_received.value, self.basic_pay_city_dependent_percentage_amount.value, self.rent_paid_excess_to_basic_10_percentage.value)
        self.exempted_hra.value = max(0, self.exempted_hra.value)
        self.max_rent_to_be_paid.value = round(self.hra_received.value + (self.basic_pay.value*0.1))

    def update_rent_paid(self, val):
        self.rent_paid.value = val
        self.basic_pay_city_dependent_percentage_amount.value = round(self.basic_pay.value*(self.basic_pay_city_dependent_percentage.value/100))
        self.rent_paid_excess_to_basic_10_percentage.value = round(self.rent_paid.value-(self.basic_pay.value*0.1))
        self.rent_paid_excess_to_basic_10_percentage.value = max(0, self.rent_paid_excess_to_basic_10_percentage.value)
        self.exempted_hra.value = min(self.hra_received.value, self.basic_pay_city_dependent_percentage_amount.value, self.rent_paid_excess_to_basic_10_percentage.value)
        self.exempted_hra.value = max(0, self.exempted_hra.value)
        self.max_rent_to_be_paid.value = round(self.hra_received.value + (self.basic_pay.value*0.1))

    def update_city_type(self, val):
        self.city_type.value = val
        if self.city_type.value == "Metro City":
            self.basic_pay_city_dependent_percentage.value = 50
        else:
            self.basic_pay_city_dependent_percentage.value = 40
        self.basic_pay_city_dependent_percentage_amount.value = round(self.basic_pay.value*(self.basic_pay_city_dependent_percentage.value/100))


    def update_period(self, val):
        # self.reset()
        self.period.value = val

        if self.period.value == "Monthly":
            self.period_multiplier.value = 12
        else:
            self.period_multiplier.value = 1


    def display_tax_regime_pie_chart(self):
        # Prepare data for the old tax regime pie chart
        old_labels = ['Tax', 'Non-Taxable']
        old_values = [self.old_regime_tax_amount.value, (self.total_income.value * self.period_multiplier.value) - self.old_regime_tax_amount.value]

        # Prepare data for the new tax regime pie chart
        new_labels = ['Tax', 'Non-Taxable']
        new_values = [self.new_regime_tax_amount.value, (self.total_income.value * self.period_multiplier.value) - self.new_regime_tax_amount.value]

        # Create subplots
        fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

        # Add old tax regime pie chart
        fig.add_trace(go.Pie(labels=old_labels, values=old_values, hole=0.4, textinfo='percent', textposition='inside', name='Old Regime'), row=1, col=1)

        # Add new tax regime pie chart
        fig.add_trace(go.Pie(labels=new_labels, values=new_values, hole=0.4, textinfo='percent', textposition='inside', name='New Regime'), row=1, col=2)

        # Add annotations for each pie chart
        fig.update_layout(
            annotations=[
                dict(text='Old', x=0.20, y=0.5, font_size=15, showarrow=False),
                dict(text='New', x=0.80, y=0.5, font_size=15, showarrow=False)
            ]
        )

        # Show the plot
        solara.FigurePlotly(fig)



    def consol(self):
        with solara.Card(style= {"textAlign":"center", "border": f'1px solid' },elevation=5):
            with solara.Column(align="center", margin=0):
                solara.Markdown("## Taxation")
                solara.ToggleButtonsSingle(value=self.period, values=["Monthly", "Annual"],on_value=self.update_period)

                with solara.Card(style={"width": "100%"}):
                    with solara.Columns():
                        solara.Markdown(f"#### {self.period.value} Total Income :")
                        solara.InputInt("", value=self.total_income)

                        solara.Markdown(f"#### {self.period.value} Basic Income :")
                        solara.InputInt("", value=self.basic_pay, on_value=self.update_basic_pay)

                        solara.Markdown(f"#### {self.period.value} HRA Received :")
                        solara.InputInt("", value=self.hra_received, on_value=self.update_hra_received)
                
                # if self.total_income.value > 0 and self.basic_pay.value > 0 and self.hra_received.value > 0:
                with solara.Columns(style={"width": "100%"}):
                    self.hra_exemptions()
                    self.deductions()


                with solara.Card(style={"width": "100%"}):
                    with solara.Columns():
                        self.old_regime()
                        self.display_tax_regime_pie_chart()
                        self.new_regime()

    def hra_exemptions(self):
        with solara.Card():
            solara.Markdown(f"### {self.period.value} HRA Exemption")
            with solara.Column():
                with solara.Columns():
                    solara.Markdown(f"#### {self.period.value} Rent Paid :")
                    solara.InputInt("", value=self.rent_paid, on_value=self.update_rent_paid)

                with solara.Columns([1,10,1]):
                    solara.Text("")
                    solara.Select(label="", value=self.city_type, values=["Non Metro City","Metro City"], on_value=self.update_city_type)
                    solara.Text("")

                with solara.Columns():
                    solara.Markdown(f"#### {self.basic_pay_city_dependent_percentage.value}% of Basic Salary :")
                    solara.InputInt("", value=self.basic_pay_city_dependent_percentage_amount.value, disabled=True)
                
                with solara.Columns():
                    solara.Markdown(f"#### Excess of Rent paid over 10% of salary :")
                    solara.InputInt("", value=self.rent_paid_excess_to_basic_10_percentage.value, disabled=True)

                with solara.Columns():
                    solara.Markdown(f"####  Amount of Exempted HRA	 :")
                    solara.InputInt("", value=self.exempted_hra.value, disabled=True)

                if self.rent_paid.value == 0:
                    if self.basic_pay.value > 0 and self.hra_received.value > 0:
                        solara.Warning(f"{self.max_rent_to_be_paid.value} Rs in {self.period.value} Rent should be Paid to Avail Max HRA Benefit !!!!", outlined=False,  icon=False)
                    else:
                        solara.Info(f"Add some rent to avail HRA Benefit !!!", outlined=False,  icon=False)
                else:
                    if self.max_rent_to_be_paid.value <= self.rent_paid.value:
                        solara.Success(f"You are Availing Max HRA Benefit !!!", outlined=False,  icon=False)
                    else:
                        solara.Warning(f"{self.max_rent_to_be_paid.value} Rs in {self.period.value} Rent should be Paid to Avail Max HRA Benefit !!!!", outlined=False,  icon=False)


    def deductions(self):
        with solara.Card():
            solara.Markdown(f"### Annual 80C Deductions")

            with solara.Column():
                with solara.Columns():
                    solara.Markdown(f"#### Provident Fund :")
                    solara.InputInt("", value=self.pf_amount)

            with solara.Column():
                with solara.Columns():
                    solara.Markdown(f"#### Public Provident Fund :")
                    solara.InputInt("", value=self.ppf_amount)

            with solara.Column():
                with solara.Columns():
                    solara.Markdown(f"#### Term Insurance Policy :")
                    solara.InputInt("", value=self.term_insurance_amount)
            with solara.Column():
                with solara.Columns():
                    solara.Markdown(f"#### ELLS :")
                    solara.InputInt("", value=self.ells_amount)

            self.total_80_deduction.value = self.pf_amount.value + self.ppf_amount.value + self.term_insurance_amount.value + self.ells_amount.value

            with solara.Column():
                with solara.Columns():
                    solara.Markdown(f"#### Total Contribution :",)
                    solara.InputInt("", value=self.total_80_deduction.value, disabled=True)

            with solara.Column():
                if self.total_80_deduction.value >= 150000:
                    solara.Success(f"You are Availing Max Limit (1,50,000 Rs) of 80C !!!", outlined=False,  icon=False)
                else:
                    solara.Warning(f"You Should Invest {150000-self.total_80_deduction.value} Rs more to get Max Benefit !!!", outlined=False,  icon=False)


    def old_regime(self):
        with solara.Column(style={"width": "100%"}):
            solara.Markdown(f"### Old Regime")
            self.total_deductions.value = (self.exempted_hra.value * self.period_multiplier.value) + min(self.total_80_deduction.value,150000) + self.standard_deductions.value
            self.old_regime_taxable_income.value = (self.total_income.value * self.period_multiplier.value) - self.total_deductions.value
            self.old_regime_taxable_income.value = max(0, self.old_regime_taxable_income.value)

            slabes = []
            tax_amount = 0
            previous_amount = 0
            slabes.append(["Tax Slab 1", "Upto Rs.2,50,000 - No Tax", tax_amount, tax_amount+previous_amount])

            previous_amount = round(tax_amount + previous_amount)
            if self.old_regime_taxable_income.value > 250000:
                tax_amount = min(self.old_regime_taxable_income.value - 250000, 250000) * 0.05
            slabes.append(["Tax Slab 2", "Rs.2,50,001Rs - Rs.5,00,000 @ 5%", tax_amount, tax_amount+previous_amount])

            previous_amount = round(tax_amount + previous_amount)
            if self.old_regime_taxable_income.value > 500000:
                tax_amount = min(self.old_regime_taxable_income.value - 500000, 500000) * 0.20
            slabes.append(["Tax Slab 3", "5,00,001 - 10,00,000 @ 20%", tax_amount, tax_amount+previous_amount])

            previous_amount = round(tax_amount + previous_amount)
            if self.old_regime_taxable_income.value > 1000000:
                tax_amount = (self.old_regime_taxable_income.value - 1000000) * 0.30
            slabes.append(["Tax Slab 4", "Above 10,00,001 @ 30%", tax_amount, tax_amount+previous_amount])

            previous_amount = round(tax_amount + previous_amount)
            tax_amount = previous_amount * 0.04
            slabes.append([" ", "Cess @ 4%", tax_amount, tax_amount+previous_amount])

            self.old_regime_tax_amount.value = round(tax_amount + previous_amount)
            df = pd.DataFrame(slabes, columns=["Slab", "Tax Rate", "Tax Amount", "Cumulative Tax Amount"])
            solara.Markdown(df.to_markdown(index=False) ,style={"textAlign": "center"})
            solara.Markdown(f"#### Taxable Income : {self.old_regime_taxable_income.value}")
            solara.Markdown(f"### Tax Paid : {self.old_regime_tax_amount.value}")

    def new_regime(self):
        with solara.Column(style={"width": "100%"}):
            solara.Markdown(f"### New Regime")
            self.new_regime_taxable_income.value = (self.total_income.value * self.period_multiplier.value)


            slabes = []
            tax_amount = 0
            previous_amount = 0
            slabes.append(["Tax Slab 1", "Upto Rs.2,50,000 - No Tax", tax_amount, tax_amount+previous_amount])

            previous_amount = round(tax_amount + previous_amount)
            if self.new_regime_taxable_income.value > 250000:
                tax_amount = min(self.new_regime_taxable_income.value - 250000, 250000) * 0.05
            slabes.append(["Tax Slab 2", "Rs.2,50,001Rs - Rs.5,00,000 @ 5%", tax_amount, tax_amount+previous_amount])

            previous_amount = round(tax_amount + previous_amount)
            if self.new_regime_taxable_income.value > 500000:
                tax_amount = min(self.new_regime_taxable_income.value - 500000, 250000) * 0.10
            slabes.append(["Tax Slab 3", "5,00,001 - 7,50,000 @ 10%", tax_amount, tax_amount+previous_amount])

            previous_amount = round(tax_amount + previous_amount)
            if self.new_regime_taxable_income.value > 750000:
                tax_amount = min(self.new_regime_taxable_income.value - 750000, 250000) * 0.15
            slabes.append(["Tax Slab 4", "7,50,001 - 10,00,000 @ 15%", tax_amount, tax_amount+previous_amount])

            previous_amount = round(tax_amount + previous_amount)
            if self.new_regime_taxable_income.value > 1000000:
                tax_amount = min(self.new_regime_taxable_income.value - 1000000, 250000) * 0.20
            slabes.append(["Tax Slab 5", "10,00,001 - 12,50,000 @ 20%", tax_amount, tax_amount+previous_amount])

            previous_amount = round(tax_amount + previous_amount)
            if self.new_regime_taxable_income.value > 1250000:
                tax_amount = min(self.new_regime_taxable_income.value - 1250000, 250000) * 0.25
            slabes.append(["Tax Slab 6", "10,00,001 - 12,50,000 @ 20%", tax_amount, tax_amount+previous_amount])

            previous_amount = round(tax_amount + previous_amount)
            if self.new_regime_taxable_income.value > 1500000:
                tax_amount = (self.new_regime_taxable_income.value - 1500000) * 0.30
            slabes.append(["Tax Slab 7", "Above 15,00,001 @ 30%", tax_amount, tax_amount+previous_amount])

            previous_amount = round(tax_amount + previous_amount)
            tax_amount = previous_amount * 0.04
            slabes.append([" ", "Cess @ 4%", tax_amount, tax_amount+previous_amount])

            self.new_regime_tax_amount.value = round(tax_amount + previous_amount)

            df = pd.DataFrame(slabes, columns=["Slab", "Tax Rate", "Tax Amount", "Cumulative Tax Amount"])
            solara.Markdown(df.to_markdown(index=False) ,style={"textAlign": "center"})
            solara.Markdown(f"### Tax Paid : {self.new_regime_tax_amount.value}")
