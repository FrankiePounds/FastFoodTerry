<style>
  main {
    background-image: url('/background.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    min-height: 100vh;
    padding-top: 4rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    color: white;
    text-shadow: 1px 1px 2px black;
  }

  .reel-grid {
    display: grid;
    grid-template-columns: repeat(5, 130px);
    grid-template-rows: repeat(3, 130px);
    gap: 4px;
    background: rgba(0, 0, 0, 0.3);
    padding: 10px;
    border-radius: 12px;
    box-shadow: 0 0 15px #000;
  }

  .symbol {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  button {
    margin-top: 1rem;
    padding: 0.75rem 1.5rem;
    background: #ffcb00;
    border: none;
    border-radius: 10px;
    font-size: 1.1rem;
    cursor: pointer;
    box-shadow: inset 0 -3px 0 rgba(0,0,0,0.2);
    transition: transform 0.1s;
  }

  button:active {
    transform: translateY(2px);
    box-shadow: inset 0 1px 0 rgba(0,0,0,0.2);
  }
</style>

<script>
  import { onMount } from 'svelte';
  import SpriteAnimator from '$lib/components/SpriteAnimator.svelte';

  let spinResult = null;
  let shouldAnimate = {
    A: false,
    K: false,
    Q: false,
    J: false,
    "10": false,
    TERRY: false,
    BURGER: false,
    SHAKE: false,
    FRY: false,
    PIZZA: false
  };

  async function doSpin() {
    const res = await fetch('/spin');
    spinResult = await res.json();

    // Reset animation triggers
    for (let key in shouldAnimate) {
      shouldAnimate[key] = false;
    }

    // Activate animation flags based on symbols in the grid
    const symbolsInGrid = new Set(spinResult.grid.flat());
    for (let symbol of symbolsInGrid) {
      if (shouldAnimate[symbol] !== undefined) {
        shouldAnimate[symbol] = true;
      }
    }

    // Turn off animations after 1 second
    setTimeout(() => {
      for (let key in shouldAnimate) {
        shouldAnimate[key] = false;
      }
    }, 1000);
  }
</script>

<main>
  <h1>🎰 Fast Food Terry</h1>
  <button on:click={doSpin}>Spin!</button>

  {#if spinResult}
    <h3>Spin Result:</h3>
    <pre>{JSON.stringify(spinResult, null, 2)}</pre>
  {/if}

  {#if spinResult}
    <div class="reel-grid">
      {#each spinResult.grid as col}
        {#each col as symbol}
          <div class="symbol">
            {#if shouldAnimate[symbol]}
              <SpriteAnimator
                spritePath={`/symbols/spritesheets/${symbol}.png`}
                frameWidth={130}
                frameHeight={130}
                frameCount={24}
                fps={24}
                playing={true}
              />
            {:else}
              <img
                src={`/symbols/static_symbols/${symbol.toLowerCase()}/${symbol.toLowerCase()}.png`}
                alt={symbol}
                width="130"
                height="130"
              />
            {/if}
          </div>
        {/each}
      {/each}
    </div>
  {/if}
  </main>
