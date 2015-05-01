<%namespace file="particledb:templates/functions/image.mak" import="make_image" />

<%def name="make_manufacturer(manufacturer)">
    <div class="panel panel-default text-center">
        <div class="panel-heading">
            <h3 class="panel-title">${manufacturer.name}</h3>
        </div>
        <div class="panel-body">
            % if manufacturer.logo_image:
                ${make_image(manufacturer.logo_image, width=150)}
            % endif
        </div>
        % if manufacturer.url:
            <div class="panel-footer">
                <a href="${manufacturer.url}" target="_blank">${manufacturer.url}</a>
            </div>
        % endif
    </div>
</%def>