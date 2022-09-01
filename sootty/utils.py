from math import ceil, log
from io import BytesIO, BufferedReader
from sootty.exceptions import SoottyError

def dec2anybase(input, base, width):
    """
    Convert a decimal into any base (2 - 36).
    Trailing zeros are added according to input value bit size (width).
    """
    res = str()
    while input > 0:
        rem = input % base
        if rem >= 0 and rem <= 9:
            res += chr(rem + ord("0"))
        else:
            res += chr(rem - 10 + ord("A"))
        input = int(input / base)
 
    return res[::-1].zfill(ceil(log(2**width - 1, base)))

def vcdid_hash(s):
    """
    Hash identifier_code into integers.
    """
    val = 0
    s_len = len(s)
    for i in reversed(range(s_len)):
        val *= 94
        val += s[i] - 32

    return val

def vcdid_unhash(value):
    """
    Unhash identifier_code from integers.
    """
    buf = str()
    while value:
        vmod = value % 94
        if vmod:
            buf += chr(vmod + 32)
        else:
            buf += '~'
            value -= 94
        value = int(value / 94)
    return buf.encode()  # bytes(buf, 'utf-8') or 'ascii'

def evcd_strcpy(src, direction):
    """
    Convert EVCD value changes into VCD input/output value changes according to direction.
    """
    evcd = b"DUNZduLHXTlh01?FAaBbCcf"
    vcdi = b"01xz01zzzzzz01xz0011xxz"  # input direction = False
    vcdo = b"zzzzzz01xz0101xz1x0x01z"  # output direction = True
    vcd = vcdo if direction else vcdi
    value = bytes()
    for vc_bit in src:
        for i in range(23):
            if evcd[i] == vc_bit:
                value += vcd[i:i+1]
                i -= 1  # choice of i can be alternative
                break
        if i == 22:
            raise SoottyError("EVCD value error: value change is invalid")
    return value

def evcd2vcd(stream):
    """
    Main function to convert EVCD input stream into VCD input stream.
    """
    buf = stream.read()
    toks = buf.split()  # compared with re.split(b'\s+', buf), this automatically strip
    tokit = iter(toks)
    vcd = BytesIO()
    vcd_ids = dict()
    try:
        scope_layer = 0
        tok = next(tokit)
        while True:
            # Basic formatter and syntax checker
            if tok == b'$comment' or tok == b'$date' or tok == b'$timescale' or tok == b'$version':
                vcd.write(tok + b' ')
                body = next(tokit)
                while body != b'$end':
                    vcd.write(body + b' ')
                    body = next(tokit)
                vcd.write(b'$end\n')  # body + \n
                tok = next(tokit)
            elif tok == b'$enddefinitions':
                if next(tokit) != b'$end':
                    raise SoottyError("EVCD syntax error: $enddefinitions not followed by $end")
                else:
                    vcd.write(b'$enddefinitions $end\n')
                    break
            elif tok == b'$scope':
                # Simply check scope, var, and upscope outside can also parse, but cannot precisely throw exceptions
                while tok == b'$scope':
                    vcd.write(b'$scope ')
                    body = next(tokit)
                    while body != b'$end':
                        vcd.write(body + b' ')
                        body = next(tokit)
                    vcd.write(b'$end\n')  # body + \n
                    scope_layer += 1
                    tok = next(tokit)
                    # Empty scope: innermost scope not followed by var_section
                    while tok == b'$var':
                        var_type = next(tokit)
                        if var_type == b'port':
                            var_size = next(tokit)
                            if var_size.startswith(b'['):  # VCS extension
                                p_hi = int(var_size[1:2])
                                p_lo = p_hi
                                p_colon = var_size.find(b':')
                                if p_colon > 0:
                                    p_lo = int(var_size[p_colon+1:p_colon+2])
                                len = p_hi - p_lo + 1 if p_hi > p_lo else p_lo - p_hi + 1
                            else:
                                len = int(var_size)
                            if len < 1:
                                raise SoottyError("EVCD value error: the size of a value must be a positive integer")
                            id_code = next(tokit)
                            if not id_code.startswith(b'<'):
                                raise SoottyError("EVCD syntax error: identifier_code not preceded by '<'")
                            hash = vcdid_hash(id_code)
                            var_ref = next(tokit)
                            if next(tokit) != b'$end':
                                raise SoottyError("EVCD syntax error: var_section reference not followed by $end")
                            else:
                                node = vcd_ids.get(hash)  # jrb_find_int(id_code, hash)
                                if node is None:
                                    vcd_ids[hash] = len
                                else:
                                    raise SoottyError("EVCD syntax error: identifier_code re-declared")
                                # var_ref containing "[" may effect: lbrack = var_ref.find(b'[')
                                # Alternatively, '%d%s%s'.format(digit, str, str).encode() is more complicated since %s needs string rather than bytes
                                # % operator to format bytes is from PEP 461
                                vcd.write(b'$var wire %d %s %s_I $end\n' % (len, vcdid_unhash(hash * 2), var_ref))
                                vcd.write(b'$var wire %d %s %s_O $end\n' % (len, vcdid_unhash(hash * 2 + 1), var_ref))
                            tok = next(tokit)
                        elif var_type == b'event' or var_type == b'integer' or var_type == b'parameter' or var_type == b'real' or var_type == b'realtime' or var_type == b'reg' or var_type == b'supply0' or var_type == b'supply1' or var_type == b'time':
                            raise SoottyError("EVCD syntax error: VCD var_type detected")
                        else:
                            raise SoottyError("EVCD syntax error: invalid var_type")
                    # There should not be any vars or anything between scopes or upscopes
                    while tok == b'$upscope':
                        if next(tokit) == b'$end':
                            vcd.write(b'$upscope $end\n')
                            scope_layer -= 1
                            tok = next(tokit)
                        else:
                            raise SoottyError("EVCD syntax error: $upscope not followed by $end")
                while tok == b'$upscope':
                    if next(tokit) == b'$end':
                        vcd.write(b'$upscope $end\n')
                        scope_layer -= 1
                        tok = next(tokit)
                    else:
                        raise SoottyError("EVCD syntax error: $upscope not followed by $end")
                if scope_layer != 0:
                    raise SoottyError("EVCD syntax error: $scope and $upscope not matched")
            else:
                raise SoottyError("EVCD syntax error: invalid keyword")
        sim_kw = False
        while True:
            tok = next(tokit)
            if tok.startswith(b'#'):
                vcd.write(tok + b'\n')
            elif tok.startswith(b'p'):
                value_change = tok[1:]
                next(tokit)  # 0_strength_component
                next(tokit)  # 1_strength_component
                id_code = next(tokit)
                hash = vcdid_hash(id_code)
                node = vcd_ids.get(hash)
                if node is not None:
                    if node == 1:  # scalar change
                        vcd.write(b'%s%s\n' % (evcd_strcpy(value_change, False), vcdid_unhash(hash * 2)))
                        vcd.write(b'%s%s\n' % (evcd_strcpy(value_change, True), vcdid_unhash(hash * 2 + 1)))
                    else:  # node > 1, vector change
                        vcd.write(b'b%s %s\n' % (evcd_strcpy(value_change, False), vcdid_unhash(hash * 2)))
                        vcd.write(b'b%s %s\n' % (evcd_strcpy(value_change, True), vcdid_unhash(hash * 2 + 1)))
                else:
                    raise SoottyError("EVCD syntax error: undeclared identifier_code")
            # Ignores simulation keywords not in comments
            elif tok == b'$dumpports' or tok == b'$dumpportson' or tok == b'$dumpportsoff' or tok == b'$dumpportsall' or tok == b'$dumpportsflush' or tok == b'$dumpportslimit' or tok == b'$vcdclose':
                if not sim_kw:
                    sim_kw = True
                    continue
                else:
                    raise SoottyError("EVCD syntax error: previous simulation keyword not enclosed by $end")
            elif tok == b'$end':
                if sim_kw:
                    sim_kw = False
                    continue
                else:
                    raise SoottyError("EVCD syntax error: redundant $end")
            # Check VCD simulation keywords not in comments
            elif tok == b'$dumpvars' or tok == b'$dumpon' or tok == b'$dumpoff' or tok == b'$dumpflush' or tok == b'$dumplimit':
                raise SoottyError("EVCD syntax error: VCD simulation keywords detected")
            else:
                raise SoottyError("EVCD syntax error: invalid simulation time or value changes")
    except StopIteration:
        pass
    vcd.seek(0)
    return BufferedReader(vcd)
