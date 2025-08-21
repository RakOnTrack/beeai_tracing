require('dotenv').config();

const config = {
  beeai: {
    apiKey: process.env.BEEAI_API_KEY,
    model: process.env.BEEAI_MODEL || 'gpt-4',
    timeout: parseInt(process.env.BEEAI_TIMEOUT) || 30000,
    maxTokens: parseInt(process.env.BEEAI_MAX_TOKENS) || 1000,
  },
  agent: {
    name: 'MyFirstBeeAgent',
    description: 'A simple BeeAI agent for learning and experimentation',
    instructions: `You are a helpful AI assistant powered by BeeAI. 
    Your role is to help users learn about AI, answer questions, and provide guidance.
    Always be friendly, informative, and encourage learning.`,
  },
};

module.exports = config;
