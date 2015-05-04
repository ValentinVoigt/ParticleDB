<%inherit file="base.mak" />

## <%namespace file="functions/manufacturer.mak" import="make_manufacturer" />

<%block name="javascript">
    ##<script src="${request.static_url('particledb:static/js/remove_part.js')}"></script>
</%block>

<%block name="title">Storage &mdash;</%block>

<h1 class="page-header">Storage</h1>

<div class="row">
    % for storage in storages:
    <div class="col-md-4 col-sm-6">
        <div class="panel panel-default panel-primary">
            <div class="panel-heading">${storage.name}</div>
            <table class="table table-bordered">
                % for row in storage.iter_rows():
                <tr>
                    % for cell in row.iter_cells():
                    <td class="text-center">
                        % if len(cell.stocks) > 0:
                            <span class="glyphicon glyphicon-download-alt" aria-hidden="true"></span>
                        % endif
                        ${cell.number}
                    </td>
                    % endfor
                </tr>
                % endfor
            </table>
        </div>
    </div>
    % endfor
</div>