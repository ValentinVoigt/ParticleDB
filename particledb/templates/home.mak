<%inherit file="base.mak" />

<h1 class="page-header">Home</h1>

<form action="${request.route_path('upload')}" method="post" accept-charset="utf-8" enctype="multipart/form-data">
    <label for="file">File</label>
    <input id="file" name="file" type="file" value="" />

    <input type="submit" value="submit" />
</form>
