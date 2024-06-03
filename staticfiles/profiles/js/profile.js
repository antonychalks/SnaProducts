let countrySelected = $('#id_default_country').val();
if(!countrySelected) {
    $('#id_default_country').css('color', 'var(--bs-secondary-color)');
};
$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    if(!countrySelected) {
        $(this).css('color', 'var(--bs-secondary-color)');
    } else {
        $(this).css('color', '#000');
    }
});