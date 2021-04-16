const cart = document.querySelector('.cart-qty')
const productCards = document.querySelectorAll('.product-card')
const subtotalPrice = document.querySelector('.subtotal-price')
const toastContainer = document.querySelector('.toast-container')
const toasts = document.querySelectorAll('.toast')


const addUpdateCart = async (id, qty) => {
	const response = await fetch(updateCartURL, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify({id, qty})
	})
	const data = await response.json()
	if (data.success) {
		cart.innerHTML = data.data.cart_qty
		toastContainer.append(createToast(data.message))
		return
	}
} 


const deleteFromCart = async id => {
	const response = await fetch(updateCartURL, {
		method: 'DELETE',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify({id})
	})
	if (response.status === 204) {
		return
	}
}


const updateTotalPrice = (parent, qty) => {
	const totalPrice = parent.querySelector('.total-price').querySelector('.price-value')
	const price = parent.querySelector('.price').querySelector('.price-value')
	totalPrice.innerHTML = (parseFloat(price.innerHTML) * parseFloat(qty)).toFixed(2).toString()
}


const createToast = message => {
	const toast = document.createElement('p')
	toast.className = 'toast'
	toast.innerHTML = message
	const close = document.createElement('button')
	close.type = 'button'
	close.className = 'btn-close'
	close.innerHTML = '&times'
	close.addEventListener('click', () => {
		toast.remove()
	})
	toast.append(close)
	setTimeout(() => {
		toast.remove()
	}, 3000)
	return toast
}

productCards.forEach(card => {
	const addToCartBtn = card.querySelector('.add-to-cart')
	addToCartBtn.addEventListener('click', e => {
		addUpdateCart(e.target.value, '1')
	})
})

toasts.forEach(toast => {
	const close = toast.querySelector('.btn-close')
	close.addEventListener('click', () => {
		toast.remove()
	})
	setTimeout(() => {
		toast.remove()
	}, 3000)
})