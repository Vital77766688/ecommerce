const addNewAddressBtn = document.querySelector('#add-new-address')
const changeAddressBtn = document.querySelectorAll('.change-address')
const modal = document.querySelector('.modal-address')
const modalClose = modal.querySelector('.close')


const clearModal = () => {
	const submit = modal.querySelector('button')
	submit.name = 'new_address'
	submit.innerHTML = 'Add'
	submit.value = ''
	modal.querySelector('#country').selectedIndex = 0
	modal.querySelector('#region').value = ''
	modal.querySelector('#city').value = ''
	modal.querySelector('#street').value = ''
	modal.querySelector('#building').value = ''
	modal.querySelector('#block').value = ''
	modal.querySelector('#is-private-house').checked = false
	modal.querySelector('#entrance').value = ''
	modal.querySelector('#appartment').value = ''
	modal.querySelector('#zip-code').value = ''	
}


if (addressNonFieldErrors || addressFieldErrors) {
	modal.classList.add('show')
}


addNewAddressBtn.addEventListener('click', e => {
	modal.classList.add('show')
})

changeAddressBtn.forEach(btn => {
	btn.addEventListener('click', e => {
		fetch(`${address_url}?id=${e.target.dataset.addressId}`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			}
		})
		.then(res => res.json())
		.then(data => {
			const submit = modal.querySelector('button')
			submit.name = 'change_address'
			submit.innerHTML = 'Change'
			submit.value = data.id
			const country = modal.querySelector('#country')
			for (let i = 0; i < country.options.length; i++) {
				if (country.options[i].value === data.country.code) {
					country.selectedIndex = i
					break
				}
			}
			modal.querySelector('#region').value = data.region
			modal.querySelector('#city').value = data.city
			modal.querySelector('#street').value = data.street
			modal.querySelector('#building').value = data.building_number
			modal.querySelector('#block').value = data.block
			modal.querySelector('#is-private-house').checked = data.is_private_house
			modal.querySelector('#entrance').value = data.entrance
			modal.querySelector('#appartment').value = data.appartment
			modal.querySelector('#zip-code').value = data.zip_code
			modal.classList.add('show')
		})
		.catch(error => console.error(error))
	})
})

modal.addEventListener('click', e => {
	if (e.target === modal) {
		clearModal()
		e.target.classList.remove('show')
	}
})
modalClose.addEventListener('click', e => {
	clearModal()
	modal.classList.remove('show')
})