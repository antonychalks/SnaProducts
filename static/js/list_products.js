$(document).ready(function() {
    $('#navbar-burger').addClass("d-none");

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
    var sort = currentUrl.searchParams.get('sort');
    var category = currentUrl.searchParams.get('category');
    var direction = currentUrl.searchParams.get('direction');
    var search = currentUrl.searchParams.get('search');
    if (sort || category || direction || search){
        $('.btn-remove-all').removeClass('d-none');
    }
});

$('.btt-link').click(function(e) {
    window.scrollTo(0,0)
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
    currentUrl.searchParams.delete("category");
    window.location.replace(currentUrl);
})

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