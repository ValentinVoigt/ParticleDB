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

var manufacturers = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: js_globals.manufacturers_prefetch_url,
});
 
// prevents caching
manufacturers.clear();
manufacturers.clearPrefetchCache();
manufacturers.initialize(true);

$(function() {
    $("#mpn").blur(mpn_check_status);
    if ($("#mpn").val().length > 0) {
        mpn_check_status();
        $('#description').focus();
    } else {
        $('#mpn').focus();
    }
    
    $('#manufacturer').typeahead(null, {
        source: manufacturers,
        display: 'name',
    });
});