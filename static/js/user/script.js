let select1 = document.getElementById('select1'), select2 = document.getElementById('select2');
select2.style.display = 'none'
select1.addEventListener('change', () => {
    fetch('get_university', {
        method: 'POST', body: JSON.stringify({
            'country_id': select1.value
        }), headers: {
            'Content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(response => {
            select2.style.display = 'flex'
            select2.innerHTML = ''
            response['all_university'].forEach(item => {
                select2.innerHTML += `<option value="${item.id}">${item.name}</option>`
            })
        })
})