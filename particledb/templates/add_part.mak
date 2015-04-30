<%inherit file="base.mak" />

<%block name="title">Add part &mdash;</%block>

<h1 class="page-header">Add part</h1>

% if error:
    <div class="alert alert-danger" role="alert">${error|nl2br,n}</div>
% endif

% if success:
    <div class="alert alert-success" role="alert">New part has been added to the database! <a href="${request.route_path('part', part_mpn=new_part.mpn)}">Goto ${new_part.mpn}</a></div>
% endif

<p>Use this form to add a new part to the database. Go to <a href="#">Stock</a> to change items in stock!</p>

<br>

<%block name="javascript">
    <script src="${request.static_url('particledb:static/js/add_part.js')}"></script>
</%block>

<form class="form-horizontal" method="POST" action="${request.route_path('add_part')}">
    <div class="form-group" id="mpn-form-group">
        <label for="mpn" class="col-sm-2 control-label">
            MPN
            <span class="text-muted">*</span>
            <span class="glyphicon glyphicon-question-sign" aria-hidden="true" data-toggle="tooltip" data-placement="top" title="Manufacturer's Part Number, e.g. NE555"></span>
        </label>
        <div class="col-sm-4">
            <input type="text" class="form-control" id="mpn" name="mpn" placeholder="MPN" value="${defaults.get('mpn', '')}">
            <span class="glyphicon glyphicon-ok form-control-feedback hidden" aria-hidden="true" id="mpn-glyphicon-ok"></span>
            <span class="glyphicon glyphicon-remove form-control-feedback hidden" aria-hidden="true" id="mpn-glyphicon-remove"></span>
            <span class="glyphicon glyphicon-option-horizontal form-control-feedback hidden" aria-hidden="true" id="mpn-glyphicon-refresh"></span>
            <span class="sr-only">(success)</span>
        </div>
    </div>
    <div class="form-group">
        <label for="description" class="col-sm-2 control-label">Description</label>
        <div class="col-sm-4">
            <input type="text" class="form-control" id="description" name="description" placeholder="Description" value="${defaults.get('description', '')}">
        </div>
    </div>
    <div class="form-group">
        <label for="manufacturer" class="col-sm-2 control-label typeahead">Manufacturer</label>
        <div class="col-sm-4">
            <input type="text" class="form-control" id="manufacturer" name="manufacturer" placeholder="Manufacturer" value="${defaults.get('manufacturer', '')}">
        </div>
    </div>
    <div class="form-group">
        <div class="col-sm-offset-2 col-sm-4">
            <button type="submit" class="btn btn-primary">Add to database</button>
        </div>
    </div>
</form>
