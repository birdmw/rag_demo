
class User:

    def __init__(self) -> None:
        self.user_data = """Ali is a 55 year old man who has a wife and a kid they are all on his healthcare plan
                            he has already paid $1567.63 so far for his deductible
                            his kid has glasses that are $150
                            his wife broke her leg and went to urgent care in network which cost $1007.45
                            the xray for the leg was $150
                            Ali had in network outpatient surgery for his heart that cost $6350.23
                            Ali takes preferred brand drug perscription heart medication they cost $432.38"""
        

    def get_user_data(self):
        return self.user_data