$(document).ready(function() {
    $('#navbar-burger').addClass("d-none");

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
    var manageSearch = currentUrl.searchParams.get('manage_search');
    if (sort || category || direction || manageSearch){
        $('.btn-remove-all').removeClass('d-none');
    }
});

$('.top-button').click(function(e) {
    window.scrollTo(0,0)
})

$('.scroll-up').click(function(e){
    window.scrollBy(0, -777.6)
})

$('.scroll-down').click(function(e){
    window.scrollBy(0, 777.6)
})

$('#category-selector').change(function(){
    const selector = $(this);
    const categoryId = selector.val();
    const newPathname = `/products/edit_category/${categoryId}/`;
    window.location.pathname = newPathname; // Set the new URL
    console.log(window.location.pathname);
})

$('.btn-remove-search').click(function(){
    var currentUrl = new URL(window.location);
    currentUrl.searchParams.delete("manage_search");
    window.location.replace(currentUrl);
})

$('.btn-remove-category').click(function(){
    var currentUrl = new URL(window.location);

    var current_categories = [];
    var categories_displayed = $('.btn-remove-category');
    let thisCategory = $(this).data("category");

    if (categories_displayed.length > 1){
        if ($(this).data("type") == 0) {
            currentUrl.searchParams.delete("category")
        } else {
            for (let i = 0; i < categories_displayed.length; i++) {

                if ($(categories_displayed[i]).data("type") == 1){

                    if ($(categories_displayed[i]).data("category") != thisCategory){
                        let category = $(categories_displayed[i]).data("category");
                        current_categories.push(category);
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
    currentUrl.searchParams.delete("manage_search");
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