$(document).ready(function() {
    const cInput = parseInt(new URLSearchParams(window.location.search).get('c-input'));
    const hInput = parseInt(new URLSearchParams(window.location.search).get('h-input'));

    $.getJSON('hyd.json', function(data) {
        const tableBody = $('#molecule-table tbody');
        const filteredData = data.filter(function(molecule) {
            const nameMatch = molecule.formula.toLowerCase().split(/c|h/);
            return parseInt(nameMatch[1]) === cInput && parseInt(nameMatch[2]) === hInput;
        });

        if (filteredData.length > 0) {
            $.each(filteredData, function(index, molecule) {
                const row = $('<tr>');
                row.append($('<td>').html(`<a href="chemdata.html?search-input=${encodeURIComponent(molecule.smiles_format)}">${molecule.smiles_format}</a>`));
                row.append($('<td>').text(molecule.formula));
                row.append($('<td>').text(molecule.mol_wt));
                row.append($('<td>').text(molecule.pubchem_status));
                row.append($('<td>').text(molecule.pubchem_cid));
                row.append($('<td>').text(molecule.iupac_name));
                row.append($('<td>').text(molecule.RotationalconstantA));
                row.append($('<td>').text(molecule.RotationalconstantB));
                row.append($('<td>').text(molecule.RotationalconstantC));
                row.append($('<td>').text(molecule.Dipolemoment));
                row.append($('<td>').text(molecule.HOMO));
                row.append($('<td>').text(molecule.LUMO));
                row.append($('<td>').text(molecule.EnergyGap));
                row.append($('<td>').text(molecule.Zeropointenergy));
                row.append($('<td>').text(molecule.Finalsinglepointenergy));
                row.append($('<td>').text(molecule.Totalthermalenergy));
                row.append($('<td>').text(molecule.TotalEnthalpy));
                row.append($('<td>').text(molecule.Totalentropy));
                row.append($('<td>').text(molecule.Gibbsfreeenergy));
                
                tableBody.append(row);
            });
        } else {
            window.location.href = '404.html';
        }
    });
    
    // Auto-scroll functionality
    const tableContainer = $('.table-container');
    $(document).mousemove(function(event) {
        const windowWidth = $(window).width();
        const mouseX = event.pageX;
        const scrollSpeed = 30;
        
        if (mouseX < 50) {
            tableContainer.scrollLeft(tableContainer.scrollLeft() - scrollSpeed);
        } else if (mouseX > windowWidth - 50) {
            tableContainer.scrollLeft(tableContainer.scrollLeft() + scrollSpeed);
        }
    });
});