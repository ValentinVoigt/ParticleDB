<%inherit file="base.mak" />

<%namespace file="functions/pagination.mak" import="paginate" />
<%namespace file="functions/image.mak" import="make_image" />

<h1 class="page-header">List of registered manufacturers</h1>

<div class="table-responsive">
    <table class="table table-striped">
        <thead>
            <tr>
                <th>#</th>
                <th>Manufacturer name</th>
                <th>Logo</th>
            </tr>
        </thead>
        <tbody>
            % for manufacturer in pagination.current_dataset:
            <tr>
                <td class="vert-align">${manufacturer.id}</td>
                <td class="vert-align">${manufacturer.name}</td>
                <td class="vert-align">${make_image(manufacturer.logo_image, height=35)}</td>
            </tr>
            % endfor
        </tbody>
    </table>
</div>

${paginate(pagination)}