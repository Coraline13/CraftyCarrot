<template>
  <div>
    <div class="hero">
      <div class="hero__overlay hero__overlay--gradient"></div>
      <div class="hero__mask"></div>
      <div class="hero__inner">
        <div class="container">
          <div class="hero__content">
            <div class="hero__content__inner" id='navConverter'>
              <h1 class="hero__title">Agricultural and handcrafted goods <br>now closer to you</h1>
              <p class="hero__text">CraftyCarrot is a platform that will make it easier for people who have been
                harvesting their own vegetables to sell them.</p>
              <router-link class="button button__accent" to="/register">Try it now</router-link>
              <router-link class="button hero__button" to="/pricing">Learn more</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="hero__sub">
		<span id="scrollToNext" class="scroll">
			<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
           class='hero__sub__down' fill="currentColor" width="512px" height="512px" viewBox="0 0 512 512"
           style="enable-background:new 0 0 512 512;" xml:space="preserve"><path d="M256,298.3L256,298.3L256,298.3l174.2-167.2c4.3-4.2,11.4-4.1,15.8,0.2l30.6,29.9c4.4,4.3,4.5,11.3,0.2,15.5L264.1,380.9c-2.2,2.2-5.2,3.2-8.1,3c-3,0.1-5.9-0.9-8.1-3L35.2,176.7c-4.3-4.2-4.2-11.2,0.2-15.5L66,131.3c4.4-4.3,11.5-4.4,15.8-0.2L256,298.3z"/></svg>
		</span>
    </div>

    <div class="steps landing__section">
      <div class="container">
        <h2>Why use CraftyCarrot?</h2>
        <p>Here's what we can think of, but surely creative people will surprise us.</p>
      </div>
      <div class="container">
        <div class="steps__inner">
          <div class="step">
            <div class="step__media">
              <img src="../assets/sell.svg" class="step__image">
            </div>
            <h4>Efficient selling</h4>
            <p class="step__text">Make it easier for people who have been harvesting their own vegetables to sell
              them!</p>
          </div>
          <div class="step">
            <div class="step__media">
              <img src="../assets/buy.svg" class="step__image">
            </div>
            <h4>Efficient buying</h4>
            <p class="step__text">You have everything well sorted and easy to find!</p>
          </div>
          <div class="step">
            <div class="step__media">
              <img src="../assets/nature.svg" class="step__image">
            </div>
            <h4>Promote harvesting and handcrafting</h4>
            <p class="step__text">In a year of technology and chemicals we have to protect and promote natural and "old
              school" traditions!</p>
          </div>
        </div>
      </div>
    </div>

    <div class="expanded landing__section">
      <div class="container">
        <div class="expanded__inner">
          <div class="expanded__media">
            <img src="../assets/mobile.svg" class="expanded__image">
          </div>
          <div class="expanded__content">
            <h2 class="expanded__title">Mobile friendly</h2>
            <p class="expanded__text">Feel free to navigate on our platform from any type of device: desktop, mobile,
              tablet etc. Our design makes it easy to buy or sell no matter what device you are using.</p>
          </div>
        </div>
      </div>
    </div>
    <div class="expanded landing__section">
      <div class="container">
        <div class="expanded__inner">
          <div class="expanded__media">
            <img src="../assets/ready.svg" class="expanded__image">
          </div>
          <div class="expanded__content">
            <h2 class="expanded__title">Ready to go!</h2>
            <p class="expanded__text">CraftyCarrot offers you the possibility to sell or buy vegetables and/or
              handcrafted goods. The creation of a profile takes only a few seconds and can be used instantly!</p>
          </div>
        </div>
      </div>
    </div>
    <div class="expanded landing__section">
      <div class="container">
        <div class="expanded__inner">
          <div class="expanded__media">
            <img src="../assets/healthier.svg" class="expanded__image">
          </div>
          <div class="expanded__content">
            <h2 class="expanded__title">Change your lifestyle</h2>
            <p class="expanded__text">Go bio and improve your lifestyle by eating healthier and using handcrafted goods
              instead of the ones created in factories. It's never too late to change the way you and your loved ones
              live. <i><b>"Be the change you want to see in the world!"</b></i></p>
          </div>
        </div>
      </div>
    </div>

    <div class="cta cta--reverse">
      <div class="container">
        <div class="cta__inner">
          <h2 class="cta__title">Get started now</h2>
          <p class="cta__sub cta__sub--center">Register now and configure your chatbot instantly.</p>
          <router-link class="button button__accent" to="/register">Start free 14-day trial</router-link>
        </div>
      </div>
    </div>

    <div class="footer footer--dark">
      <div class="container">
        <div class="footer__inner">
          <div class="footer__data">© CraftyCarrot 2019
            <div class="footer__data__item">
              <div class="footer__row"></div>
            </div>
            <div class="footer__data__item">
              <div class="footer__row"><a href="https://github.com/Coraline13/CraftyCarrot" target="_blank"
                                          class="footer__link">GitHub</a></div>
            </div>
            <div class="footer__data__item">
              <div class="footer__row">Contact</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

</script>

<style scoped>

</style>
