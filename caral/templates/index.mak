<html><head><title>Simple Index</title></head><body> 

% for p in packages:
	<a href=${p.name}>${p.name}</a><br/>
% endfor

</body></html>

