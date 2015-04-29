<%def name="paginate(pagination)">
    <nav class="text-center">
        <ul class="pagination">
            <li
            % if not pagination.has_prev:
            class="disabled"
            % endif
            >
              <a href="${pagination.route_path(pagination.page - 1)}" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
              </a>
            </li>
            % for page in pagination.iterator:
                <li
                % if page == pagination.page:
                class="active"
                % endif
                ><a href="${pagination.route_path(page)}">${page}</a></li>
            % endfor
            <li
            % if not pagination.has_next:
            class="disabled"
            % endif
            >
              <a href="${pagination.route_path(pagination.page + 1)}" aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
              </a>
            </li>
        </ul>
    </nav>
</%def>