# refer to RFC 3986 for the syntax of a valid URL

import random
import string

##################################################
#                 1. CHARACTERS                  #
##################################################

def pct_encoded():
    """
    percent encoded chars: "%" HEXDIG HEXDIG
    """
    return '%' + random.choice(string.hexdigits) + random.choice(string.hexdigits)

def gen_delims():
    """
    gen-delims: ":" / "/" / "?" / "#" / "[" / "]" / "@"
    """
    choices = ':' + '/' + '?' + '#' + '[' + ']' + '@'
    return random.choice(choices)

def sub_delims():
    """
    sub-delims: "!" / "$" / "&" / "'" / "(" / ")" / "*" / "+" / "," / ";" / "="
    """
    choices = '!' + '$' + '&' + "'" + '(' + ')' + '*' + '+' + ',' + ';' + '='
    return random.choice(choices)

def reserved():
    """
    reserved: gen-delims / sub-delims
    """
    if random.randrange(2):
        return gen_delims()
    else:
        return sub_delims()
    
def unreserved():
    """
    unreserved: ALPHA / DIGIT / "-" / "." / "_" / "~"
    """
    return string.ascii_letters + string.digits + '-' + '.' + '_' + '~'


##################################################
#                  2. SCHEMES                    # 
##################################################
def scheme(max_length = 5):
    """
    scheme: ALPHA *( ALPHA / DIGIT / "+" / "-" / "." )
    """
    scheme = ''
    scheme_length = random.randint(3, max_length)
    valid_chars = string.ascii_letters + string.digits + '+' + '-' + '.'
    # scheme += '[SCHEME START]'
    scheme += random.choice(string.ascii_letters) # scheme must start with a letter
    for _ in range(scheme_length - 1):
        scheme += random.choice(valid_chars)
    # scheme += '[SCHEME END]'
    return scheme


##################################################
#                 3. AUTHORITY                   # 
##################################################

##################################################
#              3.1  USER INFORMATION             # 
##################################################

def userinfo(max_length = 5):
    """
    userinfo: *( unreserved / pct-encoded / sub-delims / ":" )
    """
    userinfo = ''
    userinfo_length = random.randint(1, max_length)
    while userinfo_length > 0:
        userinfo += random.choice([
            random.choice(unreserved() + sub_delims() + ':'),
            random.choice(unreserved()),
            random.choice(unreserved()),
            random.choice(unreserved()),
            pct_encoded()
            ])
        userinfo_length -= 1
    userinfo += '@'   # userinfo must end with '@'
    return userinfo

##################################################
#                    3.2  HOST                   #
##################################################

def h16():
    """
    h16: 1*4HEXDIG
    """
    h16 = ''
    for _ in range(random.randint(1, 4)):
        h16 += random.choice(string.hexdigits)
    return h16

def dec_octet():
    """
    dec-octet   = DIGIT                 ; 0-9
                / %x31-39 DIGIT         ; 10-99
                / "1" 2DIGIT            ; 100-199
                / "2" %x30-34 DIGIT     ; 200-249
                / "25" %x30-35          ; 250-255
    """
    dec_octet = ''
    choice = random.randrange(5)
    if choice == 0:
        dec_octet += random.choice(string.digits)
    elif choice == 1:
        dec_octet += random.choice('123456789')
        dec_octet += random.choice(string.digits)
    elif choice == 2:
        dec_octet += '1'
        for _ in range(2):
            dec_octet += random.choice(string.digits)
    elif choice == 3:
        dec_octet += '2'
        dec_octet += random.choice('01234')
        dec_octet += random.choice(string.digits)
    else:
        dec_octet += '25'
        dec_octet += random.choice('012345')
    return dec_octet

def ip_v4_address():
    """
    IPv4address = dec-octet "." dec-octet "." dec-octet "." dec-octet
    """
    ip_v4_address = ''
    # ip_v4_address += '<IPv4 START>'
    for _ in range(3):
        ip_v4_address += dec_octet()
        ip_v4_address += '.'
    ip_v4_address += dec_octet()
    return ip_v4_address

def ls32():
    """
    ls32: ( h16 ":" h16 ) / IPv4address
    """
    ls32 = ''
    if random.randrange(2):
        ls32 = ip_v4_address()
    else:
        ls32 += h16()
        ls32 += ':'
        ls32 += h16()
    return ls32

def ip_v6_address():
    """
    IPv6address:                            6( h16 ":" ) ls32
                /                       "::" 5( h16 ":" ) ls32
                / [               h16 ] "::" 4( h16 ":" ) ls32
                / [ *1( h16 ":" ) h16 ] "::" 3( h16 ":" ) ls32
                / [ *2( h16 ":" ) h16 ] "::" 2( h16 ":" ) ls32
                / [ *3( h16 ":" ) h16 ] "::"    h16 ":"   ls32
                / [ *4( h16 ":" ) h16 ] "::"              ls32
                / [ *5( h16 ":" ) h16 ] "::"              h16
                / [ *6( h16 ":" ) h16 ] "::"
    """
    ip_v6_address = ''
    choice = random.randrange(9)
    if choice == 0:
        for _ in range(6):
            ip_v6_address += h16() + ':'
        ip_v6_address += ls32()
    elif choice == 1:
        ip_v6_address += '::'
        for _ in range(5):
            ip_v6_address += h16() + ':'
        ip_v6_address += ls32()
    elif choice == 2:
        ip_v6_address += h16() 
        ip_v6_address += '::'
        for _ in range(4):
            ip_v6_address += h16() + ':'
        ip_v6_address += ls32()
    elif choice == 3:
        ip_v6_address += h16() + ':'
        ip_v6_address += h16()
        ip_v6_address += '::'
        for _ in range(3):
            ip_v6_address += h16() + ':'
        ip_v6_address += ls32()
    elif choice == 4:
        for _ in range(2):
            ip_v6_address += h16() + ':'
        ip_v6_address += h16()
        ip_v6_address += '::'
        for _ in range(2):
            ip_v6_address += h16() + ':'
        ip_v6_address += ls32()
    elif choice == 5:
        for _ in range(3):
            ip_v6_address += h16() + ':'
        ip_v6_address += h16()
        ip_v6_address += '::'
        ip_v6_address += h16()
        ip_v6_address += ':'
        ip_v6_address += ls32()
    elif choice == 6:
        for _ in range(4):
            ip_v6_address += h16() + ':'
        ip_v6_address += h16()
        ip_v6_address += '::'
        ip_v6_address += ls32()
    elif choice == 7:
        for _ in range(5):
            ip_v6_address += h16() + ':'
        ip_v6_address += h16()
        ip_v6_address += '::'
        ip_v6_address += h16()
    else:
        for _ in range(6):
            ip_v6_address += h16() + ':'
        ip_v6_address += '::'
    return ip_v6_address

def ip_v_future(hexdig_max_len=8, usc_max_len = 8):
    """
    IPvFuture: "v" 1*HEXDIG "." 1*( unreserved / sub-delims / ":" )
    Remarks: usc = unreserved / sub-delims / ":"
    """
    ip_v_future = 'v'
    for _ in range(random.randint(1, hexdig_max_len)):
        ip_v_future += random.choice(string.hexdigits)
    ip_v_future += '.'
    for _ in range(random.randint(1, usc_max_len)):
        ip_v_future += random.choice(unreserved()+sub_delims()+':')
    return ip_v_future

def ip_literal():
    """
    IP-literal: "[" ( IPv6address / IPvFuture  ) "]"
    """
    ip_literal = ''
    # ip_literal += '<IP-LITERAL START>'
    ip_literal += '['
    choice = random.randrange(2)
    ip_literal += ip_v6_address()
    # if choice == 0:
    #     ip_literal += ip_v6_address()
    # else:
    #     ip_literal += ip_v_future()
    ip_literal += ']'
    return ip_literal

def reg_name(max_len = 10):
    """
    reg-name: *( unreserved / pct-encoded / sub-delims )
    """
    reg_name = ''
    # reg_name += '[REG-NAME START]'
    for _ in range(random.randrange(1, max_len)):
        reg_name += random.choice(string.ascii_letters + string.digits) # first char must be alphanumeric
        reg_name += random.choice([
            random.choice(unreserved() + sub_delims()),
            random.choice(unreserved() + sub_delims()),
            random.choice(unreserved() + sub_delims()),
            random.choice(unreserved() + sub_delims()),
            '.',
            '.',
            pct_encoded()
            ])
        reg_name += random.choice(string.ascii_letters + string.digits) # last char must be alphanumeric
    # reg_name += '[REG-NAME END]'
    return reg_name

def host(host_max_len):
    """
    host: IP-literal / IPv4address / reg-name
    Remarks: 
        - 16.67% chance of having IP-literal
        - 16.67% chance of having IPv4address
        - 66.66% chance of having reg-name
    """
    choice = random.randrange(3)
    if choice == 0:
        if random.randrange(2):
            return ip_literal()
        else:
            return ip_v4_address()
    else:
        return reg_name(host_max_len)

##################################################
#                    3.3  PORT                   #
##################################################

def port(max_len = 5):
    """
    port: *DIGIT
    """
    port = ''
    for _ in range(random.randrange(1, max_len)):
        port += random.choice(string.digits)
    return port

##################################################
#                 3.4  AUTHORITY                 #
##################################################

def authority(userinfo_max_len = 5, host_max_len = 10, port_max_len = 5):
    """
    authority: [ userinfo "@" ] host [ ":" port ]
    """
    authority = ''
    # authority += "[AUTHORITY START]"
    authority += "//"    # authority must start with '//'
    
    '''
    userinfo: *( unreserved / pct-encoded / sub-delims / ":" )
    remarks: 16.67% chance of having userinfo
    '''
    if not random.randrange(6):
        # authority += "[USERINFO START]"
        authority += userinfo(userinfo_max_len)
        # authority += "[USERINFO END]"
        
            
    '''
    host: IP-literal / IPv4address / reg-name
    remarks: equal chance of having IP-literal, IPv4address, or reg-name (i.e. 33% chance each)
    '''
    # authority += "[HOST START]"
    authority += host(host_max_len)
    # authority += "[HOST END]"

    '''
    port: *DIGIT
    remarks: 16.67% chance of having port
    '''
    if not random.randrange(6):
        # authority += "[PORT START]"
        authority += ':'
        authority += port(port_max_len)
        # authority += "[PORT END]"

    # authority += "[AUTHORITY END]"
    return authority


##################################################
#                    4.  PATH                   #
##################################################

def pchar():
    """
    pchar: unreserved / pct-encoded / sub-delims / ":" / "@"
    """
    return random.choice([
        random.choice(unreserved() + sub_delims() + ':' + '@'),
        random.choice(unreserved() + sub_delims() + ':' + '@'),
        random.choice(unreserved() + sub_delims() + ':' + '@'),
        random.choice(unreserved() + sub_delims() + ':' + '@'),
        pct_encoded(),])

def segment(max_len = 10):
    """
    segment: *pchar
    """
    segment = ''
    for _ in range(random.randrange(0, max_len)):
        segment += pchar()
    return segment

def segment_nz(max_len = 10):
    """
    segment-nz: 1*pchar
    """
    segment_nz = ''
    for _ in range(random.randrange(1, max_len)):
        segment_nz += pchar()
    return segment_nz

def segment_nz_nc(max_len = 10):
    """
    segment-nz-nc: 1*( unreserved / pct-encoded / sub-delims / "@" )
    """
    segment_nz_nc = ''
    for _ in range(random.randrange(1, max_len)):
        segment_nz_nc += random.choice([
            random.choice(unreserved() + sub_delims() + '@'),
            random.choice(unreserved() + sub_delims() + '@'),
            random.choice(unreserved() + sub_delims() + '@'),
            pct_encoded()
            ])
    return segment_nz_nc

def path_abempty(max_len = 10):
    """
    path-abempty: *( "/" segment )
    """
    path_abempty = ''
    # path_abempty += '<PATH-ABEMPTY START>'
    for _ in range(random.randrange(max_len)):
        path_abempty += '/'
        path_abempty += segment()
    return path_abempty

def path_absolute(max_len = 10):
    """
    path-absolute: "/" [ segment-nz *( "/" segment ) ]
    """
    path_absolute = ''
    # path_absolute += '<PATH-ABSOLUTE START>'
    path_absolute += '/'
    path_absolute += segment_nz()
    for _ in range(1,random.randrange(max_len)):
        path_absolute += '/'
        path_absolute += segment()
    return path_absolute

def path_noscheme(max_len = 10):
    """
    path-noscheme: segment-nz-nc *( "/" segment )
    """
    path_noscheme = ''
    # path_noscheme += '<PATH-NOSCHEME START>'
    path_noscheme += segment_nz_nc()
    for _ in range(random.randrange(max_len)):
        path_noscheme += '/'
        path_noscheme += segment()
    return path_noscheme

def path_rootless(max_len = 10):
    """
    path-rootless: segment-nz *( "/" segment )
    """
    path_rootless = ''
    # path_rootless += '<PATH-ROOTLESS START>'
    path_rootless = segment_nz()
    for _ in range(random.randrange(max_len)):
        path_rootless += '/'
        path_rootless += segment()
    return path_rootless

def path_empty():
    """
    path-empty: 0<pchar>
    """
    path_empty = ''
    # path_empty += '<PATH-EMPTY START>'
    return path_empty

def path():
    """
    path: path-abempty / path-absolute / path-noscheme / path-rootless / path-empty
    """
    choice = random.randrange(14)
    if choice == 0:
        return path_abempty()
    elif 1 <= choice <= 4:
        return path_absolute()
    elif 5 <= choice <= 8:
        return path_noscheme()
    elif 9 <= choice <= 12:
        return path_rootless()
    else:
        return path_empty()
    

##################################################
#                    5.  QUERY                   #
##################################################

def query(max_len = 10):
    """
    query: *( pchar / "/" / "?" )
    """
    query = ''
    # query += '[QUERY START]'
    for _ in range(random.randrange(max_len)):
        query += random.choice([
            pchar(),
            pchar(),
            pchar(),
            pchar(),
            pchar(),
            pchar(),
            '/',
            '?'])
    # query += '[QUERY END]'
    return query


##################################################
#                    6. FRAGMENT                 #
##################################################

def fragment(max_len = 10):
    """
    fragment: *( pchar / "/" / "?" )
    """
    fragment = ''
    # fragment += '<FRAGMENT START>'
    for _ in range(random.randrange(max_len)):
        fragment += random.choice([
            pchar(),
            pchar(),
            pchar(),
            pchar(),
            pchar(),
            pchar(),
            '/',
            '?'])
    # fragment += '<FRAGMENT END>'
    return fragment


##################################################
#             7. GENERATE VALID URL              #
##################################################

def hier_part():
    """
    hier-part: "//" authority path-abempty / path-absolute / path-rootless / path-empty
    """
    hier_part = ''
    if random.randrange(5):
        hier_part += authority()
        # hier_part += '[PATH START]'
        # hier_part += '[ABEMPTY START]'
        hier_part += path_abempty()
        # hier_part += '[ABEMPTY END]'
    else:
        # hier_part += '[PATH START]'
        # hier_part += '[ABSOLUTE START]'
        hier_part += path_absolute()
        # hier_part += '[ABSOLUTE END]'

        # hier_part += '[PATH END]'
    return hier_part


def url():
    """
    url: scheme ":" hier-part [ "?" query ] [ "#" fragment ]
    """
    url = ''
    url += scheme()
    url += ':'
    url += hier_part()
    if not random.randrange(4):
        url += '?'
        url += query()
    if not random.randrange(4):
        url += '#'
        url += fragment()
    return url


##################################################
#     8. GENERATE INVALID URL (NOT REQUIRED)     #
##################################################

# def invalid_url():
#     invalid_url = url()
#     invalid_chars = random.sample(string.ascii_letters + string.digits + '-._~:/?#[]@!$&\'()*+,;=', random.randint(1, 10))
#     index = random.randint(0, len(invalid_url) - 1)
#     for char in invalid_chars:
#         invalid_url = invalid_url[:index] + char + invalid_url[index+1:]
#         index = random.randint(0, len(invalid_url) - 1)
    
#     return invalid_url


##################################################
#                     9. MAIN                    #
##################################################

if __name__ == "__main__":
    N = 100
    # Generate N valid URLs
    valid_urls = [url() for _ in range(N)]
    print("Valid URLs:")
    for url in valid_urls:
        print(f'| {url : <{len(max(valid_urls, key=len))}}  |'.lower())
