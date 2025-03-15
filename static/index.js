const cards =gsap.utils.toArray(".card");

cards.forEach(card => {
    const anim =gsap.fromTo(
        card,
        {
            autoAlpha:0,
            y:100,
            x:-100,
            rotate:-10
        },
        {
            duration:0.6,
            autoAlpha:1,
            y:0,
            x:0,
            rotate:0
        }
    );
    ScrollTrigger.create({
        trigger:card,
        animation:anim,
    });
});