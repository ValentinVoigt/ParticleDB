<%inherit file="base.mak" />

<%namespace file="functions/image.mak" import="make_image" />

<h1 class="page-header">${part.mpn}</h1>

% if part.manufacturer:
    <div class="panel panel-default pull-right">
        <div class="panel-heading">
            <h3 class="panel-title">${part.manufacturer.name}</h3>
        </div>
        <div class="panel-body">
            ${make_image(part.manufacturer.logo_image)}
        </div>
    </div>
% endif

<p>${part.description}</p>