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

});
