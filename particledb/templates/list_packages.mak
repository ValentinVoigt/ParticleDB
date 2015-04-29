<%inherit file="base.mak" />

<h1 class="page-header">List of registered packages</h1>

<div class="table-responsive">
    <table class="table table-striped">
        <thead>
            <tr>
                <th>#</th>
                <th>Name</th>
                <th>Pins</th>
                <th>Picture</th>
            </tr>
        </thead>
        <tbody>
            % for package in packages:
            <tr>
                <td>${package.id}</td>
                <td>${package.name}</td>
                <td>${package.pins}</td>
                <td>${package.picture}</td>
            </tr>
            % endfor
        </tbody>
    </table>
</div>