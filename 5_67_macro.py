class MacroProcessor:
    def __init__(self):
        # Macro Name Table (MNT) - stores macro names and their positions in MDT
        self.macro_name_table = {}  # {macro_name: mdt_index}
        
        # Macro Definition Table (MDT) - stores macro definitions
        self.macro_def_table = []  # List of macro definitions
        
        # Argument List Array (ALA) - stores formal and actual parameters
        self.ala = {}  # {macro_name: {'formal': [...], 'actual': [...]}}
        
        self.intermediate_code = []

    def first_pass(self, source_code):
        """First pass: Process macro definitions and build tables"""
        lines = source_code.split('\n')
        i = 0
        mdt_index = 0

        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith('MACRO'):
                # Extract macro name and parameters
                parts = line.split()
                macro_name = parts[1]
                if len(parts) > 2:
                    # Get parameters and remove trailing commas
                    formal_params = [p.rstrip(',') for p in parts[2:]]
                else:
                    formal_params = ['-']
                
                # Add to Macro Name Table
                self.macro_name_table[macro_name] = mdt_index
                
                # Initialize ALA for this macro
                self.ala[macro_name] = {
                    'formal': formal_params,
                    'actual': []
                }
                
                # Add macro definition to MDT
                macro_def = {
                    'name': macro_name,
                    'params': formal_params,
                    'body': []
                }
                
                # Collect macro body until MEND
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('MEND'):
                    macro_def['body'].append(lines[i])
                    i += 1
                
                self.macro_def_table.append(macro_def)
                mdt_index += 1
            
            i += 1

    def expand_macro(self, macro_name, actual_params):
        """Expand a macro call using MDT and ALA"""
        # Get macro definition from MDT using MNT
        mdt_index = self.macro_name_table[macro_name]
        macro_def = self.macro_def_table[mdt_index]
        
        # Update ALA with actual parameters
        self.ala[macro_name]['actual'] = actual_params
        
        # Create parameter mapping using ALA
        param_map = dict(zip(
            self.ala[macro_name]['formal'],
            self.ala[macro_name]['actual']
        ))
        
        # Expand macro body with arguments
        expanded_code = []
        for line in macro_def['body']:
            expanded_line = line
            for formal, actual in param_map.items():
                expanded_line = expanded_line.replace(formal, actual)
            expanded_code.append(expanded_line)
        
        return expanded_code

    def second_pass(self, source_code):
        """Second pass: Expand macro calls using tables"""
        lines = source_code.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip macro definitions and MEND
            if line.startswith('MACRO') or line.startswith('MEND'):
                i += 1
                continue
            
            # Check for macro call
            parts = line.split()
            if parts and parts[0] in self.macro_name_table:
                macro_name = parts[0]
                actual_params = [p.rstrip(',') for p in parts[1:]]
                
                # Expand macro call using tables
                expanded_code = self.expand_macro(macro_name, actual_params)
                self.intermediate_code.extend(expanded_code)
            else:
                self.intermediate_code.append(line)
            
            i += 1

    def process(self, source_code):
        """Process the source code through both passes"""
        self.first_pass(source_code)
        self.second_pass(source_code)
        return '\n'.join(self.intermediate_code)

    def print_tables(self):
        # Print Macro Name Table (MNT)
        print("\nMacro Name Table (MNT)")
        print("Name".ljust(15) + "MDT Index".ljust(10))
        for name, index in self.macro_name_table.items():
            print(f"{name.ljust(15)}{str(index).ljust(10)}")


        # Print Macro Definition Table (MDT)
        print("\nMacro Definition Table (MDT)")
        print("MDT Index".ljust(10) + "Parameters".ljust(20) + "Macro Body")
        for i, macro in enumerate(self.macro_def_table):
            params_str = ", ".join(macro['params'])
            indent = " "*30
            body_lines = [line.strip() for line in macro['body']]
            body_str = "\n" + indent + ("\n" + indent).join(body_lines)
            
            print(f"{str(i).ljust(10)}{params_str.ljust(20)}{body_str}")

        # Print Argument List Array (ALA)
        print("\nArgument List Array (ALA)")
        print("Macro Name".ljust(15) + "Formal Parameters".ljust(25) + "Actual Parameters")
        for macro_name, params in self.ala.items():
            formal_str = ", ".join(params['formal'])
            actual_str = ", ".join(params['actual'])
            print(f"{macro_name.ljust(15)}{formal_str.ljust(25)}{actual_str}")


def main():
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python macro.py <input_file> <output_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Read source code from input file
    with open(input_file, 'r') as file:
        source_code = file.read()

    # Process the source code
    processor = MacroProcessor()
    intermediate_code = processor.process(source_code)
    
    # Print tables for verification
    processor.print_tables()
    
    # Write intermediate code to output file
    with open(output_file, 'w') as file:
        file.write(intermediate_code)
    print(f"\nIntermediate code has been written to '{output_file}'")

if __name__ == "__main__":
    main()
