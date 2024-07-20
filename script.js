$(document).ready(function() {
    $('#search-form').submit(function(event) {
        event.preventDefault();
        const searchInput = $('#search-input').val().trim();
        window.location.href = `chemdata.html?search-input=${encodeURIComponent(searchInput)}`;
    });

    $('#name-search-form').submit(function(event) {
        event.preventDefault();
        const cInput = $('#c-input').val();
        const hInput = $('#h-input').val();
        window.location.href = `molstochiometry.html?c-input=${encodeURIComponent(cInput)}&h-input=${encodeURIComponent(hInput)}`;
    });

    // $('#smiles-form').submit(function(event) {
    //     event.preventDefault();
    //     const smilesInput = $('#smiles-input').val().trim();
    //     window.location.href = `chemdata.html?search-input=${encodeURIComponent(smilesInput)}`;
    // });

    // $('#molstoichiometry-form').submit(function(event) {
    //     event.preventDefault();
    //     const cInput = $('#c-input').val();
    //     const hInput = $('#h-input').val();
    //     window.location.href = `molstochiometry.html?c-input=${encodeURIComponent(cInput)}&h-input=${encodeURIComponent(hInput)}`;
    // });



    // $('#dipole-search-form').submit(function(event) {
    //     event.preventDefault();
    //     const minDipole = $('#min-dipole-input').val();
    //     const maxDipole = $('#max-dipole-input').val();
    //     window.location.href = `molsearch.html?min-dipole=${encodeURIComponent(minDipole)}&max-dipole=${encodeURIComponent(maxDipole)}`;
    // });
    // $('#homo-search-form').submit(function(event) {
    //     event.preventDefault();
    //     const minHOMO = $('#min-homo-input').val();
    //     const maxHOMO = $('#max-homo-input').val();
    //     window.location.href = `homo.html?min-homo=${encodeURIComponent(minHOMO)}&max-homo=${encodeURIComponent(maxHOMO)}`;
    // });
    
    $('#property-search-form').submit(function(event) {
        event.preventDefault();
        const selectedType = $('#search-type').val();
        const minValue = $('#min-value').val();
        const maxValue = $('#max-value').val();
        window.location.href = `results.html?property=${encodeURIComponent(selectedType)}&min-value=${encodeURIComponent(minValue)}&max-value=${encodeURIComponent(maxValue)}`;
    });
});