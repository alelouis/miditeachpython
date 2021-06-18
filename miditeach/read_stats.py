import pickle
import os

files_path = os.listdir('./stats')

for file_path in files_path:
    with open('./stats/' + file_path, 'rb') as f:
        try:
            while True:
                print(pickle.load(f))
        except EOFError:
            pass
