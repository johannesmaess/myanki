import OpenAI from "openai";

const openai = new OpenAI({
    organization: "org-SrHoj75PJe64vfi44tVZkwGL",
    apiKey: "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"
});

const chatCompletion = await openai.chat.completions.create({
    model: "gpt-3.5-turbo",
    messages: [{"role": "user", "content": "Hello!"}],
  });
  
console.log(chatCompletion.choices[0].message);