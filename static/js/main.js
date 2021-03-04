const cart = document.querySelector('.cart-qty')
const productCards = document.querySelectorAll('.product-card')
const productDetails = document.querySelector('.product-details')
const cartItems = document.querySelectorAll('.cart-item')
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
		toastContainer.append(createToast('Product added to cart'))
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


const resetSubtotalPrice = () => {
	const priceValue = subtotalPrice.querySelector('.price-value')
	let stPrice = 0
	document.querySelectorAll('.total-price').forEach(tp => {
		stPrice += parseFloat(tp.querySelector('.price-value').innerText)
	})
	priceValue.innerHTML = stPrice.toFixed(2)
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


if (productDetails) {
	
	const productQty = productDetails.querySelector('.qty')
	
	updateTotalPrice(productDetails, productQty.value)
	
	const addToCartBtn = productDetails.querySelector('.add-to-cart')
	addToCartBtn.addEventListener('click', e => {
		addUpdateCart(e.target.value, productQty.value)
	})
	
	productQty.addEventListener('keyup', e => {
		updateTotalPrice(productDetails, e.target.value)
	})
	productQty.addEventListener('change', e => {
		updateTotalPrice(productDetails, e.target.value)
	})
}


cartItems.forEach(item => {

	const productQty = item.querySelector('.qty')

	updateTotalPrice(item, productQty.value)
	
	const deleteFromCartBtn = item.querySelector('.delete-from-cart')
	deleteFromCartBtn.addEventListener('click', e => {
		deleteFromCart(e.target.value)
		.then(() => {
			let cartQty = parseInt(cart.innerText) - parseInt(productQty.value)
			cart.innerHTML = cartQty
			if (cartQty === 0) {
				document.querySelector('.cart').innerHTML = '<p class="no-products-found">No products found</p>'
				document.querySelector('.summary').remove()
			} else {
				item.remove()
				resetSubtotalPrice()
			}
		})
	})

	const updateCartBtn = item.querySelector('.update-cart')
	updateCartBtn.addEventListener('click', e => {
		addUpdateCart(e.target.value, productQty.value)
		.then(() => {
			e.target.disabled = true
			updateTotalPrice(item, productQty.value)
			resetSubtotalPrice()
		})
	})

	productQty.addEventListener('keyup', e => {
		if (updateCartBtn.disabled) {
			updateCartBtn.disabled = false
		}
	})
	productQty.addEventListener('change', e => {
		if (updateCartBtn.disabled) {
			updateCartBtn.disabled = false
		}	
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