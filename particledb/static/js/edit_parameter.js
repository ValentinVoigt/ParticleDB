$(function() {
    $('.remove-paramter').click(function() {
        var id = $(this).attr('data-id');
        
        var jqxhr = $.ajax({
            url: js_globals.parameter_remove_url,
            method: "POST",
            data: {id: id},
            dataType: "json",
        }).fail(function(jqXHR, textStatus) {
            // TODO
            alert("failed :(");
        }).done(function(data) {
            $('tr[data-row-param-id='+id+']').fadeOut('fast', function() { $(this).remove(); });
            /* $("tr:not(.hidden)").each(function (index) {
                $(this).toggleClass("stripe", !!(index & 1));
            }); */
        });
    });
});