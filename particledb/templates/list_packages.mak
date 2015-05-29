<%inherit file="base.mak" />

<%namespace file="functions/pagination.mak" import="paginate" />

<%block name="title">Package list &mdash;</%block>

<h1 class="page-header">List of registered packages</h1>

<div class="table-responsive">
    <table class="table table-striped">
        <thead>
            <tr>
                <th>#</th>
                <th>Name</th>
                <th>Pins</th>
                <th>Picture</th>
            </tr>
        </thead>
        <tbody>
            % for package in pagination.current_dataset:
            <tr>
                <td>${package.id}</td>
                <td>${package.name}</td>
                <td>${package.pins}</td>
                <td>${package.picture}</td>
            </tr>
            % endfor
			% if pagination.is_empty:
                <tr>
                    <td colspan="4" class="emptyrow">none</td>
                </tr>
            % endif
        </tbody>
    </table>
</div>

${paginate(pagination)}