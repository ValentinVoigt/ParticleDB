var parts = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace(['mpn', 'desc']),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: js_globals.search_prefetch_url,
});

// prevents caching
parts.clear();
parts.clearPrefetchCache();
parts.initialize(true);

var addPartTemplate = function(query) {
    return '<div class="tt-suggestion">\
        <span class="glyphicon glyphicon-plus-sign" aria-hidden="true"></span>\
        <a href="' + js_globals.add_part_url + '?mpn=' + encodeURIComponent(query) + '">Add new part: <b>' + query + '</b></a>\
        </div>';
}

$('#search .typeahead').typeahead(null, {
    source: parts,
    display: 'mpn',
    templates: {
        suggestion: function(i) { return '<div><b>' + i.mpn + '</b> &mdash; ' + i.desc + '</div>'; },
        notFound: function(i) { return addPartTemplate(i.query); },
        footer: function(i) { return '<hr>' + addPartTemplate(i.query); },
    }
});

$('#search .typeahead').bind('typeahead:select', function(ev, suggestion) {
    var href = js_globals.search_dest_url.replace('__mpn__', suggestion.mpn);
    window.location.href = href;
});
