$(document).ready(function () {
    $('#top-navbar').removeClass('d-lg-none');
});

$( window ).on( "unload", function () {
    $('#top-navbar').addClass('d-lg-none');
});