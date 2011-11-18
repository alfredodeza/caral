<html><head><title>Links for ${project_name}</title></head><body><h1>Links for ${project_name}</h1>

% for p in packages:
	<a rel="homepage" href="/${project_name}/${p}">${p}</a><br/>
% endfor

</body></html>

