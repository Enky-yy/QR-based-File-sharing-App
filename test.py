# from flask import Flask , render_template , send_from_directory
# import socket
# import os 
# import qrcode

# shared_folder = "shared"


# file = os.listdir("shared")
# print(file)

with open ('secrets.txt', 'r')as f:
    key = f.read(-1)

print(key)