$(function() {
    $('#remove-part').click(function() {
        bootbox.confirm({
            message: "Are you <b>sure</b>?",
            size: 'small',
            callback: function(result) {
                if (result) {
                    $('#remove-part-form').submit();
                }
            }}
        ); 
    });
});