<%inherit file="base.mak" />

<%namespace file="functions/pagination.mak" import="paginate" />

<h1 class="page-header">List of registered parts</h1>

<div class="table-responsive">
    <table class="table table-striped">
        <thead>
            <tr>
                <th>#</th>
                <th>MPN</th>
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
                % if part.manufacturer:
                    ${part.manufacturer.name}
                % else:
                    <i>None</i>
                % endif
                </td>
                <td>${part.description}</td>
            </tr>
            % endfor
        </tbody>
    </table>
</div>

${paginate(pagination)}