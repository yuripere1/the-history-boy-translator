// History Boy Translator backend
// Node 18+ recommended. No framework required.
const http = require("http");

const PORT = process.env.PORT || 3000;
const KEY = process.env.OPENROUTER_API_KEY;

const SYSTEM = `You translate text into the "History Boy" texting voice.

Core voice:
- Direct and conversational
- Emotionally open
- Affectionate without being overly poetic
- Apologetic whenever the speaker thinks they crossed a boundary
- Reassuring and low-pressure
- Informal and somewhat spontaneous
- Occasionally awkward or grammatically incomplete in a natural, human way
- Emotionally expressive and comfortable admitting vulnerability
- Occasionally self-deprecating
- More interested in sincerity than polished prose

Sentence structure:
- Short sentences
- Sentence fragments
- Simple clauses
- Occasional omitted subjects or words
- Frequent line breaks
- Informal transitions
- Repetition when emotionally appropriate
- Simple conjunctions such as and, but, because, and so
- Thoughts may appear in natural emotional order rather than perfectly organized prose
- Do NOT unnecessarily combine short sentences into sophisticated sentences.

Emotional patterns:
- I'm sorry.
- No worries.
- Whenever you're ready.
- Feel free to text.
- That's absolutely ok.
- Tell me and we will or won't do them.
- Hope you are doing well.
- I just think you are cool.
Strong feelings can coexist with giving the other person permission to create distance.
The speaker often emphasizes that the person they are talking about is cool.

Vocabulary:
cool, absolutely, very, just, feel free, whenever, ready, talk, text, respond,
sorry, apologize, no worries, special, brighter, love, miss, catch up, tell me,
until then, pard, bf, set, studio, footage.

Informality:
Casual conventions such as Haha, bf, Imk, convos, pard, lowercase and, parenthetical
expressions like (:, and mild imperfect grammar can be used when natural.

Meaning:
Preserve the source meaning above all else. Do not add emotional intensity, affection,
romance, apology, certainty, or vulnerability that isn't present. Do not make the
speaker colder or more formal. If ambiguous, preserve ambiguity.

Output ONLY the translated text. No explanation, no quotation marks, no preamble.`;

function send(res, code, data){
  res.writeHead(code, {"Content-Type":"application/json","Access-Control-Allow-Origin":"*"});
  res.end(JSON.stringify(data));
}
const server=http.createServer(async(req,res)=>{
  if(req.method==="OPTIONS"){res.writeHead(204,{"Access-Control-Allow-Origin":"*","Access-Control-Allow-Headers":"Content-Type"});return res.end();}
  if(req.method!=="POST" || req.url!=="/api/translate"){return send(res,404,{error:"Not found"});}
  if(!KEY)return send(res,500,{error:"OPENROUTER_API_KEY is not configured on the server."});
  let body="";
  req.on("data",c=>body+=c);
  req.on("end",async()=>{
    try{
      const {text,model="openrouter/free"}=JSON.parse(body||"{}");
      if(!text?.trim()) return send(res,400,{error:"Missing text"});
      const response=await fetch("https://openrouter.ai/api/v1/chat/completions",{
        method:"POST",
        headers:{
          "Authorization":"Bearer "+KEY,
          "Content-Type":"application/json",
          "HTTP-Referer":"http://localhost:"+PORT,
          "X-Title":"History Boy Translator"
        },
        body:JSON.stringify({
          model,
          messages:[{role:"system",content:SYSTEM},{role:"user",content:text}],
          temperature:0.8
        })
      });
      const data=await response.json();
      if(!response.ok)return send(res,response.status,{error:data?.error?.message||"OpenRouter request failed"});
      const translation=data?.choices?.[0]?.message?.content?.trim();
      if(!translation)return send(res,502,{error:"Model returned no translation"});
      send(res,200,{translation});
    }catch(e){send(res,500,{error:e.message||"Server error"});}
  });
});
server.listen(PORT,()=>console.log(`History Boy Translator backend running at http://localhost:${PORT}`));
