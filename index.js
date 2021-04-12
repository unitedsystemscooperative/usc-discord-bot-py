const DiscordJS = require('discord.js');
require('dotenv').config();

const zGuildID = process.env.GUILDID;
const client = new DiscordJS.Client();

const getApp = (guildId) => {
  const app = client.api.applications(client.user.id);
  if (guildId) {
    app.guilds(guildId);
  }
  return app;
};

const postServerCommand = async (data) => {
  await getApp(zGuildID).commands.post({ data });
};

const deleteServerCommand = async () => await getApp(zGuildID).commands('831280362541678623').delete();

const serverCommands = [
  {
    name: 'ping',
    description: 'simple ping pong command'
  },
  { name: 'hello', description: 'say hello' },
  { name: 'inarasquad', description: 'Send the Inara Squad Link to chat' },
];

client.on('ready', async () => {
  console.log('The bot is ready');

  const commands = await getApp(zGuildID).commands.get();
  console.log(commands);

  // await deleteServerCommand();

  for (const command of serverCommands) {
    await postServerCommand(command);
  }

  const reply = async (interaction, response) => {
    let data = {
      content: response
    };

    if (typeof response === 'object') {
      data = await createAPIMessage(interaction, response);
    }

    client.api.interactions(interaction.id, interaction.token).callback.post({
      data: {
        type: 4,
        data
      }
    });
  };

  const createAPIMessage = async (interaction, content) => {
    const { data, files } = await DiscordJS.APIMessage.create(client.channels.resolve(interaction.channel_id), content).resolveData().resolveFiles();

    return { ...data, files };
  };

  const createEmbed = (title, content) => {
    const embed = new DiscordJS.MessageEmbed();

    if (title) {
      embed.setTitle(title);
    }
    embed.setDescription(content);

    return embed;
  };

  client.ws.on('INTERACTION_CREATE', async (interaction) => {
    const command = interaction.data.name.toLowerCase();

    switch (command) {
      case 'ping':
        reply(interaction, 'pong');
        break;
      case 'hello':
        reply(interaction, 'Hello, World!');
        break;
      case 'inarasquad':
        const inaraSquadContent = '**Join the squad on Inara**\n\nIf you join the squad on Inara, we can assist further with build, engineering, and other tips! https://inara.cz/squadron/7028/';
        // const inaraSquadEmbed = createEmbed('Join the squad on Inara', inaraSquadContent);
        reply(interaction, inaraSquadContent);
      default:
        break;
    }
  });
});

client.login(process.env.TOKEN);
