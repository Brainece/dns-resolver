import socket

port = 53
ip = '127.0.0.1'

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((ip, port))

def getFlags(flags):
    
    byte1 = bytes(flags[:1])
    byte1 = bytes(flags[1:2])


    rflags = ''

    QR = '1'

    OPCODE = ''
    for bit in range(1,5):
        OPCODE += str(ord(byte1)&(1<<bit))
    
    AA = '1'
    TC = '0'
    RD = '0'
    RA = '0'
    Z = '000'
    RCODE = '0000'

    return int(QR+OPCODE+AA+TC+RD,2).to_bytes(1,byteorder='big') + int(RA+Z+RCODE, 2).to_bytes(1, byteorder='big')

def getQuestionDomain(data):

    state = 0
    expectedlength = 0
    domainstring = ''
    domainparts = []
    x = 0
    y = 0

    for byte in data:
        if state == 1:
            domainstring += chr(byte)
            x += 1
            if x == expectedlength:
                domainparts.append(domainstring)
                domainstring = ''
                state = 0
            if byte == 0:
                domainparts.append(domainstring)
                break
        else:
            state = 1
            expectedlength = byte
        
        x += 1
        y += 1

        questiontype = data[y+1:y+3]
        
        return (domainparts, questiontype)


def buildResponse(data):
    
    # Transaction ID
    transactionID = data[:2]
    TID = ''
    for byte in transactionID:
        TID += hex(byte)[:2]

    # get the flags
    Flags = getFlags(data[2:4])

    # Question Count
    QDCOUNT = b'\x00\x01'

    # Answer Count
    getQuestionDomain(data[12:])

    #print(Flags)

while 1:
    data, addr = sock.recvfrom(512)
    r = buildResponse(data)
    sock.sendto(r, addr)




