<%inherit file="base.mak" />

<%namespace file="functions/pagination.mak" import="paginate" />
<%namespace file="functions/image.mak" import="make_image" />

<%block name="title">Manufacturer list &mdash;</%block>

<%block name="javascript">
    <script src="${request.static_url('particledb:static/js/edit_manufacturers.js')}"></script>
</%block>

<h1 class="page-header">List of registered manufacturers</h1>

<div class="table-responsive">
    <table class="table table-striped">
        <thead>
            <tr>
                <th>#</th>
                <th>Manufacturer name</th>
                <th>URL</th>
                <th>Logo</th>
            </tr>
        </thead>
        <tbody>
            % for manufacturer in pagination.current_dataset:
            <tr>
                <td class="vert-align">${manufacturer.id}</td>
                <td class="vert-align">
                    <a href="#" class="editable-name" data-type="text" data-name="name" data-pk="${manufacturer.id}" data-url="${request.route_path('manufacturers_edit')}" data-title="Enter name">
                        ${manufacturer.name}
                    </a>
                </td>
                <td class="vert-align">
                    <a href="#" class="editable-url" data-type="text" data-name="url" data-pk="${manufacturer.id}" data-url="${request.route_path('manufacturers_edit')}" data-title="Enter URL">
                        ${manufacturer.url if manufacturer.url else ''}
                    </a>
                </td>
                <td class="vert-align">${make_image(manufacturer.logo_image, height=35)}</td>
            </tr>
            % endfor
        </tbody>
    </table>
</div>

${paginate(pagination)}