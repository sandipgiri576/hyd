$(document).ready(function() {
    const urlParams = new URLSearchParams(window.location.search);
    const property = urlParams.get('property');
    const minValue = parseFloat(urlParams.get('min-value'));
    const maxValue = parseFloat(urlParams.get('max-value'));

    $.getJSON('hyd.json', function(data) {
        const tableBody = $('#results-table tbody');
        const filteredData = data.filter(function(molecule) {
            return molecule[property] >= minValue && molecule[property] <= maxValue;
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
    }).fail(function() {
        console.error('Error fetching data.');
        tableBody.append($('<tr>').append($('<td colspan="6">').text('Error fetching data.')));
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

