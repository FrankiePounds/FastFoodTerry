<script>
  export let spritePath = "";
  export let frameWidth = 130;
  export let frameHeight = 130;
  export let frameCount = 24;
  export let fps = 24;
  export let playing = false;

  let currentFrame = 0;
  let interval;

  $: spriteStyle = {
    width: `${frameWidth}px`,
    height: `${frameHeight}px`,
    backgroundImage: `url(${spritePath})`,
    backgroundRepeat: 'no-repeat',
    backgroundPosition: `-${currentFrame * frameWidth}px 0px`,
    imageRendering: 'pixelated'
  };

  function startAnimation() {
    stopAnimation();
    interval = setInterval(() => {
      currentFrame = (currentFrame + 1) % frameCount;
    }, 1000 / fps);
  }

  function stopAnimation() {
    clearInterval(interval);
    currentFrame = 0;
  }

  $: if (playing) startAnimation();
  $: if (!playing) stopAnimation();
</script>

<div class="sprite" style={spriteStyle}></div>

<style>
  .sprite {
    overflow: hidden;
  }
</style>
