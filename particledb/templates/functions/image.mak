<%def name="make_image(image, width=None, height=None)">
    % if image is None:
        <i>None</i>
    % else:
        <img src="${request.static_url('particledb:static/img/')}${image.path}" alt="${image.alt}"
        % if width:
            width="${width}"
        % endif
        % if height:
            height="${height}"
        % endif
        />
    % endif
</%def>