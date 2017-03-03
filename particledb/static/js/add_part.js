const INPUT_STATUS_NONE = 0;
const INPUT_STATUS_OKAY = 1;
const INPUT_STATUS_NOT_OKAY = 2;
const INPUT_STATUS_LOADING = 3;

function set_mpn_availability_status(status) {
    $('#mpn-form-group .form-control-feedback.glyphicon').addClass('hidden');
    $('#mpn-form-group')
        .removeClass('has-error')
        .removeClass('has-success')
        .removeClass('has-feedback');

    if (status == INPUT_STATUS_OKAY) {
        $('#mpn-form-group')
            .addClass('has-success')
            .addClass('has-feedback');
        $('#mpn-form-group .form-control-feedback.glyphicon-ok').removeClass('hidden');
    } else if (status == INPUT_STATUS_NOT_OKAY) {
        $('#mpn-form-group')
            .addClass('has-error')
            .addClass('has-feedback');
        $('#mpn-form-group .form-control-feedback.glyphicon-remove').removeClass('hidden');
    } else if (status == INPUT_STATUS_LOADING) {
        $('#mpn-form-group')
            .addClass('has-feedback');
        $('#mpn-form-group .form-control-feedback.glyphicon-option-horizontal').removeClass('hidden');
    }
}

function mpn_check_status() {
    if ($("#mpn").val().length == 0)
        return;

    var jqxhr = $.ajax({
        url: js_globals.mpn_check_url,
        method: "POST",
        data: {mpn: $('#mpn').val()},
        dataType: "json",
        beforeSend: function(jqXHR, settings) {
            set_mpn_availability_status(INPUT_STATUS_LOADING);
        },
    }).fail(function(jqXHR, textStatus) {
        set_mpn_availability_status(INPUT_STATUS_NONE);
    }).done(function(data) {
        if (data.available == 1) {
            set_mpn_availability_status(INPUT_STATUS_OKAY);
        } else {
            set_mpn_availability_status(INPUT_STATUS_NOT_OKAY);
        }
    });
}

function shorten(text) {
    if (text.length > 73) {
        return text.substring(0, 70) + "...";
    }
    return text;
}

function on_octopart_result_click() {
    $('#mpn').val($(this).data('mpn'));
    $('#description').val($(this).data('desc'));
    $('#manufacturer').val($(this).data('manufacturer'));
    mpn_check_status();
}

function process_octopart_search_results(data) {
    $('#octopart-loader').hide();
    $('#octopart-results').show();
    $('#octopart-results tbody').empty();
    $('#octopart-results tfoot').hide();

    if (!data || data.length == 0 || data.results.length == 0) {
        $('#octopart-results tfoot').show();
        return;
    }

    $(data.results).each(function(idx) {
        var glyph = $('<span>').addClass("glyphicon glyphicon-saved");
        var btn = $('<button>').attr('type', 'button').addClass('btn btn-sm btn-default').css('margin', '3px 0 0 3px').append(glyph);
        var mpn = $('<td>').text(this.item.mpn);
        var manufacturer = $('<td>').text(this.item.manufacturer.name);
        var desc = $('<td>').text(shorten(this.snippet || ""));
        btn.data('mpn', this.item.mpn).data('desc', this.snippet).data('manufacturer', this.item.manufacturer.name);
        var row = $('<tr>').append(btn, mpn, manufacturer, desc);
        $('#octopart-results tbody').append(row);
    });

    $('#octopart-results tbody tr button').click(on_octopart_result_click);
}

function do_mpn_search() {
    var mpn = $("#mpn").val();

    if (mpn.length < 3)
        return;

    $('#octopart-results').hide();
    $('#octopart-loader').show();

    $.ajax({
        type: "POST",
        url: js_globals.octopart_search_url,
        data: {'mpn': mpn},
        success: process_octopart_search_results,
    });
}

var manufacturers = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: js_globals.manufacturers_prefetch_url,
});

// prevents caching
manufacturers.clear();
manufacturers.clearPrefetchCache();
manufacturers.initialize(true);

var descriptions = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('description'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: js_globals.descriptions_prefetch_url,
});

// prevents caching
descriptions.clear();
descriptions.clearPrefetchCache();
descriptions.initialize(true);

$(function() {
    $("#mpn").blur(mpn_check_status);
    mpn_check_status();
    if ($("#mpn").val().length > 0) {
        $('#description').focus();
    } else {
        $('#mpn').focus();
    }

    $('#mpn').keypress(function (e) {
        if (e.which == 13) { // return key
            do_mpn_search();
            return false;
        }
    });

    $('#manufacturer').typeahead(null, {
        source: manufacturers,
        display: 'name',
    });
    $('#description').typeahead(null, {
        source: descriptions,
        display: 'description',
    });

    $('#octopart-results').hide();
    $('#mpn-octopart-search').click(do_mpn_search);
});
