const productDetails = document.querySelector('.product-details')
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