function setup_parameter_editable(editable, key_or_value) {
    if (key_or_value == 'key') {
        editable.on('hidden.nextfield', function(event, reason) {
            if (reason == 'save') {
                $(this).closest('td').next().find('.editable').editable('show');
            }
        });
    }

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
                    $('#table-parameters tbody').sortable('reload');
                    $(this).closest('tr').find('.parameter-sort').removeClass('text-muted');
                } else {
                    // TODO
                    $(this).closest('tr').addClass('danger');
                }
            },
        });
    }
}

function save_parameter_order() {
    var order = [];
    $('tr[data-row-param-id]').each(function() {
        order.push($(this).attr('data-row-param-id'));
    });

    var jqxhr = $.ajax({
        url: js_globals.parameter_reorder_url,
        method: "POST",
        data: {part: $('table[data-part-id]').data('part-id'), order: order.join()},
        dataType: "json",
    });
}

$(function() {
    $('.remove-parameter').click(on_remove_parameter_click);
    
    $('#btn-edit').click(function() {
        $(this).toggleClass('active');
        $('.remove-parameter, .parameter-sort, #btn-add-row').toggleClass('hidden');
        $('.editable-key, .editable-value').editable('toggleDisabled');
        
        if ($(this).hasClass('active')) {
            $("#table-parameters tbody").sortable('enable');
        } else {
            $('.empty-parameter').remove();
            $("#table-parameters tbody").sortable('disable');
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
    
    $("#table-parameters tbody").sortable({
        sortableClass: 'info',
        forcePlaceholderSize: true,
        handle: 'span.parameter-sort',
        items: 'tr:not(#new-parameter-template,#dummy-parameter,#btn-add-row)',
    }).sortable('disable').bind('sortupdate', function(e, ui) {
        save_parameter_order();
    });
    
    setup_parameter_editable($('.editable-key'), 'key').editable('toggleDisabled');
    setup_parameter_editable($('.editable-value'), 'value').editable('toggleDisabled');
});