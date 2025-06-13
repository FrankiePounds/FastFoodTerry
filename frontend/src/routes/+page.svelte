<script>
  import { fly } from 'svelte/transition';
  import { onMount } from 'svelte';
  import SpriteAnimator from '$lib/components/SpriteAnimator.svelte';

  const MUSIC_FILE = "/audio/midi_loop/midi_loop.mp3";
  const SPIN_SFX_FILE = "/audio/sound_effects/spin_sfx/spin_button/spin_button.mp3";
  const REEL_END_FILES = [
    "/audio/sound_effects/spin_sfx/end_reel_1/end_reel_1.mp3",
    "/audio/sound_effects/spin_sfx/end_reel_2/end_reel_2.mp3",
    "/audio/sound_effects/spin_sfx/end_reel_3/end_reel_3.mp3",
    "/audio/sound_effects/spin_sfx/end_reel_4/end_reel_4.mp3",
    "/audio/sound_effects/spin_sfx/end_reel_5/end_reel_5.mp3"
  ];
  const LOOP_BPM = 65;
  const BEAT_DIVISION = 1;

  const symbolMap = {
    A: { sprite: "a_spritesheet.png", static: "ace/ace.png", frameCount: 24 },
    K: { sprite: "k_spritesheet.png", static: "king/king.png", frameCount: 24 },
    Q: { sprite: "q_spritesheet.png", static: "queen/queen.png", frameCount: 24 },
    J: { sprite: "j_spritesheet.png", static: "jack/jack.png", frameCount: 24 },
    "10": { sprite: "10_spritesheet.png", static: "10/ten.png", frameCount: 24 },
    TERRY: { sprite: "terry_wild_spritesheet.png", static: "terry_wild/terry_wild.png", frameCount: 24 },
    BURGER: { sprite: "scatter_burger_1_3_5_spritesheet.png", static: "scatter/scatter_burger.png", frameCount: 24 },
    SHAKE: { sprite: "milk_shake_spritesheet.png", static: "milkshake/milkshake.png", frameCount: 24 },
    FRY: { sprite: "fries_spritesheet.png", static: "fries/fries.png", frameCount: 24 },
    PIZZA: { sprite: "pizza_spritesheet.png", static: "pizza_slice/pizza_slice.png", frameCount: 24 }
  };

  let spinResult = null;
  let droppingGrid = Array(5).fill().map(() => Array(3).fill(null));
  let revealState = [false, false, false, false, false];
  let spinning = false;
  let winningPositions = [];

  let music;
  let musicReady = false;
  let userInteracted = false;
  const beatLength = 60 / LOOP_BPM;

  onMount(() => {
    music = new Audio(MUSIC_FILE);
    music.loop = true;
    music.volume = 0.7;
    music.addEventListener('canplaythrough', () => {
      musicReady = true;
    });
    music.load();
  });

  function ensureMusicPlaying() {
    if (musicReady && userInteracted && music.paused) {
      music.currentTime = 0;
      music.play();
    }
  }

  function playSpinButtonSFX() {
    const sfx = new Audio(SPIN_SFX_FILE);
    sfx.volume = 0.7;
    sfx.play();
  }

  function playReelEndSFX(reelIndex) {
    if (reelIndex >= 0 && reelIndex < REEL_END_FILES.length) {
      const sfx = new Audio(REEL_END_FILES[reelIndex]);
      sfx.volume = 0.7;
      sfx.play();
    }
  }

  function nextBeatDelay() {
    if (!music) return 0;
    let t = music.currentTime % (beatLength * 16);
    let next = Math.ceil(t / (beatLength * BEAT_DIVISION)) * (beatLength * BEAT_DIVISION);
    let wait = next - t;
    if (wait < 0.01) wait += beatLength * BEAT_DIVISION;
    return wait;
  }

  // Find all winning positions: return array of [col, row] for all symbols in any winning line (left-to-right only, as in PAYLINES)
  function getWinningPositions(grid) {
    const PAYLINES = [
      [0, 0, 0, 0, 0],
      [1, 1, 1, 1, 1],
      [2, 2, 2, 2, 2]
    ];
    const WIN_LENGTH = 3;
    let wins = [];

    for (const payline of PAYLINES) {
      let symbol = grid[0][payline[0]];
      let match = true;
      let matchedCols = [0];

      // Allow wilds to be part of any win
      for (let col = 1; col < 5; col++) {
        const val = grid[col][payline[col]];
        if (val === symbol || val === "TERRY" || symbol === "TERRY") {
          matchedCols.push(col);
          if (symbol === "TERRY" && val !== "TERRY") symbol = val;
        } else {
          break;
        }
      }
      if (matchedCols.length >= WIN_LENGTH && symbol !== "BURGER") {
        for (let i = 0; i < matchedCols.length; i++) {
          wins.push([matchedCols[i], payline[matchedCols[i]]]);
        }
      }
    }
    return wins;
  }

  async function doSpin() {
    userInteracted = true;
    ensureMusicPlaying();

    if (spinning || !musicReady) return;
    spinning = true;
    spinResult = null;
    winningPositions = [];

    playSpinButtonSFX();

    let wait = nextBeatDelay();
    await new Promise(res => setTimeout(res, wait * 1000));

    const res = await fetch('/spin');
    const result = await res.json();

    droppingGrid = Array(5).fill().map(() => Array(3).fill(null));
    revealState = [false, false, false, false, false];

    for (let reel = 0; reel < 5; reel++) {
      if (reel > 0) await new Promise(res => setTimeout(res, (beatLength * 1000 * BEAT_DIVISION) / 2));

      for (let row = 0; row < 3; row++) {
        droppingGrid[reel][row] = result.grid[reel][row];
      }
      revealState[reel] = true;

      playReelEndSFX(reel);
    }

    spinResult = result;
    winningPositions = getWinningPositions(result.grid);

    spinning = false;
  }

  // Utility: is a symbol at col,row part of a current win?
  function isWinningSymbol(col, row) {
    return winningPositions.some(([c, r]) => c === col && r === row);
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
    width: 658px;
    height: 398px;
    display: grid;
    grid-template-columns: repeat(5, 130px);
    grid-template-rows: repeat(3, 130px);
    gap: 4px;
    background: rgba(0, 0, 0, 0.3);
    padding: 10px;
    border-radius: 12px;
    box-shadow: 0 0 15px #000;
    margin-top: 2rem;
    place-items: center;
    justify-content: center;
    align-content: center;
  }
  .symbol {
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(15,15,15,0.1);
    border-radius: 8px;
    width: 130px;
    height: 130px;
    overflow: hidden;
  }
  .symbol img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
</style>

<main>
  <h1>🎰 Fast Food Terry</h1>
  <button on:click={doSpin} disabled={spinning || !musicReady}>
    {spinning ? "Spinning..." : musicReady ? "Spin!" : "Loading Music..."}
  </button>

  <div class="reel-grid">
    {#each [0,1,2] as row}
      {#each [0,1,2,3,4] as col}
        {#if droppingGrid[col][row]}
          <div class="symbol">
            {#if isWinningSymbol(col, row)}
              <SpriteAnimator
                spritePath={`/symbols/spritesheets/${symbolMap[droppingGrid[col][row]].sprite}`}
                frameWidth={130}
                frameHeight={130}
                frameCount={symbolMap[droppingGrid[col][row]].frameCount}
                fps={24}
                playing={true}
                loop={true}
              />
            {:else}
              <img
                src={`/symbols/static_symbols/${symbolMap[droppingGrid[col][row]].static}`}
                alt={droppingGrid[col][row]}
                width="130"
                height="130"
                in:fly={{ y: -80, duration: 350, delay: col * 40 }}
                style="opacity:1; transition:opacity 0.25s"
              />
            {/if}
          </div>
        {:else}
          <div class="symbol"></div>
        {/if}
      {/each}
    {/each}
  </div>
</main>
