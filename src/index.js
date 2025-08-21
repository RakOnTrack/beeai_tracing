const { BaseAgent, ChatModel, Logger, LoggerLevel } = require('beeai-framework');
const config = require('./config');

// Set up logging
const logger = new Logger(LoggerLevel.INFO);

async function main() {
  try {
    console.log('🐝 Welcome to your first BeeAI project!');
    console.log('🚀 Using BeeAI Framework for Node.js');
    
    // Check if config loaded properly
    console.log('📋 Configuration loaded:', {
      agentName: config.agent.name,
      agentDescription: config.agent.description,
      hasApiKey: !!config.beeai.apiKey
    });
    
    // Create a chat model (this would typically connect to an LLM provider)
    const chatModel = new ChatModel({
      name: 'example-chat-model',
      description: 'A simple chat model for demonstration',
    });
    
    console.log('✅ Chat model created:', chatModel.name);
    
    // Create a simple agent that extends BaseAgent
    class MyFirstBeeAgent extends BaseAgent {
      constructor() {
        super({
          name: config.agent.name || 'MyFirstBeeAgent',
          description: config.agent.description || 'A simple BeeAI agent for learning',
          instructions: config.agent.instructions || 'You are a helpful AI assistant.',
        });
        
        // Ensure the name is set properly
        this.name = config.agent.name || 'MyFirstBeeAgent';
        this.description = config.agent.description || 'A simple BeeAI agent for learning';
      }
      
      async processMessage(message) {
        // Simple echo response for demonstration
        return `Hello! I'm ${this.name}. You said: "${message}". I'm here to help you learn about AI!`;
      }
    }
    
    const agent = new MyFirstBeeAgent();
    console.log('✅ Agent created successfully:', agent.name);
    
    // Example conversation
    const response = await agent.processMessage('Hello! Can you tell me about BeeAI?');
    console.log('🤖 Agent response:', response);
    
    // Log some framework information
    logger.info('BeeAI Framework version:', require('beeai-framework/package.json').version);
    logger.info('Project setup completed successfully!');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    
    if (error.message.includes('BEEAI_API_KEY')) {
      console.log('\n💡 Setup Instructions:');
      console.log('1. Copy .env.example to .env');
      console.log('2. Add your BeeAI API key to .env');
      console.log('3. Get your API key from: https://beeai.com');
    } else {
      console.log('💡 Check the README.md for troubleshooting tips.');
    }
  }
}

// Run the main function
if (require.main === module) {
  main();
}

module.exports = { main };
