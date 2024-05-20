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

    let qtyChangeButtons = $('.cart-qty-change');
    let qtyInputs = $('.cart-qty-input');
    let qtyPriceElements = $('.product_qty_price');
    let buttonMap = {};
    let decrementMap = {};
    let incrementMap = {};
    let qtyInputMap = {};
    let qtyPriceMap = {};

    
    function populateMapList() {
        buttonMap = {};
        decrementMap = {};
        incrementMap = {};
        qtyInputMap = {};
        qtyPriceMap = {};
    
        //Populates button map, decrement map and increment map with the increment and decrement buttons.
        for (let i = 0; i < qtyChangeButtons.length; i++) {
            let button = $(qtyChangeButtons[i]);
            let change = $(qtyChangeButtons[i]).data("change")
            let id = $(qtyChangeButtons[i]).data("id");
            let buttonObject = {
                button: button,
                id : id,
                change : change
            }
            if (change == "decrement"){
                decrementMap[id] = buttonObject;
                buttonMap[id] = buttonObject;
            } else if (change == "increment"){
                incrementMap[id] = buttonObject;
                buttonMap[id] = buttonObject;
            } else {
                throw new Error("Button has no change data.");
            }
            buttonMap[id] = buttonObject;
        }
    
        //Populates the qty input map with qty inputs.
        for (let i = 0; i < qtyInputs.length; i++){
            let button = $(qtyInputs[i]);
            var id = $(button).data("id");
            let value = $(qtyInputs[i]).val();
            let inputObject = {
                button: button,
                id : id,
                value : value
            }
            
            qtyInputMap[id] = inputObject;
        }

        //Populates the qty price map.
        for (let i = 0; i < qtyPriceElements.length; i++){
            var id = $(qtyPriceElements[i]).data("id");
            var price = $(qtyPriceElements[i]).data("price");
            let element = $(qtyPriceElements[i]);
            let qtyPriceObject = {
                id : id,
                price : price,
                element : element
            };
            qtyPriceMap[id] = qtyPriceObject;
        }
    }
    
    // Function to disable the buttons at the appropriate times
    function setButtonsDisplay(productId) {
        let decrementButton = decrementMap[productId];
        let incrementButton = incrementMap[productId];
        let inputObject = qtyInputMap[productId];
        let quantity = parseInt(inputObject.value);
        if (quantity == 1) {
            $(decrementButton.button).prop('disabled', true);
        } else if (quantity == 99) {
            $(incrementButton.button).prop('disabled', true);
        } else {
            $(decrementButton.button).prop('disabled', false);
            $(incrementButton.button).prop('disabled', false);
        }
    }
    
    // Displays the price with the quantity multiplier
    function displayPriceQty(){
        console.log("setting price qty display", "qtyInputMap[id]: ", qtyInputMap)
        Object.keys(qtyInputMap).forEach(id => {
            if (qtyInputMap[id].value > 1){
                let quantity = qtyInputMap[id].value;
                let price = qtyPriceMap[id].price;
                let newPrice = price * quantity;
                qtyPriceMap[id].element.parent().removeClass("d-none");
                qtyPriceMap[id].element.text(newPrice.toFixed(2))
            } else if (qtyInputMap[id].value == 1){
                qtyPriceMap[id].element.parent().addClass("d-none");
            }
            setButtonsDisplay(id);
        });
    }
    
    // Checks if the button needs to be displayed and the quantity price needs to be displayed whenever the input changes.
    $('.cart-qty-input').change(function() {
        var productId = $(this).data('product_id');
        setButtonsDisplay(productId);
        displayPriceQty();
    });
    
    // Increments the quantity
    $('.cart-qty-change').on("click", function(e){
        e.preventDefault();
        var productId = $(this).data('id');
        var change = $(this).data('change');
        var amount = parseInt($(this).data('amount'));
        let inputObject = qtyInputMap[productId];
        let button = inputObject.button;
        let quantity = parseInt(button.val());
    
        if (!isNaN(quantity)) {
            if (change === "decrement"){
                if (quantity - amount < 1){
                    button.val(1);
                    inputObject.value = 1;
                } else {
                    button.val(quantity - amount);
                    inputObject.value = quantity - amount;
                }
            } else if (change === "increment"){
                if (quantity + amount > 99){
                    button.val(99);
                    inputObject.value = 99;
                } else {
                    button.val(quantity + amount);
                    inputObject.value = quantity + amount;
                }
            }

            displayPriceQty();
            setButtonsDisplay(productId);
        } else {
            console.error("Invalid quantity value:", inputObject.text());
        }
    })

    // Update quantity on click Credit: Code institute Project Boutique_Ado
    $('.update-button').click(function(e) {
        var form = $(this).prev('.update_form');
        form.submit();
    })

    // Remove item and reload on click. Credit: Code institute Project Boutique_Ado
    $('.remove-button').click(function(e) {
        var csrfToken = "{{ csrf_token }}";
        var itemId = $(this).attr('id').split('remove_')[1]; //Gets the second half of the update link.
        var size = $(this).data('size'); //data-size attribute from html element.
        var url = `/bag/remove/${itemId}`; //Creates the url to be removed.
        var data = {'csrfmiddlewaretoken': csrfToken, 'size': size}; 

        $.post(url, data) // Posts the data to the url written above.
            .done(function() { 
                location.reload(); // once its done the webpage is reloaded.
            });
    })

    // Populates the map lists after everything is loaded.
    populateMapList();

    // Shows the total price attached to a product if the qty is more than one.
    displayPriceQty()

    //Iterates through the buttons to check if they need to be disabled.
    Object.keys(qtyInputMap).forEach(id => {
        setButtonsDisplay(id);
    });
});
    
$( window ).on( "unload", function () {
    $('#top-navbar').addClass('d-lg-none');
});