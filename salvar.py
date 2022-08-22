import logging
import os
import pandas as pd

def salvar_csv(self, obj):
    logging.info('***SALVANDO***')

    FILE_PATH = self.FILE_PATH + '.csv'
    if os.path.exists(FILE_PATH):
        df1 = pd.read_csv(FILE_PATH)
        df = pd.DataFrame(obj)
        merged = pd.concat([df1,df])
        merged.to_csv(FILE_PATH, index=False)


    else:
        df = pd.DataFrame(obj)
        df.to_csv(FILE_PATH, index=False)