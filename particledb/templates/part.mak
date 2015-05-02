<%inherit file="base.mak" />

<%namespace file="functions/manufacturer.mak" import="make_manufacturer" />

<%block name="javascript">
    <script src="${request.static_url('particledb:static/js/remove_part.js')}"></script>
    <script src="${request.static_url('particledb:static/js/edit_parameter.js')}"></script>
    <script src="${request.static_url('particledb:static/js/dist/html5sortable/html.sortable.min.js')}"></script>
</%block>

<%block name="title">${part.mpn} &mdash;</%block>

<h1 class="page-header">${part.mpn}</h1>

<div class="row">
    <div class="col-md-8">
        <div class="panel panel-default">
            <div class="panel-body">
                ${part.description}
            </div>
        </div>
    </div>
    
    <div class="col-md-4">
        % if part.manufacturer:
            ${make_manufacturer(part.manufacturer)}
        % endif
    </div>
</div>

<div class="row">
    <div class="col-md-6">
        <h3 class="page-header">
            Parameters
            <button type="button" class="btn btn-default btn-xs pull-right" id="btn-edit" aria-label="Edit">
                <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
                Edit
            </button>
        </h3>
        <table class="table table-striped table-condensed" id="table-parameters" data-part-id="${part.id}">
            <colgroup>
                <col width="40%">
                <col width="60%">
            </colgroup>
            <tbody>
                <!-- Template for new entries. Copied by JavaScript -->
                <tr class="hidden" id="new-parameter-template">
                    <td>
                        <span class="glyphicon glyphicon-sort hidden parameter-sort text-muted" aria-hidden="true"></span>
                        <a href="#" class="editable" data-type="text" data-url="${request.route_path('parameter_edit')}" data-title="Change key"></a>
                    </td>
                    <td>
                        <a href="#" class="editable" data-type="text" data-url="${request.route_path('parameter_edit')}" data-title="Change value"></a>
                        <a href="#" class="text-danger pull-right remove-parameter hidden">
                            <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                        </a>
                    </td>
                </tr>
                <!-- Dummy row to restore even table striping -->
                <tr class="hidden" id="dummy-parameter"><td colspan="2"></td></tr>
                % for param in part.parameters:
                <tr data-row-param-id="${param.id}">
                    <td>
                        <span class="glyphicon glyphicon-sort hidden parameter-sort" aria-hidden="true"></span>
                        <a href="#" class="editable editable-key" data-type="text" data-pk="${param.id}" data-url="${request.route_path('parameter_edit')}" data-title="Change key">
                            ${param.key}
                        </a>
                    </td>
                    <td>
                        <a href="#" class="editable editable-value" data-type="text" data-pk="${param.id}" data-url="${request.route_path('parameter_edit')}" data-title="Change value">
                            ${param.value}
                        </a>
                        <a href="#" class="text-danger pull-right remove-parameter hidden" data-id="${param.id}">
                            <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                        </a>
                    </td>
                </tr>
                % endfor
                <tfoot>
                    <tr id="btn-add-row" class="hidden active">
                        <td colspan="2" class="text-right">
                            <button type="button" class="btn btn-default btn-xs" id="btn-add" aria-label="Add">
                                <span class="glyphicon glyphicon-plus" aria-hidden="true"></span>
                                Add
                            </button>
                        </td>
                    </tr>
                </tfoot>
            </tbody>
        </table>
    </div>
    <div class="col-md-6">
        <h3 class="page-header">Stock</h3>
        <p>None in stock</p>
    </div>
</div>

<form action="${request.route_path('remove_part', part_mpn=part.mpn)}" method="POST" id="remove-part-form"></form>

<p class="clearfix">
    <hr>
    <button type="button" class="btn btn-danger pull-right" id="remove-part">Remove from database</button>
</p>
