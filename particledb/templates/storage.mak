<%inherit file="base.mak" />

## <%namespace file="functions/manufacturer.mak" import="make_manufacturer" />

<%block name="javascript">
    <script src="${request.static_url('particledb:static/js/storage.js')}"></script>
</%block>

<%block name="title">Storage &mdash;</%block>

<h1 class="page-header">
    Storage
    <button type="button" class="btn btn-default pull-right" data-toggle="modal" data-target="#add-storage-modal">
        <span class="glyphicon glyphicon-plus" aria-hidden="true"></span>
        Add
    </button>
</h1>

% for storage in storages:
<div class="pull-left" style="margin:0 30px 30px 0">
    <div class="panel panel-default panel-primary">
        <div class="panel-heading">
            ${storage.name}
            % if storage.is_empty:
                <form action="${request.route_path('storage_remove')}" method="POST" class="pull-right">
                    <input type="hidden" name="id" value="${storage.id}">
                    <a href="#" class="remove-storage" style="color:white">
                        <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                    </a>
                </form>
            % endif
        </div>
        <table class="table table-bordered">
            % for row in storage.iter_rows():
            <tr>
                % for cell in row.iter_cells():
                <td class="vert-align text-center
                    % if len(cell.stocks) > 0:
                        info
                    % endif
                " style="width:45px; height:40px;">
                    ${cell.number}
                </td>
                % endfor
            </tr>
            % endfor
        </table>
    </div>
</div>
% endfor

% if len(storages) == 0:
<div class="alert alert-info" role="alert">
    <strong>No storage added yet!</strong>
    Use <i>Add</i> button above to add a new storage container.
</div>
% endif

<div class="clearfix"></div>

<strong>Legend</strong>
<div class="legend">
    <div></div>
    Empty cell
</div>
<div class="legend">
    <div class="bg-info"></div>
    Cell with contents
</div>
<div class="legend">
    <div class="bg-danger"></div>
    Full cell
</div>

<%def name="make_add_storage_form()">
    <p>You can add a new storage container here.</p>
    <p>Storage containers a 2-dimensional. They have a width and a height. </p>

    <form class="form-horizontal" style="margin:40px 0 20px 0" id="storage-form">
        <div class="form-group">
            <label for="storage-name" class="col-sm-4 control-label">Name</label>
            <div class="col-sm-6">
                <input type="text" class="form-control" id="storage-name" name="name" placeholder="Name">
            </div>
        </div>
        <div class="form-group">
            <label for="storage-columns" class="col-sm-4 control-label">Columns</label>
            <div class="col-sm-4">
                <input type="number" class="form-control" id="storage-columns" name="columns" placeholder="Columns" min="1">
            </div>
        </div>
        <div class="form-group">
            <label for="storage-rows" class="col-sm-4 control-label">Rows</label>
            <div class="col-sm-4">
                <input type="number" class="form-control" id="storage-rows" name="rows" placeholder="Rows" min="1">
            </div>
        </div>
    </form>
</%def>

<%def name="make_add_storage_modal()">
    <div class="modal fade" id="add-storage-modal" tabindex="-1" role="dialog" aria-labelledby="Add new storage" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    <h4 class="modal-title">Add new storage</h4>
                </div>
                <div class="modal-body">
                    <div class="alert alert-danger hidden" role="alert" id="error-message"></div>
                    ${make_add_storage_form()}
                </div>
                <div class="modal-footer">
                    <span id="loader" class="hidden">
                        <span class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span>
                        Saving...
                    </span>
                    <button type="button" class="btn btn-default" id="btn-cancel" data-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" id="btn-save">Save</button>
                </div>
            </div>
        </div>
    </div>
</%def>

${make_add_storage_modal()}
