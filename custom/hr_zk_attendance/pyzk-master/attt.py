from zk import ZK, const

conn = None
# create ZK instance
zk = ZK('10.100.10.10', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
conn = zk.connect()
print(conn)

