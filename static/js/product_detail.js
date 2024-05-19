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

    var productId = $('.qty-input').data("product_id")
    let decrementButtons = $('.qty-change[data-change="decrement"]');
    let incrementButtons = $('.qty-change[data-change="increment"]');

    // Function to disable the buttons at the appropriate times
    function setButtonsDisplay(productId) {
        let quantity = parseInt($('.qty-input').val(), 10);
    
        if (quantity < 2) {
            decrementButtons.each(function() {
                $(this).prop('disabled', true);
            });
        } else if (quantity > 98) {
            incrementButtons.each(function() {
                $(this).prop('disabled', true);
            });
        } else {
            decrementButtons.each(function() {
                $(this).prop('disabled', false);
            });
            incrementButtons.each(function() {
                $(this).prop('disabled', false);
            });
        }
    }

    // Displays the price with the quantity multiplier
    function displayPriceQty(){
        if ($('.qty-input').val() > 1){
            let originalPrice = parseFloat($('#product_price').text());
            let quantity = parseInt($('.qty-input').val());
            let newPrice = originalPrice * quantity;
            let productDelivery = parseFloat($('#product-delivery').text());
            let productDeliveryQty = productDelivery * quantity
            let minHalfDelivery = parseInt($('#min_half_delivery').text());
            let minFreeDelivery = parseInt($('#min_free_delivery').text());
            let halfDelivery = productDeliveryQty/2

            if (newPrice >= minFreeDelivery){
                $('#qty-delivery').text("Free delivery!");
                
            } else if (newPrice >= minHalfDelivery){
                $('#qty-delivery').text("+£" + halfDelivery);
            } else {
                $('#qty-delivery').text("+£" + productDeliveryQty)
            }

            $('#product_qty_price').text(newPrice.toFixed(2));
            $('.price_qty').removeClass("d-none");
        }
    }

    // Calls the function on page load to check if the quantity is already more than one, and displays the pirce if applicable.
    displayPriceQty()

    // Checks if the button needs to be displayed and the quantity price needs to be displayed whenever the input changes.
    $('.qty-input').change(function() {
        var itemId = $(this).data('item_id');
        setButtonsDisplay(productId);
        displayPriceQty();
    });

    // Increments the quantity
    $(incrementButtons).on("click", function(e){
        e.preventDefault();
        buttonValue =  parseInt($(this).find('i').text().trim(), 10);
        var closestInput = $(this).closest('.input-group').find('.qty-input')[0];
        let quantity = parseInt($(closestInput).val())
        if (quantity + buttonValue > 99){
            $(closestInput).val(99);
            displayPriceQty();
            setButtonsDisplay(productId);
        } else {
            $(closestInput).val(quantity + buttonValue);
            displayPriceQty();
            setButtonsDisplay(productId);
        }
    })

    // Decrements the quantity
    $(decrementButtons).on("click", function(e){
        e.preventDefault();
        buttonValue =  parseInt($(this).find('i').text().trim(), 10);
        var closestInput = $(this).closest('.input-group').find('.qty-input')[0];
        let quantity = parseInt($(closestInput).val())
        if (quantity - buttonValue < 1){
            $(closestInput).val(1);
            displayPriceQty();
            setButtonsDisplay(productId);
        } else {
            $(closestInput).val(quantity - buttonValue);
            displayPriceQty();
            setButtonsDisplay(productId);
        }
    })

});

$( window ).on( "unload", function () {
    $('#top-navbar').addClass('d-lg-none');
});
