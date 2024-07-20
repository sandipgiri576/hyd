$(document).ready(function() {
    const searchInput = new URLSearchParams(window.location.search).get('search-input');

    // Define a mapping for property names
    const propertyNameMap = {
        'smiles_format': 'SMILE',
        'formula': 'Formula',
        'mol_wt': 'Molecular weight(g/mol)',
        'pubchem_status': 'Pubchem status',
        'pubchem_cid': 'Pubchem cid',
        'iupac_name': 'IUPAC name',
        'RotationalconstantA': 'Rotational constant A(cm-1)',
        'RotationalconstantB': 'Rotational constant B(cm-1)',
        'RotationalconstantC': 'Rotational constant C(cm-1)',
        'Dipolemoment': 'Dipole moment(Debye)',
        'HOMO': 'HOMO(eV)',
        'LUMO': 'LUMO(eV)',
        'EnergyGap': 'Energy Gap(eV)',
        'Zeropointenergy': 'Zeropoint energy(Eh)',
        'Finalsinglepointenergy': 'Singlepoint energy(Eh)',
        'Totalthermalenergy': 'Thermal energy(Eh)',
        'TotalEnthalpy': 'Enthalpy(Eh)',
        'Totalentropy': 'Entropy(Eh)',
        'Gibbsfreeenergy': 'Gibbs free energy(Eh)'    
    };

    $.getJSON('hyd.json', function(data) {
        const tableBody = $('#molecule-table tbody');
        const molecule = data.find(function(molecule) {
            return molecule.smiles_format.toLowerCase() === searchInput.toLowerCase();
        });

        // if (molecule) {
        //     const row = $('<tr>');
        //     const mappedName = propertyNameMap[key] || key.charAt(0).toUpperCase() + key.slice(1).replace(/_/g, ' ');
        //     row.append($('<th>').text('smiles_format'));
        //     row.append($('<td>').text(molecule.smiles_format));
        //     tableBody.append(row);

        //     Object.entries(molecule).forEach(function([key, value]) {
        //         if (key !== 'smiles_format') {
        //             const row = $('<tr>');
        //             row.append($('<th>').text(key.charAt(0).toUpperCase() + key.slice(1)));
        //             row.append($('<td>').text(value));
        //             tableBody.append(row);
        //         }
        //     });

        if (molecule) {
            tableBody.empty(); // Clear existing content

            Object.entries(molecule).forEach(function([key, value]) {
                const row = $('<tr>');
                const mappedName = propertyNameMap[key] || key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
                row.append($('<th>').text(mappedName));
                row.append($('<td>').text(value));
                tableBody.append(row);
            });

            // Automatically load the structure
            if (molecule.structure) {
                var filePath = "static/structure/" + molecule.structure;
                Jmol.script(jmolApplet0, 'load ' + filePath);
            }
        } else {
            window.location.href = '404.html';
        }
    });
});



