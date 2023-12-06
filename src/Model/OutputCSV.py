from pandas import DataFrame

class OutputCSV:

    __FIELDS__ = ['fait','nbOccurences','annee','mois','departement']
    
    def __init__(self):
        self.data = DataFrame(columns=self.__FIELDS__)

    def addDepartement(self, dF : DataFrame, df_name: str, headers : list):
        print(f'Parsing sheet {df_name} {headers}')
        for index, row in dF.iterrows():
            self.addFait(row)
                
    

                

    


    