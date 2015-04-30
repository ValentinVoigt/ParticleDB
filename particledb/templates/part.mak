<%inherit file="base.mak" />

<%namespace file="functions/image.mak" import="make_image" />

<%block name="javascript">
    <script src="${request.static_url('particledb:static/js/remove_part.js')}"></script>
</%block>

<h1 class="page-header">${part.mpn}</h1>

% if part.manufacturer:
    <div class="panel panel-default pull-right">
        <div class="panel-heading">
            <h3 class="panel-title">${part.manufacturer.name}</h3>
        </div>
        <div class="panel-body" style="padding:15px 40px">
            % if part.manufacturer.logo_image:
                ${make_image(part.manufacturer.logo_image, width=150)}
            % endif
            % if part.manufacturer.url:
                <p class="text-center" style="margin-top:20px">
                    <a href="${part.manufacturer.url}" target="_blank">${part.manufacturer.url}</a>
                </p>
            % endif
        </div>
    </div>
% endif

<p>${part.description}</p>

<form action="${request.route_path('remove_part', part_mpn=part.mpn)}" method="POST" id="remove-part-form"></form>

<p class="clearfix">
    <hr>
    <button type="button" class="btn btn-danger pull-right" id="remove-part">Remove from database</button>
</p>
