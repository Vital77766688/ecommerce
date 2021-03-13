const cartItems = document.querySelectorAll('.cart-item')

const resetSubtotalPrice = () => {
	const priceValue = subtotalPrice.querySelector('.price-value')
	let stPrice = 0
	document.querySelectorAll('.total-price').forEach(tp => {
		stPrice += parseFloat(tp.querySelector('.price-value').innerText)
	})
	priceValue.innerHTML = stPrice.toFixed(2)
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