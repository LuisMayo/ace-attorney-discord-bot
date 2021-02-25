# Ace Attorney Discord Bot
 Telegram bot that turns comment chains into ace attorney scenes. Inspired by and using https://github.com/micah5/ace-attorney-reddit-bot
 Currently [being executed](https://discord.com/oauth2/authorize?client_id=806980920544460831&permissions=100352&scope=bot).
 
 For any problem that may be encountered, you can join the [discord support server](https://discord.gg/pcS4MPbRDU) and we'll try to fix it
 
 Check also the [Twiitter](https://github.com/LuisMayo/ace-attorney-twitter-bot), [Reddit](https://github.com/micah5/ace-attorney-reddit-bot) and [Telegram](https://github.com/LuisMayo/ace-attorney-telegram-bot) bots!
 
## Getting Started

### Prerequisites
Everything included in [/ace-attoney-bot/Readme.md](https://github.com/LuisMayo/ace-attorney-bot/blob/main/README.md). Which has been copied here for easy of use

 - Python 3
 - Discord Bot Token. Obtain it from [Discord developer portal](https://discord.com/developers/)
 - Ace Attorney data. Download it [here](https://drive.google.com/drive/folders/1jNpnB3pjHFvOyrfZ-WxlOXNaZ-XH4INx?usp=sharing) and put them in `./assets/`
 - FFMPEG instalation. In most Linux distros it should be available in the default package manager, although it may have some caveats (check note below). In Windows systems it'd include downloading a [pre-compiled zip folder](https://ffmpeg.org/download.html#build-windows), extracting it and adding the /bin folder into the [system path](https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/)
 
 
### Installing

1. Clone the repository with submodules

```
git clone --recursive https://github.com/LuisMayo/ace-attorney-discord-bot
```
2. Install dependencies of this repo and the child repo
``` bash
python -m pip install -r requirements.txt
python -m pip install -r ace-attorney-reddit-bot/requirements.txt
```

3. Put yout Token in a `token.txt` file

4. Start the project
`python main.py`

#### Note about Linux systems
In Linux it may be a bit harder to set the enviorenment properly. More specifically it may be hard to install required codecs.
If having a codec problem (like "couldn't find codec for id 27") you may need to compile ffmpeg and opencv by yourself.
You should be good using these guides (tested on Ubuntu with success and on Debian without success)
  - [FFMPEG compilation guide](https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu)
  - [Opencv compilation guide](https://docs.opencv.org/master/d2/de6/tutorial_py_setup_in_ubuntu.html)

## Contributing
Since this is a tiny project we don't have strict rules about contributions. Just open a Pull Request to fix any of the project issues or any improvement you have percieved on your own. Any contributions which improve or fix the project will be accepted as long as they don't deviate too much from the project objectives. If you have doubts about whether the PR would be accepted or not you can open an issue before coding to ask for my opinion
