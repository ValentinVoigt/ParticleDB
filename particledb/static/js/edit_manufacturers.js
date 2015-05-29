function xeditable_update_value(response, newValue) {
    return {newValue: response.value};
}

function xeditable_error(response, newValue) {
    return response.responseJSON.message;
}

$(function() {
    $('.editable-name').editable({success: xeditable_update_value, error: xeditable_error});
    $('.editable-url').editable({success: xeditable_update_value, error: xeditable_error});
    
    $('.logo-upload').fileupload({
        dataType: 'json',
        done: function (e, data) {
            var url = data.result.files[0].url;
            var filename = data.result.files[0].name;
            $(this).parent().find('span.btn,img').remove();
            $('<img>').attr('src', url).attr('height', 35).attr('alt', filename).insertAfter($(this));
        },
        fail: function (e, data) {
            alert(data.errorThrown);
        },
    });
});