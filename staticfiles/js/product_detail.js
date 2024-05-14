$(document).ready(function () {
    $('#top-navbar').removeClass('d-lg-none');

    let imgEnlarged = false

    $('.zoom-overlay').on("click", function() {
        $('.enlarge-img').toggleClass("d-none");
        imgEnlarged = true;
    });

    $('.enlarge-img').on("click", function(event) {
        if (event.target.nodeName != "img") {
            $('.enlarge-img').toggleClass("d-none");
        }
    });

});

$( window ).on( "unload", function () {
    $('#top-navbar').addClass('d-lg-none');
});

