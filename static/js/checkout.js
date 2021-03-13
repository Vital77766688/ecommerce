const isBillingSame = document.querySelector('#is-billing-same')
const billingAddress = document.querySelector('.billing-address')
const modal = document.querySelector('.modal-address')
const modalClose = modal.querySelector('.close')
const addDeliveryAddressBtn = document.querySelector('#add-delivery-address')
const addBillingAddressBtn = document.querySelector('#add-billing-address')
const addressForm = document.querySelector('#address-form')

if (addressNonFieldErrors || addressFieldErrors) {
	modal.classList.add('show')
}

const addHiddenClass = (elem, target) => {
	elem.checked ? target.classList.add('hidden') : target.classList.remove('hidden')
}

addHiddenClass(isBillingSame, billingAddress)

isBillingSame.addEventListener('change', e => {
	addHiddenClass(e.target, billingAddress)
})

addDeliveryAddressBtn.addEventListener('click', e => {
	modal.classList.add('show')
})
addBillingAddressBtn.addEventListener('click', e => {
	modal.classList.add('show')
})
modal.addEventListener('click', e => {
	e.target.classList.remove('show')
})
modalClose.addEventListener('click', e => {
	modal.classList.remove('show')
})