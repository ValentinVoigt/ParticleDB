<%def name="make_navigation(navigation)">
    <ul class="nav nav-sidebar">
        % for item in navigation:
            % if item is None:
                </ul>
                <ul class="nav nav-sidebar">
            % elif type(item) is tuple:
                <% nav_active, title, href = item[0:3] %>
                <% options = [] if len(item) == 3 else item[3] %>
                <li
                % if nav_active == view.nav_active:
                    class="active"
                % elif 'indent' in options:
                    class="active-indent"
                % endif
                ><a href="${href}">
                % if 'indent' in options:
                <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
                % endif
                ${title}
                % if nav_active == view.nav_active:
                    <span class="sr-only">(current)</span>
                % endif
                </a></li>
            % elif type(item) is str:
                <li><b>${item}</b></li>
            % else:
                <% raise TypeError("Invalid navigation entry: %r" % item) %>
            % endif
        % endfor
    </ul>
</%def>