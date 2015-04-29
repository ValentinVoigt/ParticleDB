<%def name="make_image(image)">
    % if image is None:
        <i>None</i>
    % else:
        <img src="${request.static_url('particledb:static/img/')}${image.path}" alt="${image.alt}" />
    % endif
</%def>