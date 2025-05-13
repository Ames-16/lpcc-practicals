import sys

optab = ["STOP", "ADD", "SUB", "MULT", "MOVER", "MOVEM", "COMP", "BC", "DIV", "READ", "PRINT"]
regtab = ["AREG", "BREG", "CREG", "DREG"]
adtab = ["START", "END", "ORIGIN", "EQU", "LTORG"]
dltab = ["DS", "DC"]
cctab = ["EQ", "LT", "GT", "LE", "GE", "NE"]


symbol_table = []
symbol_count = 0
literal_table = []
lit_count = 0
pool_table = []
pool_count = 0
current_pool = {
    'pool_num': 1,
    'literals': [],  # List of literals in current pool
    'start_addr': 0  # Will be set when pool is processed
}

#--------------Symbol Table----------------------

def search_op(s):
    return optab.index(s.upper())

def search_reg(s):
    return regtab.index(s.upper())
    
def search_ad(s):
    return adtab.index(s.upper())

def search_dl(s):
    return dltab.index(s.upper())

def search_cc(s):
    return cctab.index(s.upper())
    

def add_symb(s, a, v, l):
    global symbol_count
    symbol_count += 1
    symbol_table.append({
        'symb': s,
        'pos': symbol_count,
        'addr': a,
        'val': v,
        'len': l
    })

def search_symb(s):
    for entry in symbol_table:
        if entry['symb'] == s:
            return entry
    return None

def display_symbtab():
    print("#\tSymbol\tAddress\tValue\tLength")
    for entry in symbol_table:
        print(f"{entry['pos']}\t{entry['symb']}\t{entry['addr']}\t{entry['val']}\t{entry['len']}")

#--------------Literal Table----------------------

def add_literal(lit_value):
    global lit_count
    # lit_value = int(lit_value.strip("'\""))
    
    # Check if literal already exists
    for entry in literal_table:
        if entry['value'] == lit_value:
            return entry['pos']
    
    # Add new literal
    lit_count += 1
    literal_table.append({
        'pos': lit_count,
        'value': lit_value,
        'address': 0  # Will be filled during second pass
    })
    

def search_literal(value):
    for entry in literal_table:
        if entry['value'] == value:
            return entry
    return None

def display_littab():
    print("\nLiteral Table:")
    print("#\tValue\tAddress")
    for entry in literal_table:
        print(f"{entry['pos']}) \t{entry['value']}\t{entry['address']}")


#------------------Pool table----------------------

def add_to_pool(literal):
    current_pool['literals'].append(literal)

def create_new_pool():
    global pool_count, current_pool
    
    if current_pool['literals']:  # Only add non-empty pools
        pool_count += 1
        pool_table.append({
            'pool_num': pool_count,
            'literals': current_pool['literals'],
            'start_addr': 0  # Will be set during address assignment
        })
    
    # Initialize new current pool
    current_pool = {
        'pool_num': pool_count + 1,
        'literals': [],
        'start_addr': 0
    }

def assign_pool_addresses(start_addr):
    current_addr = start_addr
    for pool in pool_table:
        pool['start_addr'] = current_addr
        for lit in pool['literals']:
            # Update literal address in literal table
            lit_entry = search_literal(lit)
            if lit_entry:
                lit_entry['address'] = current_addr
            current_addr += 1

def display_pooltab():
    print("\nPool Table:")
    print("Pool\tStart Address\tStart Literal")
    for pool in pool_table:
        # start_literal = pool['literals'][0]
        # print(f"{pool['pool_num']}\t{pool['start_addr']}\t\t{start_literal}")
        literals_str = ", ".join(str(lit) for lit in pool['literals'])
        print(f"{pool['pool_num']}\t{pool['start_addr']}\t\t{literals_str}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <source_file>")
        sys.exit(1)
    
    source_filename = sys.argv[1]
    temp_filename = "temp.i"
    pc = 0

    with open(source_filename, 'r') as sf, open(temp_filename, 'w') as tf:
        for line in sf:
            line = line.strip()
            if not line:
                continue
            tokens = line.split()
            n = len(tokens)
            t1 = t2 = t3 = t4 = ''
            if n >= 1:
                t1 = tokens[0]
            if n >= 2:
                t2 = tokens[1]
            if n >= 3:
                t3 = tokens[2]
            if n >= 4:
                t4 = tokens[3]

            #Case: 1 token
            if n == 1:
                if t1 in optab:
                    if (op_idx := search_op(t1)) == 0:        #STOP
                        tf.write(f"{pc:03d}) (IS, {op_idx:02d})\n")
                elif t1 in adtab:
                    if (ad_idx := search_ad(t1)) == 0:          #START
                        tf.write(f"{pc:03d}) (AD, {ad_idx + 1:02d}) (C, 0)\n")
                    elif ad_idx != -1:                          #Not END
                            tf.write(f"{pc:03d}) (AD, {ad_idx + 1:02d})\n")

            #Case: 2 tokens
            elif n == 2:
                if t1 in optab:
                    op_idx = search_op(t1)
                    if op_idx in [9, 10]:
                        s = t2
                        p = search_symb(s)
                        if p is None:
                            add_symb(s, 0, 0, 0)
                            sym_pos = symbol_count
                        else:
                            sym_pos = p['pos']
                        tf.write(f"{pc:03d}) (IS, {op_idx:02d}) (S, {sym_pos})\n")
                    else:
                        s = t1
                        p = search_symb(s)
                        if p is None:
                            add_symb(s, pc, 0, 0)
                        else:
                            p['addr'] = pc
                        tf.write(f"{pc:03d}) (IS, 00)\n")
                else:
                    ad_idx = search_ad(t1)
                    if ad_idx != -1:
                        if ad_idx == 0:
                            new_pc = int(t2) - 1
                            tf.write(f"{pc:03d}) (AD, {ad_idx + 1:02d}) (C, {t2})\n")
                            pc = new_pc
                        else:
                            tf.write(f"{pc:03d}) (AD, {ad_idx + 1:02d})\n")

            #Case: 3 tokens
            elif n == 3:
                if t2 in dltab:                     #If DL statement
                    dl_idx = search_dl(t2)
                    if dl_idx == 0:
                        s = t1
                        value = int(t3)
                        p = search_symb(s)
                        if p is None:
                            add_symb(s, pc, 0, value)
                        else:
                            p['addr'] = pc
                            p['val'] = 0
                            p['len'] = value
                        tf.write(f"{pc:03d}) (DL, {dl_idx + 1:02d}) (C, {t3})\n")
                        pc += value - 1
                    elif dl_idx == 1:
                        s = t1
                        value = int(t3.strip("'\""))
                        p = search_symb(s)
                        if p is None:
                            add_symb(s, pc, value, 1)
                        else:
                            p['addr'] = pc
                            p['val'] = value
                            p['len'] = 1
                        tf.write(f"{pc:03d}) (DL, {dl_idx + 1:02d}) (C, {value})\n")
                
                else:                               
                    if t1 in optab:                 #If IS statement
                        op_idx = search_op(t1)
                        if 1 <= op_idx <= 8:
                            reg_part = t2.rstrip(',')

                            if op_idx == 7:
                                cc_idx = search_cc(reg_part)
                                reg_idx = cc_idx + 1
                            else:
                                reg_idx = search_reg(reg_part)

                            if t3.startswith('='):  # Handle literal
                                lit_value = t3
                                lit_pos = add_literal(lit_value)
                                add_to_pool(lit_value)  # Add to current pool
                                tf.write(f"{pc:03d}) (IS, {op_idx:02d}) ({reg_idx + 1}) (L, {lit_pos})\n")
                            else:
                                s = t3
                                p = search_symb(s)
                                if p is None:
                                    add_symb(s, 0, 0, 0)
                                    sym_pos = symbol_count
                                else:
                                    sym_pos = p['pos']
                            tf.write(f"{pc:03d}) (IS, {op_idx:02d}) ({reg_idx + 1}) (S, {sym_pos})\n")
                        else:
                            op_idx = search_op(t2)
                            s = t1
                            p = search_symb(s)
                            if p is None:
                                add_symb(s, pc, 0, 0)
                            else:
                                p['addr'] = pc
                            s = t3
                            p = search_symb(s)
                            if p is None:
                                add_symb(s, 0, 0, 0)
                                sym_pos = symbol_count
                            else:
                                sym_pos = p['pos']
                            tf.write(f"{pc:03d}) (IS, {op_idx:02d}) (S, {sym_pos})\n")

            elif n >= 4:
                op_idx = search_op(t2)
                reg_part = t3.rstrip(',')
                reg_idx = search_reg(reg_part)
                s = t1
                p = search_symb(s)
                if p is None:
                    add_symb(s, pc, 0, 0)
                else:
                    p['addr'] = pc
                
                if t4.startswith('='):  # Handle literal
                    lit_value = t4
                    lit_pos = add_literal(lit_value)
                    add_to_pool(lit_value)  # Add to current pool
                    tf.write(f"{pc:03d}) (IS, {op_idx:02d}) ({reg_idx + 1}) (L, {lit_pos})\n")
                else:
                    s = t4
                    p = search_symb(s)
                    if p is None:
                        add_symb(s, 0, 0, 0)
                        sym_pos = symbol_count
                    else:
                        sym_pos = p['pos']
                tf.write(f"{pc:03d}) (IS, {op_idx:02d}) ({reg_idx + 1}) (S, {sym_pos})\n")
            pc += 1

            # Add pool handling after processing each line
            if t1 == "LTORG" or t1 == "END":
                # Process current pool
                assign_pool_addresses(pc)
                if t1 == "LTORG":
                    create_new_pool()  # Start new pool after LTORG
                elif t1 == "END":
                    create_new_pool()  # Final pool

    with open(temp_filename, 'r') as tf:
        print(tf.read(), end='')

    display_symbtab()
    display_littab()
    display_pooltab()

if __name__ == "__main__":
    main()