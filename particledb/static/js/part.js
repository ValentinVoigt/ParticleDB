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

    $('#fileupload').fileupload({
        dataType: 'json',
        start: function (e) {
            $('#progress').removeClass('hide');
            $('#fileupload').prop('disabled', true);
            $('#fileupload').parent().find('.btn').addClass('disabled');
        },
        stop: function (e, data) {
            location.reload();
        },
        fail: function (e, data) {
            alert(data.errorThrown);
        },
        always: function(e, data) {
            $('#progress').addClass('hide');
            $('#fileupload').prop('disabled', false);
            $('#fileupload').parent().find('.btn').removeClass('disabled');
        },
        progressall: function (e, data) {
            var percentage = parseInt(data.loaded / data.total * 100, 10);
            $('#progress div.progress-bar')
                .data('aria-valuenow', percentage)
                .css('width', percentage + "%")
                .find('span.sr-only').text(percentage + "% Complete");
            if (percentage == 100)
                $('#progress div.progress-bar').addClass('progress-bar-striped active');
        },
        dropZone: $('#dropzone'),
    });

    $('.delete-file').click(function() {
        var id = $(this).data('id');
        var jqxhr = $.ajax({
            url: js_globals.delete_file_url,
            method: "POST",
            data: {id: id},
            dataType: "json",
        }).done(function(data) {
            $('div#file-'+id).fadeOut('fast', function() { $(this).remove(); });
        });
        return false;
    });

    $('#change-description').editable({
        name: 'description',
    });
});
