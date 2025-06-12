<script>
  import SpriteAnimator from '$lib/components/SpriteAnimator.svelte';

  let spinResult = null;
  let shouldAnimate = {
    a: false,
    k: false,
    q: false,
    j: false,
    "10": false,
    terry: false,
    burger: false,
    shake: false,
    fry: false,
    pizza: false
  };

  // Symbol-to-image map: keys MUST match backend's output, filenames all lowercase!
  const symbolMap = {
    A: { sprite: "a_spritesheet.png", static: "ace/ace.png" },
    K: { sprite: "k_spritesheet.png", static: "king/king.png" },
    Q: { sprite: "q_spritesheet.png", static: "queen/queen.png" },
    J: { sprite: "j_spritesheet.png", static: "jack/jack.png" },
    "10": { sprite: "10_spritesheet.png", static: "10/ten.png" },
    TERRY: { sprite: "terry_wild_spritesheet.png", static: "terry_wild/terry_wild.png" },
    BURGER: { sprite: "scatter_burger_1_3_5_spritesheet.png", static: "scatter/scatter_burger.png" },
    SHAKE: { sprite: "milk_shake_spritesheet.png", static: "milkshake/milkshake.png" },
    FRY: { sprite: "fries_spritesheet.png", static: "fries/fries.png" },
    PIZZA: { sprite: "pizza_spritesheet.png", static: "pizza_slice/pizza_slice.png" }
  };

  async function doSpin() {
    const res = await fetch('/spin');
    spinResult = await res.json();

    // Reset animation flags
    for (let key in shouldAnimate) shouldAnimate[key] = false;

    // Activate animation for symbols present in grid
    const symbolsInGrid = new Set(spinResult.grid.flat());
    for (let symbol of symbolsInGrid) {
      if (symbolMap[symbol]) {
        let animKey = symbol.toLowerCase();
        if (shouldAnimate[animKey] !== undefined) shouldAnimate[animKey] = true;
      }
    }

    setTimeout(() => {
      for (let key in shouldAnimate) shouldAnimate[key] = false;
    }, 1000);
  }
</script>

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
    margin-top: 2rem;
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

<main>
  <h1>🎰 Fast Food Terry</h1>
  <button on:click={doSpin}>Spin!</button>

  <!-- Debug panel: See exactly what symbols are in your grid -->
  {#if spinResult}
    <pre style="background:rgba(0,0,0,0.8);color:#0f0;padding:10px;font-size:0.8rem;text-align:left;max-width:550px;overflow:auto;">
{JSON.stringify(spinResult, null, 2)}
    </pre>
  {/if}

  {#if spinResult}
    <!-- Transposed grid rendering: 3 rows, 5 columns -->
    <div class="reel-grid">
      {#each [0,1,2] as row}
        {#each [0,1,2,3,4] as col}
          {#if symbolMap[spinResult.grid[col][row]]}
            <div class="symbol">
              {#if shouldAnimate[spinResult.grid[col][row].toLowerCase()]}
                <SpriteAnimator
                  spritePath={`/symbols/spritesheets/${symbolMap[spinResult.grid[col][row]].sprite}`}
                  frameWidth={130}
                  frameHeight={130}
                  frameCount={24}
                  fps={24}
                  playing={true}
                />
              {:else}
                <img
                  src={`/symbols/static_symbols/${symbolMap[spinResult.grid[col][row]].static}`}
                  alt={spinResult.grid[col][row]}
                  width="130"
                  height="130"
                />
              {/if}
            </div>
          {:else}
            <!-- Fallback: show the symbol text if not mapped -->
            <div class="symbol" style="background:#222;color:#fff;width:130px;height:130px;align-items:center;justify-content:center;display:flex;">
              {spinResult.grid[col][row]}
            </div>
          {/if}
        {/each}
      {/each}
    </div>
  {/if}
</main>
