export async function GET() {
  const res = await fetch('http://localhost:5000/api/spin');
  const data = await res.json();

  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' }
  });
}
