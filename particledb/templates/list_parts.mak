<%inherit file="base.mak" />

<%namespace file="functions/pagination.mak" import="paginate" />

<%block name="title">Parts list &mdash;</%block>

<h1 class="page-header">
    List of registered parts
    <a href="${request.route_path('add_part')}">
        <button type="button" class="btn btn-default pull-right">
            <span class="glyphicon glyphicon-plus" aria-hidden="true"></span> Add part
        </button>
    </a>
</h1>

<div class="table-responsive">
    <table class="table table-striped">
        <thead>
            <tr>
                <th>#</th>
                <th>MPN</th>
                <th>Avail.</th>
                <th>Manufacturer</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            % for part in pagination.current_dataset:
            <tr>
                <td>${part.id}</td>
                <td>
                    <a href="${request.route_path("part", part_mpn=part.mpn)}">${part.mpn}</a>
                </td>
                <td>
                    ${sum([i.quantity for i in part.stocks])}
                </td>
                <td>
                % if part.manufacturer:
                    ${part.manufacturer.name}
                % else:
                    <i>None</i>
                % endif
                </td>
                <td>${part.description}</td>
            </tr>
            % endfor
			% if pagination.is_empty:
                <tr>
                    <td colspan="5" class="emptyrow">none</td>
                </tr>
            % endif
        </tbody>
    </table>
</div>

${paginate(pagination)}