exclude_fields = {
    MC: ['#connection_set-group'],
    AC: ['#list-group']
}


window.onload = function() {
    var element = document.querySelector('#id_proj_type');
    element.addEventListener('change', function() {
        Object.entries(exclude_fields).forEach(element => {
            var display = this.value == element[0] ? 'none' : 'block';
            element[1].forEach(query => { document.querySelector(query).style.display = display; });
        });
    });
    element.dispatchEvent(new Event('change'));
}