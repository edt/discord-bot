# discord-bot


## Features

The following is a list of features the bot has:

- [x] generic image upload from folders with auto generated commands
- [x] reboot command
- [ ] reminder function to ping one or more people
  `!remind "Schnitzel" "datetime" @user1 @user2`

- [x] upload command to create new commands and/or add images to existing ones
  `!upload <command> <url>`
  Command should give warning if file is larger than 8 MB.
- [x] status command to retrieve info about server/bot

## Available commands

For general info or info about a specific command call `!help` or `!help command`.

`!help` - print info for user

`!status` - give a status overview over the server/bot

`!upload <cmd> <url>` - upload an image/video to the cmd. If the command does not exist it will automatically be created

`!roll NdX+Y` - roll dice

`!reboot` - reboot the bot

`!shutdown` - shut down the both

`!upgrade` - pull update from git and reboot

Commands of the category 'Images' are automatically generated and thus not documented.

These commands will randomly pick an image from a folder associated with the command and post it to the channel where the command was issued.


## Commandline Usage

The following arguments are available:

#### -h, --help

  Print arguments, etc.

#### -v[vvvv]

Set log level. Maximum is 5.

#### -c, --config <config.json>

Manually set the config that shall be used.

#### --reset

Purge cache before starting.

#### --data <directory>

Local directory for permanent local data.

## Config File

The default configuration file is called setting.ini.
It typically resides in the directory of discord-bot.

Alternative location can be specified with `--config`.

The content should look like:

```INI
[General]
token = discord-bot-oauth-token
data_dir = /usr/data/stuff
cache_dir = /var/data/discord-bot/cache

[reddit]
id = reddit-app-id
token = reddit-app-auth-token
agent = blob-bot script v1.0 by rawplus
```

## Dependencies

Currently this project has the following dependencies:

- discord.py
- PRAW
- tabulate

They can be installed with the following command on Debian based systems:

`sudo pip3 install discord.py praw tabulate`
