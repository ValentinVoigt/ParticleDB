function xeditable_update_value(response, newValue) {
    return {newValue: response.value};
}
function xeditable_error(response, newValue) {
    return response.responseJSON.message;
}

$(function() {
    $('.editable-name').editable({success: xeditable_update_value, error: xeditable_error});
    $('.editable-url').editable({success: xeditable_update_value, error: xeditable_error});
});