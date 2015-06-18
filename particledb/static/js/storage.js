function is_digit(val) {
    var patt = /[0-9]+/;
    return patt.test(val);
}

function form_is_valid() {
    var name = $('#storage-name').val();
    var columns = $('#storage-columns').val();
    var rows = $('#storage-rows').val();
    var valid = true;

    $('#error-message').addClass('hidden');

    /* Name */
    if (name.length > 0) {
        $('#storage-name').closest('div.form-group').removeClass('has-error');
    } else {
        $('#storage-name').closest('div.form-group').addClass('has-error');
        valid = false;
    }

    /* Columns */
    if (is_digit(columns) && columns > 0) {
        $('#storage-columns').closest('div.form-group').removeClass('has-error');
    } else {
        $('#storage-columns').closest('div.form-group').addClass('has-error');
        valid = false;
    }

    /* Rows */
    if (is_digit(rows) & rows > 0) {
        $('#storage-rows').closest('div.form-group').removeClass('has-error');
    } else {
        $('#storage-rows').closest('div.form-group').addClass('has-error');
        valid = false;
    }

    return valid;
}

function disable_form() {
    $('#storage-form input,#btn-save,#btn-cancel').prop('disabled', true).addClass('disabled');
    $('#loader').removeClass('hidden');
}

function enable_form() {
    $('#storage-form input,#btn-save,#btn-cancel').prop('disabled', false).removeClass('disabled');
    $('#loader').addClass('hidden');
}

function ajax_save() {
    var jqxhr = $.ajax({
        url: js_globals.storage_add_url,
        method: "POST",
        data: {
            name: $('#storage-name').val(),
            width: $('#storage-columns').val(),
            height: $('#storage-rows').val(),
        },
        dataType: "json",
        beforeSend: disable_form,
    }).always(enable_form).done(function(data) {
        if (!data.status) {
            $('#error-message').text(data.message).removeClass('hidden');
        } else {
            window.location = js_globals.storage_url;
        }
    });
}

function on_btn_save_click() {
    if (form_is_valid()) {
        ajax_save();
    }
}

function on_remove_storage_click() {
    var that = $(this);

    bootbox.confirm({
        message: "Do you really want to delete this storage container?",
        size: 'small',
        callback: function(result) {
            if (result) {
                that.closest('form').submit();
            }
        },
    });

    /* prevent scrolling */
    return false;
}

$(function() {
    $('#btn-save').click(on_btn_save_click);
    $('.remove-storage').click(on_remove_storage_click);
});
