<%inherit file="base.mak" />

<%namespace file="functions/manufacturer.mak" import="make_manufacturer" />

<%block name="javascript">
    <script src="${request.static_url('particledb:static/js/part.js')}"></script>
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
        <h4>
            Downloads

            <label for="fileupload" class="pull-right" style="cursor:pointer">
                <input class="hide" id="fileupload" type="file" name="files[]" data-url="${request.route_path('upload_file', part_id=part.id)}" multiple>
                <span class="btn btn-xs btn-default">
                    <span class="glyphicon glyphicon-upload" aria-hidden="true"></span>
                    Upload
                </span>
            </label>
        </h4>
        <div id="files">
        % for file in part.files:
            <div class="dropdown" id="file-${file.id}">
                <a href="${request.route_path('uploaded_file', uuid=file.uuid)}">
                    ${file.filename}
                </a>
                <a class="dropdown-toggle" data-toggle="dropdown">
                    <span class="caret" aria-expanded="true"></span>
                </a>
                (${file.formatted_size})
                
                <ul class="dropdown-menu" role="menu">
                    <li><a role="menuitem" tabindex="-1" href="#" class="delete-file" data-id="${file.id}">Delete</a></li>
                </ul>
            </div>
        % endfor
        </div>

        % if len(part.files) == 0:
            <p><i>none</i></p>
        % endif
        
        <div class="progress hide" id="progress">
            <div class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%">
                <span class="sr-only">0% Complete</span>
            </div>
        </div>
        <br>
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
        <table class="table table-striped table-condensed" id="table-parameters" data-part-id="${part.id}">
            <thead>
                <tr>
                    <th>Storage</th>
                    <th>Cell</th>
                    <th>Quantity</th>
                    <th>Package</th>
                </tr>
            </thead>
            <tbody>
                % if len(part.stocks) == 0:
                    <td colspan="4" class="text-center">None in stock</td>
                % else:
                    % for stock in part.stocks: 
                    <tr>
                        <td>${stock.cell.storage.name}</td>
                        <td>${stock.cell.number}</td>
                        <td>${stock.quantity}</td>
                        % if stock.package:
                            <td>${stock.package.name}</td>
                        % else:
                            <td>&mdash;</td>
                        % endif
                    </tr>
                    % endfor
                % endif
            </tbody>
        </table>
    </div>
</div>

<p class="clearfix"><hr></p>

% if not part.in_stock:
    <form action="${request.route_path('remove_part', part_mpn=part.mpn)}" method="POST" id="remove-part-form">
        <button type="button" class="btn btn-danger pull-right" id="remove-part">Remove from database</button>
    </form>
% endif