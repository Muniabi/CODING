document.querySelectorAll('.slider').forEach((n, i) => {
    window[`slider${i + 1}`] = new Swiper(n, {
        freeMode: true,
        centerSlides: true,
        direction: 'vertical',
        mousewheel: true,
        slidesPerView: 1.75,
    })
})