
class User:

    def __init__(self) -> None:
        self.user_data = ("Ali is a 55 year old man who has a wife and a kid they are all on his healthcare plan. "
                          "His kid has glasses that are $150. "
                          "His wife broke her leg and went to urgent care in network which cost $1007.45. "
                          "The xray for the leg was $150. "
                          "Ali had in network outpatient surgery for his heart that cost $6350.23. "
                          "Ali takes preferred brand drug perscription heart medication that cost $432.38. "
                          "Ali's family is covered by the silver plan.")    
        
    def get_user_data(self):
        return self.user_data
