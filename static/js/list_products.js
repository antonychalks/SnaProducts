$(document).ready(function() {
    $('#navbar-burger').addClass("d-none");

    // Image overlay
    let imgEnlarged = false
    let productId = ""

    $('.zoom-overlay').on("click", function(e) {
        e.preventDefault()
        let productId = $(this).data("product_id");
        console.log(productId)
        let englargeImg = $(`#enlarge-img-${productId}`)
        console.log(englargeImg)
        englargeImg.toggleClass("d-none");
        imgEnlarged = true;
    });

    $('.enlarge-img').on("click", function(event) {
        let enlargeImg = $('.enlarge-img');
        if (event.target.nodeName != "img") {
            for (let i = 0; i < enlargeImg.length; i++){
                if (!$(enlargeImg[i]).hasClass("d-none")){
                    $(enlargeImg[i]).addClass("d-none");
                    imgEnlarged = false;
                }
            }
        }
    });

    // Checks if the buttons are active and gives the active class to them
    var currentUrl = new URL(window.location);
    var direction = currentUrl.searchParams.get("direction");
    if(direction == "asc"){
        $('#button-asc').addClass("direction-active");
        $('#button-desc').removeClass("direction-active");
    } else if(direction == "desc"){
        $('#button-desc').addClass("direction-active");
        $('#button-asc').removeClass("direction-active");
    } else {
        $('#button-asc').removeClass("direction-active");
        $('#button-desc').removeClass("direction-active");
    }

    // Displays the remove all button if any filters or sorts are active.
    var sort = currentUrl.searchParams.get('sort');
    var category = currentUrl.searchParams.get('category');
    var direction = currentUrl.searchParams.get('direction');
    var search = currentUrl.searchParams.get('search');
    if (sort || category || direction || search){
        $('.btn-remove-all').removeClass('d-none');
    }
});

$('.top-button').click(function(e) {
    window.scrollTo(0,0)
})

$('.arrow-up').click(function(e){
    let cardHeight = $('.product-card').height() + 16;
    window.scrollBy(0, -cardHeight)
})

$('.arrow-down').click(function(e){
    let cardHeight = $('.product-card').height() + 16;
    window.scrollBy(0, cardHeight)
})

$('#sort-selector').change(function(){
    var selector = $(this)
    var currentUrl = new URL(window.location);
    var selectedVal = selector.val();

    if(selectedVal != "reset"){
        var sort = selectedVal;
        currentUrl.searchParams.set("sort", sort);
        window.location.replace(currentUrl);
    } else {
        currentUrl.searchParams.delete("sort");
        window.location.replace(currentUrl);
    }
})

$('.btn-remove-search').click(function(){
    var currentUrl = new URL(window.location);
    currentUrl.searchParams.delete("search");
    window.location.replace(currentUrl);
})

$('.btn-remove-category').click(function(){
    var currentUrl = new URL(window.location);

    var current_categories = [];
    var categories_displayed = $('.btn-remove-category');
    let thisCategory = $(this).data("category");
    console.log(thisCategory)

    if (categories_displayed.length > 1){
        if ($(this).data("type") == 0) {
            currentUrl.searchParams.delete("category")
            console.log("Deleting Category")
        } else {
            for (let i = 0; i < categories_displayed.length; i++) {

                if ($(categories_displayed[i]).data("type") == 1){

                    if ($(categories_displayed[i]).data("category") != thisCategory){
                        let category = $(categories_displayed[i]).data("category");
                        current_categories.push(category);
                    } else {
                        console.log("removing ", categories_displayed[i])
                    }

                }
            }

            let newCategories = current_categories.filter(word => word != thisCategory)
            newCategories = current_categories.join(',');
    
            currentUrl.searchParams.set("category", newCategories);    
        }
    } else {
        currentUrl.searchParams.delete("category")
    }
    window.location.replace(currentUrl);
});

$('.btn-remove-sort').click(function(){
    var currentUrl = new URL(window.location);
    currentUrl.searchParams.delete("sort");
    currentUrl.searchParams.delete("direction");
    window.location.replace(currentUrl);
})

$('.btn-remove-all').click(function(){
    var currentUrl = new URL(window.location);
    currentUrl.searchParams.delete("sort");
    currentUrl.searchParams.delete("direction");
    currentUrl.searchParams.delete("category");
    currentUrl.searchParams.delete("search");
    window.location.replace(currentUrl);
})

$('#button-asc').click(function(){
    var currentUrl = new URL(window.location);
    currentUrl.searchParams.set("direction", "asc");
    window.location.replace(currentUrl);
})

$('#button-desc').click(function(){
    var currentUrl = new URL(window.location);
    currentUrl.searchParams.set("direction", "desc");
    window.location.replace(currentUrl);
})