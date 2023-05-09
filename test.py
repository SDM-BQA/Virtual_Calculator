myEquation = '5+6+'  # incorrect equation
try:
    result = eval(myEquation)
    print(result)
except (SyntaxError, NameError):
    print("Invalid equation")
