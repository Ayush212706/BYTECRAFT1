def disassemble(code):
    rows = ["ADDR   INSTRUCTION          ARG"]
    for address, instruction in enumerate(code):
        arg = "" if instruction.arg is None else repr(instruction.arg)
        rows.append(f"{address:04}   {instruction.op.name:<20} {arg}")
    return "\n".join(rows)
