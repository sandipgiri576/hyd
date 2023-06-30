import sys
import sqlite3
import csv
import pandas as pd
from rdkit import Chem
from rdkit.Chem.rdMolDescriptors import CalcMolFormula


class Molecules():
    # Initializing the connection and cursor object to it.
    def __init__(self):
        self.connection = None
        self.cursor = None
    # connect with a database --argument is database name!

    def CreateConnection(self, database_name):
        try:
            self.connection = sqlite3.connect(
                database_name, check_same_thread=False)
        except Exception as e:
            print("Error: "+str(e))
        else:
            print("Database connection succeeded")
        return self.connection

    # Databse Management - loading all information present in csv file
    def Load_Molecules(self, file_):
        # All Commands related to database;
        # Chemdatafile - CSV file
        print("Loading database")

        query_drop = "DROP TABLE IF EXISTS chemdatafile;"
        try:
            self.cursor.execute(query_drop)
        except Exception as e:
            print("Query failed while executing the defined statement!: "+str(e))
        query1 = '''
            CREATE TABLE IF NOT EXISTS chemdatafile (
            smiles VARCHAR(29) NOT NULL, `A` DECIMAL(38, 5) NOT NULL, `B` DECIMAL(38, 7) NOT NULL, `C` DECIMAL(38, 7) NOT NULL, mu DECIMAL(38, 4) NOT NULL, homo DECIMAL(38, 4) NOT NULL, lumo DECIMAL(38, 4) NOT NULL, gap DECIMAL(38, 4) NOT NULL, zpve DECIMAL(38, 6) NOT NULL, u298 DECIMAL(38, 6) NOT NULL, h298 DECIMAL(38, 6) NOT NULL, g298 DECIMAL(38, 6) NOT NULL, cv DECIMAL(38, 3) NOT NULL
            );
        '''
        if (file_):
            file = open('./webserver/HYD_database/chemdatafile.csv')
        else:
            file = open('./chemdatafile.csv')
        # Now, Read the contents from the file using csv reader
        contents = csv.reader(file)
        contents2 = next(contents)
        # Already the table has been created, the rest is to insert all the info
        query2 = "INSERT INTO chemdatafile values(?,?,?,?,?,?,?,?,?,?,?,?,?);"
        try:
            self.cursor.execute(query1)
            self.cursor.executemany(query2, contents)
        except Exception as e:
            print("Query failed while executing the defined statement!: "+str(e))

        print("Loading database has been done...")

    # Retrieving all the Information using the table name
    def RetrieveFullInfo(self, table_name):
        RetrievedList = []
        query = f"SELECT * FROM {table_name};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving information using and condition -- molecules with only the specified elements
    def RetrieveElements_AND(self, table_name, element1='', element2='', element3='', element4='', element5=''):
        RetrievedList = []
        query = f"SELECT * FROM {table_name} WHERE (smiles like '%{element1}%' or smiles like '%{element1.lower()}%')  AND (smiles like '%{element2}%' or smiles like '%{element2.lower()}%') AND (smiles like '%{element3}%' or smiles like '%{element3.lower()}%') AND (smiles like '%{element4}%' or smiles like '%{element4.lower()}%') AND (smiles like '%{element5}%' or smiles like '%{element5.lower()}%');"
        try:
            self.cursor.execute(query)
            RetrievedList = self.cursor.fetchall()
        except Exception as e:
            print("Query failed while executing the defined statement!: "+str(e))
        return RetrievedList
    # Retrieving information using OR condition -- molecules with any of the specified elements
    def RetrieveElements_OR(self, table_name, element1=None, element2=None, element3=None, element4=None, element5=None):
        RetrievedList = []
        query = f"SELECT * FROM {table_name} WHERE smiles like '%{element1}%' or smiles like '%{element2}%' or smiles like '%{element3}%' or smiles like '%{element4}%' or smiles like '%{element5}%';"
        try:
            self.cursor.execute(query)
            RetrievedList = self.cursor.fetchall()
        except Exception as e:
            print("Query failed while executing the defined statement!: "+str(e))
        return RetrievedList
    # Retrieving information using AND condition -- molecules with only the specified elements and other chemical properties
    def RetrieveElements_AND1(self, table_name, element1='', element2='', element3='', element4='', element5='', A_val=None, B_val=None, C_val=None, mu_val=None, homo_val=None, lumo_val=None, gap_val=None, zpve_val=None, u298_val=None, h298_val=None, g298_val=None, cv_val=None):
        RetrievedList = []
        query = f"SELECT * FROM {table_name} WHERE smiles like '%{element1}%' AND smiles like '%{element2}%' AND smiles like '%{element3}%' AND smiles like '%{element4}%' AND smiles like '%{element5}%' and A={A_val} and B={B_val} and C={C_val} and mu={mu_val} and homo={homo_val} and lumo={lumo_val} and gap={gap_val} and zpve={zpve_val} and u298={u298_val} and h298={h298_val} and g298={g298_val} and cv={cv_val};"
        try:
            self.cursor.execute(query)
            RetrievedList = self.cursor.fetchall()
        except Exception as e:
            print("Query failed while executing the defined statement!: "+str(e))
        return RetrievedList
    # Retrieving only smile representation
    def RetrieveSmiles(self, table_name):
        RetrievedList = []
        query = f"SELECT smiles FROM {table_name}"
        try:
            self.cursor.execute(query)
            RetrievedList = self.cursor.fetchall()
        except Exception as e:
            print("Query failed while executing the defined statement!: "+str(e))
        return RetrievedList
    # Finding molecular formula for the specified smile string using rdkit
    def MolFormula_Smiles(self, smile):
        mol = Chem.MolFromSmiles(smile)
        mol_formula = CalcMolFormula(mol)
        return mol_formula
    # Retrieving all the info using stochiomtric values -- number of elements
    def MolFromStoichiometry(self, table_name, elementC=0, elementH=0, elementO=0, elementF=0, elementN=0):
        RetrievedList = self.RetrieveSmiles(table_name)
        Final_MolDict = {}
        key = 0
        # Optimized algorithm for finding number of particular elements in a molecular formula
        for smile in RetrievedList:
            mol = self.MolFormula_Smiles(smile[0])
            num_list = {"elementC": 0, "elementH": 0,
                        "elementO": 0, "elementF": 0, "elementN": 0}
            i = 0
            j = 0
            n = len(mol)
            carry = ""
            while (i < n or j < n):
                if (j < n and mol[j].isnumeric()):
                    if (j != n):
                        carry += mol[j]
                        j += 1
                elif (j == n or mol[j].isalpha() or mol[j] == '-' or mol[j] == '+'):
                    if (i < j and mol[i].isalpha()):
                        val = 0
                        try:
                            val = int(carry)
                        except Exception as e:
                            val = 1
                        if (mol[i].upper() == 'C'):
                            num_list["elementC"] += val
                        elif (mol[i].upper() == 'H'):
                            num_list["elementH"] += val
                        elif (mol[i].upper() == 'O'):
                            num_list["elementO"] += val
                        elif (mol[i].upper() == 'F'):
                            num_list["elementF"] += val
                        elif (mol[i].upper() == 'N'):
                            num_list["elementN"] += val
                        carry = ""
                    i = j
                    j += 1
                else:
                    i = j
                    j += 1
            if (num_list["elementC"] == elementC and num_list["elementH"] == elementH and num_list["elementF"] == elementF and num_list["elementN"] == elementN and num_list["elementO"] == elementO):
                key += 1
                Final_MolDict[key] = [
                    mol, self.MolFromSmile('chemdatafile', smile[0])]
                # print(Final_MolDict)
        return Final_MolDict
    # Retrieving properties using smile representation
    def MolFromSmile(self, table_name, smile_rep):
        print("the smile rep is: "+smile_rep)
        RetrievedList = []
        query = f"SELECT * FROM {table_name} WHERE smiles=(?) or smiles=(?);"
        try:
            self.cursor.execute(query, (smile_rep, smile_rep.upper()))
            RetrievedList = self.cursor.fetchall()
        except Exception as e:
            print("Query failed while executing the defined statement!: "+str(e))
        return RetrievedList
    # Retrieving info using a,b,c constants
    def RetrieveRotationalConstants(self, table_name, a, b, c):
        query = f"SELECT * FROM {table_name} WHERE A=? AND B=? AND C=?;"
        self.cursor.execute(query, (a, b, c,))
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using dipole moment
    def RetrieveDipoleMoment(self, table_name, DipoleMoment):
        query = f"SELECT * FROM {table_name} WHERE mu=?;"
        self.cursor.execute(query, (DipoleMoment,))
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using Internal constants
    def RetreiveInternalConstant(self, table_name, InternalConstant):
        query = f"SELECT * FROM {table_name} WHERE alpha={InternalConstant};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using homo value 
    def RetrieveHighestOccupiedMolecularOrbit(self, table_name, MO):
        query = f"SELECT * FROM {table_name} WHERE homo=?;"
        self.cursor.execute(query, (MO,))
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using lumo value
    def RetrieveLowestUnoccupiedMolecularOrbit(self, table_name, MO):
        query = f"SELECT * FROM {table_name} WHERE lumo=?;"
        self.cursor.execute(query, (MO,))
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using gap value
    def RetrieveGap(self, hl, table_name):
        query = f"SELECT * FROM {table_name} WHERE GAP={hl};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using r2 value
    def RetrieveScore(self, table_name, score):
        query = f"SELECT * FROM {table_name} WHERE r2={score};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using ZPVE value
    def RetrieveZeroPointVibrationalEnergy(self, table_name, VE):
        query = f"SELECT * FROM {table_name} WHERE ZPVE={VE};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using u at 0k 
    def RetrieveInternalEnergy_0(self, table_name, u0=0.0):
        query = f"SELECT * FROM {table_name} WHERE u0={u0};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using u at 298k 
    def RetrieveInternalEnergy_298(self, table_name, u298=None):
        query = f"SELECT * FROM {table_name} WHERE u298={u298};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using h at 298k
    def RetrieveEnthalpy_298(self, table_name, h298=None):
        query = f"SELECT * FROM {table_name} WHERE h298={h298};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using g at 298k
    def RetrieveGibbsFreeEnergy_298(self, table_name, g298=None):
        query = f"SELECT * FROM {table_name} WHERE g298={g298};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using cv value
    def RetrieveMolarHeatCapacity(self, table_name, cv=None):
        query = f"SELECT * FROM {table_name} WHERE cv={cv};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using u0_atom value
    def RetrieveInternalEnergy_atom_0(self, table_name, u0_atom=None):
        query = f"SELECT * FROM {table_name} WHERE u0_atom={u0_atom};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using u298_atom value
    def RetrieveInternalEnergy_atom_298(self, table_name, u298_atom=None):
        query = f"SELECT * FROM {table_name} WHERE u298_atom={u298_atom};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using h298_atom value
    def RetrieveEnthalpy_atom_298(self, table_name, h298_atom=None):
        query = f"SELECT * FROM {table_name} WHERE h298_atom={h298_atom};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Retrieving info using g298_atom value
    def RetrieveGibbsFreeEnergy_atom_298(self, table_name, g298_atom=None):
        query = f"SELECT * FROM {table_name} WHERE g298_atom={g298_atom};"
        self.cursor.execute(query)
        RetrievedList = self.cursor.fetchall()
        return RetrievedList
    # Algorithm-1 for extraction of hydrocarbons - exclusively hydrogens and carbons
    def hydrocarbons_utility1(self, table_name):
        columns = ["smiles", "mol_no"]
        rows = self.RetrieveFullInfo('chemdatafile')
        print("Retrieving has been done!")
        newrows = []
        # file path can be changed!
        with open("D:\Projects\webserver\HYD_database\HydroCarbons_smiles.csv", 'w') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(columns)
            for ls in rows:
                smile_str = "".join(char for char in ls[2] if char.isalpha())
                if ((all(char == 'C' or char == 'c' or char == 'H' or char == 'h' for char in smile_str))):
                    csv_writer.writerow(ls)
        return
    # Algorithm-2 for extraction of hydrocarbons - exclusively hydrogens and carbons
    def hydrocarbons_utility2(self, table_name):
        columns = ["smiles", "mol_no"]
        rows = self.RetrieveFullInfo('chemdatafile')
        print("Retrieving has been done!")
        newrows = []
        for ls in rows:
            y = 1
            for l in ls[2]:
                if (l >= 'a' and l < 'c') or (l > 'c' and l < 'h') or (l > 'h' and l <= 'z'):
                    y = 0
                    break
                if (l >= 'A' and l < 'C') or (l > 'C' and l < 'H') or (l > 'H' and l <= 'Z'):
                    y = 0
                    break
            if (y):
                newrows.append(ls)
        print("removal has been done!")

        with open("D:\Projects\webserver\HYD_database\HydroCarbons_smiles.csv", 'w') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(columns)
            csv_writer.writerows(newrows)
        print("file created output file ")
        return
    # info inserting into csv file
    def to_csv_utility(self):

        # columns for chemdatafile
        '''columns = ["smiles", 'A', 'B', 'C', "mu", "homo", "lumo", "gap",
                   "zpve", "u298", "h298", "g298", "cv"]'''
        # columns for pubchemfile
        columns = ["smiles", "mol_no"]
        rows = self.RetrieveElements_AND(
            "pubchemfile", element1='C', element2='O')
        # To CSV File from two lists with rows and columns
        with open("Oxy-Carbon_smiles", 'w') as file:
            write_file = csv.writer(file)
            write_file.writerow(columns)
            write_file.writerows(rows)
        return

    def dat_to_excel(self):
        # Limitation of rows where a sheet can have only 1048576 rows ->csv is the option
        df = pd.read_table(
            "D:\Projects\pubchem_data\pubchem.tar\pubchem\pubchem.dat")
        # df.to_excel('pubchem.xlsx')
        # print(df.head())
        return
    # Information extraction for log files
    def file_extraction(self, file_path):
        res_dict = {}
        with open(file_path, 'r') as in_file:
            i = 0
            for row in in_file:
                if (row == "QM Software:   orca\n"):
                    i = 1
                elif (i == 1):
                    row_values = [row_val.strip()
                                  for row_val in row.split(':')]
                    for val in row_values:
                        res_dict[val[0]] = val[1]
        return res_dict
    # Working with pandas
    def write_csv(self, file_path, res_dict):
        df = pd.read_csv(file_path)
        df["energy"] = NULL
        for key in res_dict:
            for x in df.index:
                if (key == df.loc[x, xyz_file]):
                    df.loc[x, xyz_file] = res_dict[key]

    # Conversion from dat to csv files.
    def dat_to_csv(self):
        columns = ["smiles", "serial No."]
        #in_file=open("filepath", 'r')
        #out_file=open("file", 'w')
        with open("D:\Projects\pubchem_data\pubchem.tar\pubchem\pubchem.dat", 'r') as in_file:
            with open("pubchem.csv", 'w') as out_file:
                csv_writer = csv.writer(out_file)
                csv_writer.writerow(columns)
                for row in in_file:
                    row_values = [row_val.strip()
                                  for row_val in row.split(',')]
                    csv_writer.writerow(row_values)
        return


if (__name__ == "__main__"):
    QueryDB = Molecules()
    # Connect with the sqlite databse
    QueryDB.CreateConnection("chemdatabase.db")
    QueryDB.cursor = QueryDB.connection.cursor()
    # Load molecules
    QueryDB.Load_Molecules(True)
    QueryDB.MolFromStoichiometry('chemdatafile', elementC=5, elementH=4)
    QueryDB.connection.commit()
else:
    QueryDB = Molecules()
    # Connect with the sqlite databse
    QueryDB.CreateConnection("chemdatabase.db")
    # add cursor object to the molecules prototype
    QueryDB.cursor = QueryDB.connection.cursor()
    QueryDB.Load_Molecules(False)
    QueryDB.connection.commit()
