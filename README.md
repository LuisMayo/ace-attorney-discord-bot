# Ace Attorney Discord Bot
 Discord bot that turns comment chains into ace attorney scenes. Inspired by and using https://github.com/micah5/ace-attorney-reddit-bot
 Currently [being executed](https://discord.com/oauth2/authorize?client_id=806980920544460831&permissions=100352&scope=bot).
 
 For any problem that may be encountered, you can join the [discord support server](https://discord.gg/pcS4MPbRDU) and we'll try to fix it
 
 Check also the [Twiitter](https://github.com/LuisMayo/ace-attorney-twitter-bot), [Reddit](https://github.com/micah5/ace-attorney-reddit-bot) and [Telegram](https://github.com/LuisMayo/ace-attorney-telegram-bot) bots!
 
## Getting Started

### Prerequisites
 - Everything included in [/objection_engine/Readme.md](https://github.com/LuisMayo/objection_engine/blob/main/README.md#prerequisites).
 - Discord Bot Token. Obtain it from [Discord developer portal](https://discord.com/developers/)

#### Optional
 - [Google Translation API Credentials](https://cloud.google.com/translate/docs/setup): These are needed for language support other than English. Other languages may work even without this credentials as the system will fallback to TextBlob's translation system.
 
### Installing

1. Clone the repository with submodules

```
git clone --recursive https://github.com/LuisMayo/ace-attorney-discord-bot
```
2. Install dependencies of this repo and of objection engine. Refer to [objection engine's install instructions](https://github.com/LuisMayo/objection_engine/blob/main/README.md#installing) for any problems you may encounter
``` bash
python -m pip install -r requirements.txt
python -m pip install -r objection_engine/requirements.txt
```

3. Copy `config.yaml.example` into `config.yaml` and fill your token there

4. Start the project
`python main.py`


## Contributing
Since this is a tiny project we don't have strict rules about contributions. Just open a Pull Request to fix any of the project issues or any improvement you have percieved on your own. Any contributions which improve or fix the project will be accepted as long as they don't deviate too much from the project objectives. If you have doubts about whether the PR would be accepted or not you can open an issue before coding to ask for my opinion
