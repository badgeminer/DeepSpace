def new(name,ms):
    with open(name,"wb") as f:
        for i in range(ms):
            f.write(bytes.fromhex("00"))