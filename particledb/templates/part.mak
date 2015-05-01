<%inherit file="base.mak" />

<%namespace file="functions/manufacturer.mak" import="make_manufacturer" />

<%block name="javascript">
    <script src="${request.static_url('particledb:static/js/remove_part.js')}"></script>
    <script src="${request.static_url('particledb:static/js/edit_parameter.js')}"></script>
</%block>

<%block name="title">${part.mpn} &mdash;</%block>

<h1 class="page-header">${part.mpn}</h1>

<div class="panel panel-default">
    <div class="panel-body">
        ${part.description}
    </div>
</div>

<div class="row">
    <div class="col-md-4">
        <h3 class="page-header">Stock</h3>
        <p>None in stock</p>
    </div>
    <div class="col-md-4">
        <h3 class="page-header">Paramters</h3>
        <table class="table table-striped table-condensed">
            <tbody>
                % for param in part.parameters:
                <tr data-row-param-id="${param.id}">
                    <td>${param.key}</td>
                    <td>
                        ${param.value}
                        <a href="#" class="text-danger pull-right remove-paramter" data-id="${param.id}">
                            <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                        </a>
                    </td>
                </tr>
                % endfor
                <tr>
                    <td>
                        <input type="text">
                    </td>
                    <td>
                        <input type="text">
                    </td>
                </tr>
                <tr>
                    <td colspan="2" class="text-right">
                        <button type="button" class="btn btn-default btn-xs" aria-label="Add">
                            <span class="glyphicon glyphicon-plus" aria-hidden="true"></span>
                            Add
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="col-md-4">
    % if part.manufacturer:
        ${make_manufacturer(part.manufacturer)}
    % endif
    </div>
</div>

<form action="${request.route_path('remove_part', part_mpn=part.mpn)}" method="POST" id="remove-part-form"></form>

<p class="clearfix">
    <hr>
    <button type="button" class="btn btn-danger pull-right" id="remove-part">Remove from database</button>
</p>
