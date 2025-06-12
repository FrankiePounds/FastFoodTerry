<script>
  let result = null;

  async function spin() {
    const res = await fetch('/spin');
    result = await res.json();
  }
</script>

<h1>🎰 Fast Food Terry</h1>
<button on:click={spin}>Spin!</button>

{#if result}
  <h2>Spin Result:</h2>
  <pre>{JSON.stringify(result, null, 2)}</pre>
{/if}
