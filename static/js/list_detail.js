$(document).ready(function () {
    // Remove item and reload on click. Credit: Code institute Project Boutique_Ado
    $('.remove-button').click(function (e) {
        var csrfToken = $(this).data('csrf_token');
        var itemId = $(this).attr('id').split('remove_')[1]; //Gets the second half of the update link.
        var url = `/list/remove_from_list/${itemId}/`; //Creates the url to be removed.
        var data = {'csrfmiddlewaretoken': csrfToken};

        $.post(url, data) // Posts the data to the url written above.
            .done(function () {
                location.reload(); // once it's done, the webpage is reloaded.
            });
    });

    const productId = $('.qty-input').data("product_id")

    function setButtonsDisplay() {
        let quantity = parseInt($('.qty-input').val(), 10);
        let buttonIncrement = $('.btn-increment')
        let buttonDecrement = $('.btn-decrement')


        if (quantity < 2) {
            buttonDecrement.prop('disabled', true);
        } else if (quantity > 98) {
            buttonIncrement.prop('disabled', true);
        } else {
            buttonDecrement.prop('disabled', false);
            buttonIncrement.prop('disabled', false);
        }
    }

    setButtonsDisplay()

    $('.qty-input').change(function() {
        var itemId = $(this).data('item_id');
        displayPriceQty();
    });

    // Increments the quantity
    $('.btn-increment').on("click", function(e){
        console.log("Increment button clicked")
        e.preventDefault();
        const input = $('.qty-input');
        let quantity = parseInt($(input).val())
        if (quantity + 1 > 99){
            $(input).val(99);
        } else {
            $(input).val(quantity + 1);
            setButtonsDisplay()
        }
    })

    // Decrements the quantity
    $('.btn-decrement').on("click", function(e){
        console.log("Decrement button clicked")
        e.preventDefault();
        const input = $('.qty-input');
        let quantity = parseInt($(input).val())
        if (quantity - 1 < 1){
            $(input).val(1);
        } else {
            $(input).val(quantity - 1);
            setButtonsDisplay()
        }
    })
});
