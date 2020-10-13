from namv_mi import helpers

class Vehicle():
    def __init__(self, df_row):
        '''
        This may be unneccessary... 
        since we r just using the df_row key, vals
        '''
        #print(df_row)
        #print(df_row.name)
        for key, val in df_row.items():
            self.__dict__[key] = val
