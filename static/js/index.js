$(document).ready(function () {
    console.log("Showing top-nav")
    $('#top-navbar').removeClass('d-lg-none');
});

$( window ).on( "unload", function () {
    console.log("Hiding top-nav")
    $('#top-navbar').addClass('d-lg-none');
});