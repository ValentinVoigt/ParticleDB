<%def name="make_image(image, width=None, height=None)">
    % if image is None:
        <i>None</i>
    % else:
        <img src="${request.route_path('uploaded_file', uuid=image.uuid)}" alt="${image.filename}"
        % if width:
            width="${width}"
        % endif
        % if height:
            height="${height}"
        % endif
        />
    % endif
</%def>