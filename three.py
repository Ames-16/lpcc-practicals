class ExpressionParser:
    def __init__(self):
        self.temp_count = 0
        self.three_address_code = []
    
    def new_temp(self):
        """Generate a new temporary variable name"""
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp
    
    def parse_expression(self, expr):
            """
            Recursive descent parser for expressions
            Handles:
            - Addition and subtraction (lowest precedence)
            - Multiplication and division (middle precedence)
            - Exponentiation (higher precedence)
            - Parentheses (highest precedence)
            - Variables and constants
            
            Returns:
                tuple: (result identifier, list of three-address code instructions)
            """
            expr = expr.strip()
            
            # Look for addition or subtraction (lowest precedence)
            parentheses_level = 0
            for i in range(len(expr) - 1, -1, -1):  # Scan right to left
                if expr[i] == ')':
                    parentheses_level += 1
                elif expr[i] == '(':
                    parentheses_level -= 1
                
                if parentheses_level == 0 and expr[i] in '+-' and i > 0:
                    # Make sure it's not a unary operator
                    if i == 0 or expr[i-1] in '+-*/^(':
                        continue
                    
                    left, _ = self.parse_expression(expr[:i])
                    right, _ = self.parse_expression(expr[i+1:])
                    temp = self.new_temp()
                    self.three_address_code.append(f"{temp} = {left} {expr[i]} {right}")
                    return temp, self.three_address_code
            
            # Look for multiplication or division (middle precedence)
            parentheses_level = 0
            for i in range(len(expr) - 1, -1, -1):  # Scan right to left
                if expr[i] == ')':
                    parentheses_level += 1
                elif expr[i] == '(':
                    parentheses_level -= 1
                
                if parentheses_level == 0 and expr[i] in '*/':
                    left, _ = self.parse_expression(expr[:i])
                    right, _ = self.parse_expression(expr[i+1:])
                    temp = self.new_temp()
                    self.three_address_code.append(f"{temp} = {left} {expr[i]} {right}")
                    return temp, self.three_address_code
            
            # Look for exponentiation (higher precedence)
            parentheses_level = 0
            for i in range(len(expr) - 1, -1, -1):  # Scan right to left
                if expr[i] == ')':
                    parentheses_level += 1
                elif expr[i] == '(':
                    parentheses_level -= 1
                
                if parentheses_level == 0 and expr[i] == '^':
                    left, _ = self.parse_expression(expr[:i])
                    right, _ = self.parse_expression(expr[i+1:])
                    temp = self.new_temp()
                    self.three_address_code.append(f"{temp} = {left} ^ {right}")
                    return temp, self.three_address_code
            
            # Check for parentheses
            if expr.startswith('(') and expr.endswith(')'):
                # Make sure the outer parentheses match
                parentheses_level = 0
                for i in range(len(expr)):
                    if expr[i] == '(':
                        parentheses_level += 1
                    elif expr[i] == ')':
                        parentheses_level -= 1
                    
                    if parentheses_level == 0 and i < len(expr) - 1:
                        # The outer parentheses don't match
                        break
                else:
                    # The outer parentheses match, so remove them
                    return self.parse_expression(expr[1:-1])
            
            # Handle unary operators
            if expr.startswith('+'):
                operand, _ = self.parse_expression(expr[1:])
                return operand, self.three_address_code
            elif expr.startswith('-'):
                operand, _ = self.parse_expression(expr[1:])
                temp = self.new_temp()
                self.three_address_code.append(f"{temp} = - {operand}")
                return temp, self.three_address_code
            
            # It's a variable or constant
            return expr.strip(), self.three_address_code
        


def generate_three_address_code(expression):
    """
    Generate three-address code for the given expression
    
    Args:
        expression (str): Mathematical expression to convert
    
    Returns:
        list: List of three-address code instructions
    """
    parser = ExpressionParser()
    result, code = parser.parse_expression(expression)
    
    # Add assignment to the final variable if needed
    if result not in ["t" + str(parser.temp_count - 1), "t0"]:
        final_temp = parser.new_temp()
        code.append(f"{final_temp} = {result}")
    
    return code


# Example usage
if __name__ == "__main__":
    expr = input("Enter expression: ")
    code = generate_three_address_code(expr)
    for line in code:
        print(line)