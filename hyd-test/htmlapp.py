from flask import Flask, render_template, request
import sqlite3
import checkpoint as cp

# Web application object
app = Flask(__name__)
DB_NAME = "chemdatabase.db"


# Decorator app.route('/')-- special function routing the function to call whenver the application made to run
@app.route('/')
def index() :
    # Home page with different search queries
    return render_template('index.html')


# +
# Decorator app.route('/results')-- function call occurs once the search query is done after the application made to run with url - 127.0.0.1:5000/results
# GET-POST -- Post method is better to use for security reasons without showing name value pairs in th url
@app.route('/results', methods=['POST'])
def results() :
    # requests are made to retrieve info form the user input in home page
    drug_name = request.form['drug_name'].lower()

    # If else statements- match with the search queries from the home page!
    # Choice1-- using molecular name
    if request.form['choice'] == 'choice1' :
        try :
            properties = cp.get_physical_properties(drug_name)
        except : 
            return render_template('nophysicochemical.html', name=drug_name)
        pic_url = cp.get_molecular_picture(drug_name)
        print(properties)
        property_key_list = ["MolecularWeight", "MolecularFormula", "IUPACName", "IsomericSMILES",
                             "CanonicalSMILES", "InChI", "InChIKey",
                             "RotatableBondCount"]
        variable_list = [None, None, None, None, None, None, None, None]
        for i in range(len(property_key_list)):
            if property_key_list[i] in properties.keys() :
                variable_list[i] = properties[property_key_list[i]]
        return render_template('physicochemical.html', name=drug_name, url=pic_url,
                    formula=variable_list[1], mw=variable_list[0], iupac=variable_list[2], isomericsmile=variable_list[3], 
                    canonicalsmile=variable_list[4], inchi=variable_list[5], inchikey=variable_list[6], rb=variable_list[7])
    # Choice2-- using smile representation
    elif request.form["choice"] == 'choice2' :
        result=[]
        try:
            result=cp.get_MolFromSmile(drug_name)
            print(result)
        except Exception as e:
            print("Molecule from smile Retrieving failed! "+str(e))
        return render_template("chemdatafile.html", name=drug_name, s_rep=result[0][0],a_val=result[0][1], b_val=result[0][2], c_val=result[0][3], mu_val=result[0][4], homo_val=result[0][5], lumo_val=result[0][6], gap_val=result[0][7], zpve_val=result[0][8], u298_val=result[0][9], h298_val=result[0][10],g298_val=result[0][11], cv_val=result[0][12] )
    # Choice3-- using molecular formula
    elif request.form["choice"] == "choice3" :
        return render_template(str(drug_name)+"_fresh_new.html")
    # choice 4- using stoichiometric values
    elif (request.form["choice"]=="choice4"):
        cf_val=request.form.get("ElementC","")
        hf_val=request.form.get("ElementH","")
        of_val=request.form.get("ElementO","")
        ff_val=request.form.get("ElementF","")
        nf_val=request.form.get("ElementN","")
        try:
            res=cp.get_MolFromStoichiometry(element1=cf_val, element2=hf_val,element3=of_val,element4=ff_val,element5=nf_val)
            print(res)
            return render_template("MolStoichiometry.html",c_val=cf_val, h_val=hf_val,o_val=of_val,f_val=ff_val,n_val=nf_val,results=res)
        except Exception as e:
            print("Molecule with stoichiomery Retrieving failed! "+str(e))
    
# render template is used to return a html page or fetch a html page whether it is dynamic or not dynamic
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
    

