const orderArrows = document.querySelectorAll('.order-arrow')

orderArrows.forEach(arrow => {
	arrow.addEventListener('click', e => {
		const details = document
							.querySelector(`#${e.target.dataset.orderId}`)
							.querySelector('.order-details')
		details.classList.toggle('show')
		e.target.classList.toggle('show')
	})
})