class Property:
    def __init__(self, name, location, value, risk_category, risk_score):
        self.name = name
        self.location = location
        self.value = value
        self.risk_category = risk_category
        self.risk_score = risk_score

    def __str__(self):
        return f"{self.name} ({self.location}) - Value: ${self.value:,.2f}, Risk: {self.risk_category} ({self.risk_score}/10)"

#if __name__ == "__main__":
    #test_property = Property("Warehouse A", "Chicago", 450000, "Fire", 7)
  #  print(test_property)