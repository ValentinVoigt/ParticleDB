function setup_parameter_editable(editable, key_or_value) {
    return editable.editable({
        name: key_or_value,
    });
}

function remove_parameter(id) {
    var jqxhr = $.ajax({
        url: js_globals.parameter_remove_url,
        method: "POST",
        data: {id: id},
        dataType: "json",
    }).done(function(data) {
        $('tr[data-row-param-id='+id+']').fadeOut('fast', function() { $(this).remove(); });
    });
}

function on_remove_parameter_click() {
    var id = $(this).attr('data-id');
    
    if (!id) {
        // new (empty) parameter
        $(this).closest('tr').fadeOut('fast', function() { $(this).remove(); });
    } else {
        bootbox.confirm({
            message: "Do you really want to delete this parameter?",
            size: 'small',
            callback: function(result) {
                if (result) {
                    remove_parameter(id);
                }
            },
        });
    }
    
    return false; // prevent scrolling
}

function check_if_both_are_filled(e, reason) {
    if (reason != 'save')
        return;

    var key = $(this).closest('tr').find('.editable-key').editable('getValue', true);
    var value = $(this).closest('tr').find('.editable-value').editable('getValue', true);
    
    if (key.length  > 0 && value.length > 0) {
        $(this).closest('tr').find('.editable').editable('submit', {
            url: js_globals.parameter_add_url,
            ajaxOptions: {
                dataType: 'json',
            },
            data: {part: $('table[data-part-id]').data('part-id')},
            success: function(data, config) {
                if (data && data.id) {
                    var editables = $(this).closest('tr').find('.editable');
                    editables.removeClass('editable-unsaved').off('hidden.add_new').editable('option', 'pk', data.id);
                    $(this).closest('tr').find('a.remove-parameter').attr('data-id', data.id);
                    $(this).closest('tr').removeClass('empty-parameter').attr('data-row-param-id', data.id);
                } else {
                    // TODO
                    $(this).closest('tr').addClass('danger');
                }
            },
        });
    }
}

$(function() {
    $('.remove-parameter').click(on_remove_parameter_click);
    
    $('#btn-edit').click(function() {
        $(this).toggleClass('active');
        $('.remove-parameter').toggleClass('hidden');
        $('#btn-add-row').toggleClass('hidden');
        $('.editable-key, .editable-value').editable('toggleDisabled');
        
        if (!$(this).hasClass('active')) {
            $('.empty-parameter').remove();
        }
    });
    
    $('#btn-add').click(function() {
        var template = $('#new-parameter-template').clone();
        template.removeClass('hidden').removeAttr('id').addClass('empty-parameter');
        template.find('.remove-parameter').click(on_remove_parameter_click);
        template.find('a.editable').first().addClass('editable-key');
        template.find('a.editable').last().addClass('editable-value');
        setup_parameter_editable(template.find('.editable-key'), 'key');
        setup_parameter_editable(template.find('.editable-value'), 'value');
        template.find('.editable-key').on('hidden.add_new', check_if_both_are_filled);
        template.find('.editable-value').on('hidden.add_new', check_if_both_are_filled);
        $('#table-parameters tr:last').before(template);
    });
    
    setup_parameter_editable($('.editable-key'), 'key').editable('toggleDisabled');
    setup_parameter_editable($('.editable-value'), 'value').editable('toggleDisabled');
});