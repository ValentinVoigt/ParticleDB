$(function() {
    $('.remove-paramter').click(function() {
        var id = $(this).attr('data-id');
        bootbox.confirm({
            message: "Do you really want to delete this parameter?",
            size: 'small',
            callback: function(result) {
                if (result) {
                    var jqxhr = $.ajax({
                        url: js_globals.parameter_remove_url,
                        method: "POST",
                        data: {id: id},
                        dataType: "json",
                    }).done(function(data) {
                        $('tr[data-row-param-id='+id+']').fadeOut('fast', function() { $(this).remove(); });
                    });
                }
            },
        });
    });
    
    $('#btn-edit').click(function() {
        $(this).toggleClass('active');
        $('.remove-paramter').toggleClass('hidden');
        $('#btn-add-row').toggleClass('hidden');
        $('.editable-key, .editable-value').editable('toggleDisabled');
    });
    
    $('.editable-key').editable({
        params: function(params) {
            params.col = 'key';
            return params;
        }
    }).editable('toggleDisabled');
    $('.editable-value').editable({
        params: function(params) {
            params.col = 'value';
            return params;
        }
    }).editable('toggleDisabled');
});