export async function POST(req: Request) {
  const { message } = await req.json();
  
  const response = await fetch("http://localhost:11434/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "qwen3:4b",
      messages: [{ role: "user", content: message }],
      stream: false  // Make sure this is false
    })
  });
  
  if (!response.ok) {
    return Response.json({ error: "Ollama error" }, { status: 500 });
  }
  
  const data = await response.json();
  console.log("Ollama response:", data); // Debug log
  
  return Response.json(data);
}