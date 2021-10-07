import mysql.connector
from mysql.connector.constants import ClientFlag

config = {
    'user': 'root',
    'password': 'avatar',
    'host': '34.85.166.17',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl_keys/server-ca.pem',
    'ssl_cert': 'ssl_keys/client-cert.pem',
    'ssl_key': 'ssl_keys/client-key.pem'
}


def connect():
    cnxn = mysql.connector.connect(**config)
    return cnxn
