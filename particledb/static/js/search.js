var parts = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('mpn'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: js_globals.search_prefetch_url,
});
 
// prevents caching
parts.clear();
parts.clearPrefetchCache();
parts.initialize(true);
 
$('#search .typeahead').typeahead(null, {
    source: parts,
    display: 'mpn',
    templates: {
        suggestion: function(i) { return '<div><b>' + i.mpn + '</b> &mdash; ' + i.desc + '</div>'; },
    }
});

$('#search .typeahead').bind('typeahead:select', function(ev, suggestion) {
    var href = js_globals.search_dest_url.replace('__mpn__', suggestion.mpn);
    window.location.href = href;
});